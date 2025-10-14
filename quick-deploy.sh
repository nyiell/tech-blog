#!/bin/bash

# Quick Deploy Script for Chirpy Blog
# This script helps you deploy your blog to GitHub Pages quickly

set -e

echo "=========================================="
echo "   Tech Insights Blog - Quick Deploy"
echo "=========================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✓ Git initialized"
else
    echo "✓ Git repository already initialized"
fi

echo ""
echo "🎯 Next steps to deploy your blog:"
echo ""
echo "1. Create a new GitHub repository:"
echo "   - Go to: https://github.com/new"
echo "   - Repository name: blog (or any name you prefer)"
echo "   - Make it public"
echo "   - Don't add README, .gitignore, or license (already included)"
echo ""
echo "2. Run these commands:"
echo "   git add ."
echo "   git commit -m 'Initial commit: Tech blog with 2 posts'"
echo "   git remote add origin https://github.com/d14znet/blog.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Enable GitHub Pages:"
echo "   - Go to repository Settings → Pages"
echo "   - Source: Deploy from a branch"
echo "   - Branch: main / (root)"
echo "   - Click Save"
echo ""
echo "4. Wait 2-3 minutes, then visit:"
echo "   https://d14znet.github.io/blog/"
echo ""
echo "=========================================="
echo ""
echo "📄 For detailed instructions, see: DEPLOYMENT.md"
echo "👀 For a preview, open: PREVIEW.html"
echo ""
echo "Your blog is ready to go! 🚀"
echo ""
