#!/usr/bin/env python3
"""
Build markdown files from MISP data for MkDocs.
"""
import json
from pathlib import Path
from typing import Dict, Any, List


def get_threat_level_name(level_id: int) -> str:
    """Convert threat level ID to human-readable name."""
    levels = {
        1: "High",
        2: "Medium",
        3: "Low",
        4: "Undefined"
    }
    return levels.get(level_id, "Unknown")


def get_analysis_name(analysis_id: int) -> str:
    """Convert analysis ID to human-readable name."""
    analysis = {
        0: "Initial",
        1: "Ongoing",
        2: "Complete"
    }
    return analysis.get(analysis_id, "Unknown")


def format_tags(tags: List[Dict[str, Any]]) -> str:
    """Format tags as markdown badges."""
    if not tags:
        return ""

    tag_html = []
    for tag in tags:
        name = tag.get("name", "")
        # Skip redundant tag
        if name == 'hvs:sharing="threat-insights"':
            continue
        # Escape special characters
        name_clean = name.replace('"', '&quot;')
        tag_html.append(f'<span class="tag">{name_clean}</span>')

    return " ".join(tag_html)


def format_indicators(indicators: Dict[str, List[Dict[str, Any]]]) -> str:
    """Format indicators as markdown sections."""
    output = []

    sections = [
        ("URLs", "urls"),
        ("Domains", "domains"),
        ("IP Addresses", "ips"),
        ("Hashes", "hashes"),
        ("Email Addresses", "emails"),
        ("Other Indicators", "other")
    ]

    for title, key in sections:
        items = indicators.get(key, [])
        if not items:
            continue

        output.append(f"\n#### {title}\n\n")

        for item in items:
            value = item.get("value", "")
            comment = item.get("comment", "")
            attr_type = item.get("type", "")

            # Each indicator as a card
            output.append('<div class="indicator-card" markdown="1">\n\n')

            output.append(f"`{value}`\n\n")

            if attr_type:
                output.append(f"**Type:** {attr_type}\n\n")

            if comment:
                output.append(f"**Note:** {comment}\n\n")

            output.append('</div>\n\n')

    return "".join(output)


def format_objects(objects: List[Dict[str, Any]]) -> str:
    """Format MISP objects as markdown sections."""
    if not objects:
        return ""

    output = ["\n### Objects\n"]

    for obj in objects:
        obj_name = obj.get("name", "Unknown")
        obj_meta = obj.get("meta-category", "")

        output.append(f"\n#### {obj_name}")
        if obj_meta:
            output.append(f" *({obj_meta})*")
        output.append("\n\n")

        attributes = obj.get("Attribute", [])
        if attributes:
            for attr in attributes:
                if attr.get("deleted"):
                    continue

                attr_type = attr.get("object_relation", attr.get("type", ""))
                value = attr.get("value", "")
                comment = attr.get("comment", "")

                output.append(f"- **{attr_type}**: `{value}`")
                if comment:
                    output.append(f" - {comment}")
                output.append("\n")

    return "".join(output)


def create_event_markdown(event: Dict[str, Any], events_dir: Path) -> str:
    """Create a markdown file for a single event."""
    uuid = event["uuid"]
    info = event.get("info", "Untitled Event")
    date = event.get("date", "Unknown")
    threat_level = get_threat_level_name(event.get("threat_level_id", 4))
    analysis = get_analysis_name(event.get("analysis", 0))
    tags = event.get("tags", [])
    indicators = event.get("indicators", {})
    objects = event.get("objects", [])
    orgc = event.get("orgc", {})
    org_name = orgc.get("name", "Unknown")

    # Calculate total indicators
    total_indicators = sum(len(v) for v in indicators.values())

    # Build markdown content
    md_content = [
        f"# {info}\n\n",
        f'<div class="meta-grid">\n',
        f'<div class="meta-item"><label>UUID</label><div class="value"><code>{uuid}</code></div></div>\n',
        f'<div class="meta-item"><label>Date</label><div class="value">{date}</div></div>\n',
        f'<div class="meta-item"><label>Threat Level</label><div class="value"><span class="threat-level threat-level-{event.get("threat_level_id", 4)}">{threat_level}</span></div></div>\n',
        f'<div class="meta-item"><label>Analysis</label><div class="value">{analysis}</div></div>\n',
        f'<div class="meta-item"><label>Organization</label><div class="value">{org_name}</div></div>\n',
        f'<div class="meta-item"><label>Indicators</label><div class="value">{total_indicators}</div></div>\n',
        f'</div>\n\n',
    ]

    # Add tags
    if tags:
        md_content.append("## Tags\n\n")
        md_content.append(f'<div class="tags">\n{format_tags(tags)}\n</div>\n\n')

    # Add indicators
    if total_indicators > 0:
        md_content.append("## Indicators of Compromise\n")
        md_content.append(format_indicators(indicators))

    # Add objects
    if objects:
        md_content.append(format_objects(objects))

    # Write to file
    filename = f"{uuid}.md"
    filepath = events_dir / filename

    with open(filepath, "w") as f:
        f.write("".join(md_content))

    return filename


def create_index_markdown(events: List[Dict[str, Any]], docs_dir: Path):
    """Create the main index.md file with event listings."""
    md_content = [
        "# HvS Threat Insights\n\n",
        "## MISP Threat Intelligence Feed\n\n",
        "Welcome to the HvS-Consulting MISP threat intelligence feed viewer. ",
        "Browse through threat intelligence events, indicators of compromise (IoCs), ",
        "and security analysis from our research team.\n\n",
        f"**Total Events**: {len(events)}\n\n",
        "---\n\n",
        "## Recent Events\n\n"
    ]

    # Add event cards
    for event in events:
        uuid = event["uuid"]
        info = event.get("info", "Untitled Event")
        date = event.get("date", "Unknown")
        threat_level = get_threat_level_name(event.get("threat_level_id", 4))
        tags = event.get("tags", [])
        indicators = event.get("indicators", {})
        total_indicators = sum(len(v) for v in indicators.values())

        md_content.append(f'<a href="events/{uuid}/" class="event-card-link">\n')
        md_content.append('<div class="event-card" markdown="1">\n\n')
        md_content.append(f"### {info}\n\n")

        # Meta information
        md_content.append(f'<span class="threat-level threat-level-{event.get("threat_level_id", 4)}">{threat_level}</span> ')
        md_content.append(f'<span class="tag">📅 {date}</span> ')
        md_content.append(f'<span class="tag">🔍 {total_indicators} indicators</span>\n\n')

        # Tags
        if tags:
            formatted_tags = format_tags(tags[:5])  # Show first 5 tags
            if formatted_tags:  # Only add if there are tags after filtering
                md_content.append(formatted_tags)
                if len([t for t in tags if t.get("name") != 'hvs:sharing="threat-insights"']) > 5:
                    md_content.append(f' <span class="tag">+{len(tags) - 5} more</span>')
                md_content.append("\n\n")

        md_content.append("</div>\n")
        md_content.append("</a>\n\n")

    # Write to file
    with open(docs_dir / "index.md", "w") as f:
        f.write("".join(md_content))


def build_docs():
    """Build all markdown documentation from MISP data."""
    print("Building markdown documentation from MISP data...")

    # Setup paths
    data_dir = Path("data")
    docs_dir = Path("docs")
    events_dir = docs_dir / "events"

    # Create events directory
    events_dir.mkdir(exist_ok=True)

    # Load events
    events_file = data_dir / "events_index.json"
    if not events_file.exists():
        print(f"Error: {events_file} not found. Run fetch_data.py first.")
        return

    with open(events_file) as f:
        events = json.load(f)

    print(f"Loaded {len(events)} events")

    # Create index page
    create_index_markdown(events, docs_dir)
    print("✓ Created index page")

    # Create individual event pages
    for event in events:
        create_event_markdown(event, events_dir)

    print(f"✓ Created {len(events)} event pages")
    print(f"\nDocumentation built successfully!")
    print(f"\nTo view locally, run:")
    print(f"  mkdocs serve")
    print(f"  Then open http://127.0.0.1:8000")


if __name__ == "__main__":
    build_docs()
