# Deployment Guide for Your Chirpy Blog

## Overview
Your blog is now ready with 2 technical posts:
1. **OCI Migrations Deep Dive** - Cloud migration architecture and lessons learned
2. **Bridging the Metaverse** - Web3 identity and cross-chain interoperability

## Quick Start Options

### Option 1: Deploy to GitHub Pages (Recommended)

1. **Create a GitHub repository:**
   ```bash
   cd /Users/gc/Downloads/Blogs/chirpy-blog
   git init
   git add .
   git commit -m "Initial commit: Tech blog with 2 posts"
   ```

2. **Push to GitHub:**
   ```bash
   # Create a new repository on GitHub named "blog" or "tech-insights"
   git remote add origin https://github.com/d14znet/blog.git
   git branch -M main
   git push -u origin main
   ```

3. **Enable GitHub Pages:**
   - Go to repository Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main` / `(root)`
   - Click Save

4. **Wait for deployment:**
   - GitHub Actions will automatically build and deploy your site
   - Your blog will be available at: `https://d14znet.github.io/blog/`
   - First deployment takes 2-3 minutes

### Option 2: Test Locally (Requires Ruby/Docker)

**Using Docker (if Docker Desktop is running):**
```bash
cd /Users/gc/Downloads/Blogs/chirpy-blog
docker run --rm -v "$PWD":/srv/jekyll -p 4000:4000 jekyll/jekyll:4.2.2 jekyll serve --host 0.0.0.0
```
Then visit: http://localhost:4000

**Using Local Ruby (requires Ruby >= 3.0):**
```bash
cd /Users/gc/Downloads/Blogs/chirpy-blog
bundle install
bundle exec jekyll serve
```
Then visit: http://localhost:4000

### Option 3: Deploy to Netlify

1. **Push to GitHub** (see Option 1, steps 1-2)

2. **Connect to Netlify:**
   - Go to https://app.netlify.com
   - Click "Add new site" → "Import an existing project"
   - Connect your GitHub repository
   - Build settings:
     - Build command: `jekyll build`
     - Publish directory: `_site`

3. **Deploy:**
   - Netlify will automatically build and deploy
   - You'll get a URL like: `https://your-site.netlify.app`
   - You can configure a custom domain in Netlify settings

## Blog Structure

```
chirpy-blog/
├── _config.yml          # Site configuration
├── _posts/              # Blog posts
│   ├── 2025-10-13-oci-migrations-deep-dive.md
│   └── 2025-10-14-bridging-the-metaverse.md
├── _tabs/               # Navigation pages (About, Archives, etc.)
├── assets/              # Images, CSS, JS
└── index.html           # Home page
```

## Customization

### Adding More Posts
Create new files in `_posts/` with this naming convention:
```
YYYY-MM-DD-title-slug.md
```

Use this front matter template:
```yaml
---
title: "Your Post Title"
date: YYYY-MM-DD HH:MM:SS -0400
categories: [Category1, Category2]
tags: [tag1, tag2, tag3]
author: Gaurav Chandra
description: "Brief description for SEO"
---
```

### Updating Site Info
Edit `_config.yml`:
- Change `url` to your GitHub Pages URL
- Update social links
- Modify theme settings

### Adding Images
Place images in `assets/img/posts/` and reference them:
```markdown
![Alt text](/assets/img/posts/your-image.jpg)
```

## Sharing Your Blog

Once deployed, share these links:

### Individual Posts:
- OCI Migration: `https://d14znet.github.io/blog/posts/oci-migrations-deep-dive/`
- Metaverse Identity: `https://d14znet.github.io/blog/posts/bridging-the-metaverse/`

### Social Media Sharing:
Both posts include:
- SEO-optimized meta descriptions
- Proper Open Graph tags for preview cards
- Author attribution
- Reading time estimates

## Troubleshooting

### GitHub Pages Not Building?
- Check Actions tab for build errors
- Ensure `_config.yml` has correct `baseurl: "/blog"` if not using root domain
- Verify all markdown files have proper front matter

### Missing Styles?
- Check `_config.yml` `url` and `baseurl` settings
- Clear browser cache
- Wait 5 minutes for CDN propagation

### Posts Not Showing?
- Verify post dates aren't in the future
- Check file naming: `YYYY-MM-DD-slug.md`
- Ensure front matter is valid YAML

## Next Steps

1. **Deploy to GitHub Pages** (fastest option)
2. **Add images** to enhance your posts (optional)
3. **Customize About page** in `_tabs/about.md`
4. **Add Google Analytics** in `_config.yml` (optional)
5. **Set up comments** using Giscus or Utterances (optional)

## Support

- Chirpy theme docs: https://chirpy.cotes.page/
- Jekyll docs: https://jekyllrb.com/docs/
- GitHub Pages docs: https://docs.github.com/en/pages

---

**Your blog is ready to go! Choose a deployment option above and share your technical insights with the world.**
