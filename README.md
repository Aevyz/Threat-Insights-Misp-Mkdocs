# HvS Threat Insights - MkDocs Edition

A modern, searchable static website for browsing MISP threat intelligence events from HvS-Consulting's feed, built with MkDocs Material theme.

## Features

- **Powerful Search**: Full-text search across all events, tags, and indicators powered by MkDocs Material
- **Modern UI**: Clean, responsive design using Material Design components
- **HvS Brand Colors**: Custom color scheme matching HvS-Consulting brand identity
- **Advanced Filtering**: Built-in search features with suggestions and highlighting
- **Static Generation**: Pure markdown to HTML - deploy anywhere
- **Easy Maintenance**: No custom templating - just markdown and MkDocs configuration

## Quick Start

### 1. Install Dependencies

Create a virtual environment and install requirements:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Fetch Latest Data

Download the latest threat intelligence from the MISP feed:

```bash
python fetch_data.py
```

This creates a `data/` directory with all event information in JSON format.

### 3. Build Documentation

Generate markdown files from the MISP data:

```bash
python build.py
```

This populates the `docs/` directory with markdown files for each event.

### 4. View Locally

Start the MkDocs development server:

```bash
mkdocs serve
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Deployment

### Build Static Site

Generate the complete static site:

```bash
mkdocs build
```

This creates a `site/` directory with production-ready HTML files.

### Deploy to GitHub Pages

```bash
mkdocs gh-deploy
```

This automatically builds and pushes to your repository's `gh-pages` branch.

### Deploy to Netlify

1. Run `mkdocs build` to generate the `site/` directory
2. Drag and drop the `site/` folder to Netlify's web interface

Or configure continuous deployment:

**netlify.toml**:
```toml
[build]
  command = "pip install -r requirements.txt && python fetch_data.py && python build.py && mkdocs build"
  publish = "site"
```

### Deploy to Vercel

Install Vercel CLI and deploy:

```bash
vercel --prod
```

Configure build settings:
- **Build Command**: `pip install -r requirements.txt && mkdocs build`
- **Output Directory**: `site`

## Project Structure

```
misp-threat-insights-mkdocs/
├── mkdocs.yml              # MkDocs configuration
├── requirements.txt        # Python dependencies
├── fetch_data.py           # Downloads MISP feed data
├── build.py                # Generates markdown from JSON data
├── docs/
│   ├── index.md            # Main landing page (auto-generated)
│   ├── events/             # Individual event pages (auto-generated)
│   └── stylesheets/
│       └── extra.css       # HvS brand color customizations
├── data/                   # Downloaded MISP data (gitignored)
└── site/                   # Generated static site (gitignored)
```

## Customization

### Update Feed URL

Edit [fetch_data.py](fetch_data.py) and change the `FEED_BASE_URL` constant:

```python
FEED_BASE_URL = "https://your-misp-instance.com/feed/your-feed/"
```

### Modify Colors

The HvS brand colors are defined in [docs/stylesheets/extra.css](docs/stylesheets/extra.css). Update the CSS variables to change the color scheme:

```css
:root {
    --hvs-blue-400: #00335E;
    --hvs-blue-350: #1C496F;
    /* ... more colors ... */
}
```

### Configure MkDocs

Edit [mkdocs.yml](mkdocs.yml) to modify site settings, navigation, plugins, and theme options. See the [MkDocs documentation](https://www.mkdocs.org/) for available options.

### Add Custom Pages

Create new markdown files in the `docs/` directory and add them to the `nav` section in `mkdocs.yml`.

## Search Features

The Material theme provides advanced search capabilities out of the box:

- **Real-time Search**: Instant results as you type
- **Search Suggestions**: Smart suggestions based on content
- **Search Highlighting**: Highlighted matches in results
- **Keyboard Shortcuts**: Press `F` or `S` to focus search
- **Deep Linking**: Share search results with URL parameters

## Automation

Keep the site updated with the latest threat intelligence using a cron job:

```bash
# Update every 6 hours
0 */6 * * * cd /path/to/misp-threat-insights-mkdocs && \
  ./venv/bin/python fetch_data.py && \
  ./venv/bin/python build.py && \
  mkdocs gh-deploy --force
```

## Advantages Over Jinja2 Approach

This MkDocs-based implementation offers several benefits:

1. **Maintainability**: No custom templating code to maintain
2. **Built-in Search**: Powerful search without custom JavaScript
3. **Theme Ecosystem**: Access to Material theme updates and plugins
4. **Easy Customization**: CSS overrides instead of template modifications
5. **Better SEO**: Semantic HTML and proper meta tags by default
6. **Responsive Design**: Mobile-optimized out of the box
7. **Accessibility**: WCAG-compliant components
8. **Version Control**: Markdown is easier to track than HTML templates

## Requirements

- Python 3.8+
- MkDocs 1.5+
- MkDocs Material 9.5+
- Internet connection (to fetch MISP data)

## License

MIT License - feel free to use and modify for your needs.

## Credits

- Powered by [MISP](https://www.misp-project.org/) threat intelligence data
- Built with [MkDocs](https://www.mkdocs.org/) and [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- HvS-Consulting brand colors and design
