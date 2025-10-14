---
title: "My Unexpected Experience with OCI Migrations: A Deep Dive"
date: 2025-10-13 10:00:00 -0400
categories: [Cloud Architecture, Migration]
tags: [oci, aws, cloud-migration, oracle, infrastructure]
author: Gaurav Chandra
description: "What I learned orchestrating large-scale AWS-to-OCI migrations while navigating tag validation conflicts, hydration agents, and the hidden complexities of Oracle Cloud Migrations"
image:
  path: /assets/img/posts/oci-migration.jpg
  alt: Oracle Cloud Infrastructure Migration Architecture
---

When I started this AWS-to-OCI migration project, I expected the typical challenges: network configuration, performance tuning, maybe some application compatibility issues. What I didn't expect was to spend weeks deep in the weeds of OCI's tag validation system, reverse-engineering hydration agent behavior through API calls, and coordinating with Oracle support across multiple tenancies while building a comprehensive post-migration orchestration architecture.

Here's the contrarian truth that took me too long to realize: **Cloud migrations aren't primarily about moving workloads—they're about understanding the hidden architectural assumptions of your target platform**. Oracle Cloud Infrastructure's tag-based hierarchical governance model, its availability domain constraints, and its replication architecture are fundamentally different from AWS in ways that the documentation doesn't fully prepare you for.

This post is the technical deep dive I wish I'd had at the start. It covers:
- The real architecture of Oracle Cloud Migrations (OCM) service and how it actually works under the hood
- Why tag validation became our biggest blocker and the three workarounds we discovered
- The replication mechanics involving hydration agents, golden volumes, and crash-consistent snapshots
- Post-migration orchestration architecture using Ansible Tower, database replication, and backup strategies
- Practical lessons learned from coordinating across multiple stakeholders and analyzing OCI APIs

If you're planning an AWS-to-OCI migration at scale, or if you're curious about the architectural patterns that govern cross-cloud migrations, this is for you.

---

## Understanding the OCM Service Architecture: Beyond the UI

### The Mental Model Problem

The Oracle Cloud Migrations UI presents a deceptively simple hierarchy: you create a Migration Project, add Migration Plans, and click "Replicate." But this abstraction hides critical architectural details that will bite you if you don't understand what's happening underneath.

Here's what I learned through extensive API analysis and coordination with Oracle's engineering team:

<img src="/assets/img/diagrams/oci-architecture.svg" alt="OCM Service Architecture" style="width: 100%; max-width: 900px; display: block; margin: 20px auto;">

**Caption:** The OCM service separates concerns between replication (moving data) and launching (creating compute). This distinction is crucial for understanding parallelization limits and troubleshooting failures.

### The Three-Layer Separation

What makes OCM unique is its strict separation of concerns:

1. **Replication Layer**: Managed by hydration agents, creates "golden volumes" that are immutable snapshots
2. **Planning Layer**: Configuration metadata that maps how golden volumes become running instances
3. **Deployment Layer**: User-controlled Terraform execution that creates actual compute resources

This separation enables fascinating capabilities:
- Replicate once, launch multiple times with different configurations
- Test different instance shapes without re-transferring data
- Keep golden volumes synchronized with source while running multiple test environments

But it also introduces complexity that the UI obscures. For example, you can't "replicate a migration plan"—replication happens at the Migration Asset level, which exists in the Migration Project scope. The plan is just metadata about how to launch.

### The Hydration Agent: OCM's Secret Weapon

The hydration agent deserves special attention because it's the workhorse of the entire system. Here's how it actually works:

<img src="/assets/img/diagrams/oci-hydration.svg" alt="Hydration Agent Sequence" style="width: 100%; max-width: 900px; display: block; margin: 20px auto;">

**Caption:** The hydration agent is ephemeral—it exists only during replication. It acts as a streaming proxy between AWS snapshots and OCI block volumes, with no intermediate object storage involved (unlike VMware migrations).

**Key Insight**: For AWS migrations, data flows directly from AWS EBS snapshots to OCI block volumes via the hydration agent. There's no object storage bucket involved, unlike migrations from VMware where images are temporarily stored in object storage. This direct streaming approach is more efficient but requires the hydration agent to have network connectivity to both AWS and OCI APIs simultaneously.

### The Availability Domain Constraint

This is where things get interesting for large-scale migrations. OCI has a hard limit: **10 concurrent hydration agents per Availability Domain per tenancy**.

<img src="/assets/img/diagrams/oci-availability.svg" alt="Availability Domain Distribution" style="width: 100%; max-width: 800px; display: block; margin: 20px auto;">

**Caption:** To parallelize beyond 10 replications, you must distribute assets across multiple Availability Domains or create multiple Migration Projects. In regions with only one AD (like Chicago), you're hard-capped at 10 concurrent replications.

**The Workaround for Scale**: If you need to migrate hundreds of VMs, you have two options:
1. **Spatial distribution**: Spread assets across multiple ADs in the same region (max 30 concurrent in Ashburn with 3 ADs)
2. **Project multiplication**: Create multiple Migration Projects, each with its own set of assets

The Oracle team I worked with mentioned that their cloud lift teams use a "one project, one asset" model when integrating with external orchestration engines. This maximizes flexibility but requires building your own coordination layer on top of OCM APIs.

---

## The Tag Validation Crisis: When Governance Meets Migration

### The Problem That Stopped Everything

About two weeks into the project, we hit a wall. Every discovery operation in our `ocicloudinternal` tenant was failing with this error:

```
Error returned by CreateAsset operation in Inventory service.
(400, InvalidParameter, false) Invalid tags
```

The error was cryptic. The migration worked fine in our `ocideltekengineering` tenant, but failed consistently in another tenant with identical-looking configurations. After extensive coordination with Oracle support (SR 4-0001062947), we uncovered something fundamental about how OCI's tag validation actually works.

### How OCI Tag Validation Really Works

OCI's tagging system implements a hierarchical governance model that validates tags at multiple levels:

<img src="/assets/img/diagrams/oci-tags.svg" alt="Tag Validation Flow" style="width: 100%; max-width: 800px; display: block; margin: 20px auto;">

**Caption:** Tag validation in OCI checks parent compartment rules during resource creation. User-applied tags can conflict with parent tag defaults, causing validation failures that aren't obvious from the UI.

**The Root Cause**: According to Oracle support's analysis, the OCM service was failing because:

1. **Parent compartments** had Tag Defaults that required specific values (e.g., `CostCenter=<required>`)
2. **Migration compartments** had user-applied tags with different values
3. **During asset creation**, OCI's API validated against parent rules and rejected the conflicting configuration
4. **The UI never exposed** which specific tag was causing the conflict or where to configure the reconciliation

This is a design pattern in OCI's governance model: tags flow downward through the hierarchy, but validation flows upward. Resources inherit tag defaults from parents, but parent rules can also block child resource creation if tags conflict.

### The Three Workarounds We Discovered

After weeks of coordination with Oracle support and internal testing, we identified three approaches:

#### Workaround 1: Delete User-Applied Tags (Not Viable for Us)

```bash
# Option 1: Remove all user-applied tags from the migration compartment
# This wasn't viable because our organization requires tags for billing
```

**Why it works**: Removes the conflict source entirely
**Why we couldn't use it**: Enterprise governance required tags on all resources

#### Workaround 2: Convert User-Applied Tags to Tag Defaults (Temporary Testing Solution)

```bash
# Option 2: Change user-applied tags to tag defaults
# Navigate to: Identity & Security -> Compartments -> [Migration Compartment] -> Tag Defaults

oci iam tag-default create \
  --compartment-id <migration_compartment_id> \
  --tag-definition-id <tag_def_id> \
  --value "DefaultValue"
```

**Why it works**: Tag Defaults can be validated against parent rules during compartment configuration, before resource creation
**Why it's only temporary**: Loses the flexibility of user-applied tags; not suitable for production

#### Workaround 3: Use Terraform/APIs with Explicit Tag Handling (Production Solution)

This became our production approach. Instead of using the UI, we used Terraform to set up prerequisites and APIs for discovery/replication:

```hcl
# Terraform approach: Explicitly define tag values that reconcile with parent rules
resource "oci_cloud_bridge_asset_source" "aws_source" {
  compartment_id  = var.migration_compartment_id
  type            = "VMWARE"  # Despite the name, used for AWS too
  display_name    = "AWS-Production-Source"

  # Explicitly pass tags that match parent requirements
  freeform_tags = {
    "CostCenter" = var.cost_center_from_parent
    "Environment" = "Migration"
  }

  defined_tags = {
    "${var.tag_namespace}.${var.tag_key}" = var.tag_value_matching_parent_default
  }

  # AWS connection details
  assets_compartment_id = var.assets_compartment_id
  discovery_credentials {
    type            = "BASIC"
    secret_id       = var.aws_credentials_secret_id
  }
}
```

**The Key Insight**: The OCM APIs allow you to pass tag values directly during asset creation. This bypasses the UI's inability to prompt for required tags and lets you programmatically resolve conflicts with parent Tag Defaults.

---

## Key Takeaways: What I'd Do Differently

After months of navigating this migration, here are the insights I'd share with my past self:

### 1. Understand Tag Governance Before You Start

**Don't**: Assume tag validation "just works" and discover conflicts during discovery
**Do**: Audit your tag namespace, validators, and Tag Defaults across the entire compartment hierarchy **before** creating asset sources

**Time saved**: At least 2 weeks of troubleshooting

### 2. Go API-First for Anything Non-Trivial

**Don't**: Rely on the UI for complex tag configurations or large-scale migrations
**Do**: Invest upfront in Terraform/API workflows using OCI CLI and Python SDK

**Time saved**: Countless hours of clicking through UI forms and manually debugging tag errors

### 3. Design Post-Migration Orchestration Early

**Don't**: Wait until after replication to think about configuration management, database sync, and backups
**Do**: Stand up Ansible Tower (or equivalent) and design your post-migration architecture in parallel with OCM setup

**Time saved**: Avoids "migration complete but not production-ready" limbo

### 4. Test Crash-Consistent Recovery Procedures

**Don't**: Assume databases will boot cleanly after crash-consistent snapshots
**Do**: Launch test instances early and validate database recovery, check for corruption, measure recovery time

**Time saved**: Avoids cutover-day surprises

### 5. Distribute Assets Across Availability Domains from the Start

**Don't**: Put all assets in one AD and hit the 10-hydration-agent limit
**Do**: Assign target ADs during migration asset creation to maximize parallelization (30 concurrent in Ashburn)

**Time saved**: Dramatically reduces overall replication time for large migrations

---

## Conclusion: The Migration Journey Is the Product

If there's one meta-lesson from this experience, it's this: **the migration itself is a product you're building**. It has requirements (move VMs from AWS to OCI), architecture (OCM + Ansible + database replication), and users (application teams, DBAs, security).

Treat it like you would any engineering project:
- Design the architecture thoughtfully
- Prototype and iterate
- Document obsessively
- Coordinate across stakeholders
- Build automation to reduce toil
- Learn from failures and refine

The OCM service is a powerful tool, but it's just one component in a larger system you're building. The value comes from how you integrate it with your organization's processes, governance requirements, and operational workflows.

For me, this migration was as much about coordination, problem-solving, and architectural thinking as it was about moving VMs. The technical challenges—tag validation, hydration agents, crash-consistent snapshots—were puzzles that deepened my understanding of both OCI's design philosophy and the realities of multi-cloud operations.

If you're embarking on a similar journey, I hope this deep dive gives you the insights to navigate it more smoothly than I did. And if you hit a wall with tag validation errors or hydration agent limits, at least now you'll know you're not alone—and you'll have a roadmap to get unstuck.

---

*Generated with deep technical analysis and real-world battle scars from cloud migration trenches.*
