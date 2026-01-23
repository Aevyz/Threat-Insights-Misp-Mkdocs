#!/bin/bash
# Quick push script for deploying to GitHub

set -e

echo "🚀 Pushing MISP Threat Insights to GitHub..."
echo ""

# Check if we have uncommitted changes
if [[ -n $(git status -s) ]]; then
    echo "📝 You have uncommitted changes:"
    git status -s
    echo ""
    read -p "Do you want to commit these changes? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter commit message: " commit_msg
        git add .
        git commit -m "$commit_msg"
    fi
fi

# Push to GitHub
echo "📤 Pushing to GitHub..."
if git push -u origin main; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "Next steps:"
    echo "1. Enable GitHub Pages at:"
    echo "   https://github.com/Aevyz/Threat-Insights-Misp-Mkdocs/settings/pages"
    echo ""
    echo "2. Monitor deployment at:"
    echo "   https://github.com/Aevyz/Threat-Insights-Misp-Mkdocs/actions"
    echo ""
    echo "3. View site at:"
    echo "   https://aevyz.github.io/Threat-Insights-Misp-Mkdocs/"
    echo ""
else
    echo ""
    echo "❌ Push failed. You may need to authenticate."
    echo ""
    echo "Try one of these options:"
    echo "1. GitHub CLI: gh auth login"
    echo "2. Personal Access Token: git push (enter token as password)"
    echo "3. SSH: git remote set-url origin git@github.com:Aevyz/Threat-Insights-Misp-Mkdocs.git"
    echo ""
    echo "See DEPLOYMENT.md for more details."
    exit 1
fi
