# Deployment Guide

## Quick Deployment to GitHub

The repository is ready to push! Here's how to deploy:

### 1. Push to GitHub

```bash
# You'll need to authenticate with GitHub
git push -u origin main
```

If you need to authenticate, you have several options:

**Option A: Use GitHub CLI (Recommended)**
```bash
gh auth login
git push -u origin main
```

**Option B: Use Personal Access Token**
```bash
# Create a token at: https://github.com/settings/tokens
# Then use it as your password when prompted
git push -u origin main
```

**Option C: Use SSH**
```bash
# Change remote to SSH
git remote set-url origin git@github.com:Aevyz/Threat-Insights-Misp-Mkdocs.git
git push -u origin main
```

### 2. Enable GitHub Pages

After pushing, you need to enable GitHub Pages:

1. Go to: https://github.com/Aevyz/Threat-Insights-Misp-Mkdocs/settings/pages
2. Under "Source", you'll see the GitHub Actions workflow is ready
3. The first deployment will run automatically after the first push

### 3. Verify Deployment

Once the GitHub Action completes:

- **GitHub Pages URL**: https://aevyz.github.io/Threat-Insights-Misp-Mkdocs/
- **Action Status**: https://github.com/Aevyz/Threat-Insights-Misp-Mkdocs/actions

## What the GitHub Action Does

The workflow (`.github/workflows/deploy.yml`) will:

1. **On every push to main**: Rebuild and deploy the site
2. **Every 6 hours**: Automatically fetch latest threat intelligence and rebuild
3. **Manual trigger**: You can trigger it manually from the Actions tab

### Workflow Steps:

1. Fetch latest MISP threat intelligence data
2. Generate markdown documentation from the data
3. Build the MkDocs static site
4. Deploy to GitHub Pages

## Manual Deployment (Local)

If you want to build and test locally before pushing:

```bash
# Fetch latest data
python fetch_data.py

# Build markdown docs
python build.py

# Build MkDocs site
mkdocs build

# Preview locally
mkdocs serve
```

## Updating Threat Intelligence

The site will automatically update every 6 hours via GitHub Actions. To manually trigger an update:

1. Go to: https://github.com/Aevyz/Threat-Insights-Misp-Mkdocs/actions
2. Click on "Deploy MkDocs to GitHub Pages"
3. Click "Run workflow"
4. Select the main branch
5. Click "Run workflow"

## Customization

### Change Update Frequency

Edit `.github/workflows/deploy.yml` and modify the cron schedule:

```yaml
schedule:
  # Run every 6 hours (current)
  - cron: '0 */6 * * *'

  # Examples:
  # Every hour: '0 * * * *'
  # Every 12 hours: '0 */12 * * *'
  # Daily at midnight: '0 0 * * *'
```

### Change MISP Feed URL

Edit `fetch_data.py` and update the `FEED_BASE_URL`:

```python
FEED_BASE_URL = "https://your-misp-instance.com/feed/your-feed/"
```

### Customize Colors

Edit `docs/stylesheets/extra.css` to change the HvS brand colors.

## Troubleshooting

### Action Fails on First Run

If the GitHub Action fails on the first run, it's likely because:

1. **Pages not enabled**: Go to Settings > Pages and enable GitHub Pages
2. **Permissions issue**: Go to Settings > Actions > General > Workflow permissions and select "Read and write permissions"

### Data Fetch Fails

The workflow is configured with `continue-on-error: true` for data fetching, so if the MISP feed is temporarily unavailable, it will use the last successfully fetched data.

### Preview Before Deploying

Always test locally first:

```bash
mkdocs serve
```

Then visit http://127.0.0.1:8000 to preview changes.
