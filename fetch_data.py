#!/usr/bin/env python3
"""
Fetch MISP threat intelligence data from the feed and prepare it for MkDocs.
"""
import json
import requests
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


FEED_BASE_URL = "https://misp.ir.hvs-consulting.de/feed/threat-insights/"


def fetch_manifest() -> Dict[str, Any]:
    """Fetch the manifest.json from the MISP feed."""
    url = f"{FEED_BASE_URL}manifest.json"
    print(f"Fetching manifest from {url}")
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def fetch_event(uuid: str) -> Dict[str, Any]:
    """Fetch a single event JSON by UUID."""
    url = f"{FEED_BASE_URL}{uuid}.json"
    print(f"Fetching event {uuid}")
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def enrich_event_data(uuid: str, manifest_entry: Dict[str, Any], event_data: Dict[str, Any]) -> Dict[str, Any]:
    """Combine manifest metadata with full event data."""
    event = event_data.get("Event", {})

    # Extract attributes for searching
    attributes = event.get("Attribute", [])

    # Categorize attributes
    indicators = {
        "urls": [],
        "domains": [],
        "ips": [],
        "hashes": [],
        "emails": [],
        "other": []
    }

    for attr in attributes:
        if attr.get("deleted"):
            continue

        attr_type = attr.get("type", "")
        value = attr.get("value", "")

        if attr_type in ["url", "uri"]:
            indicators["urls"].append(attr)
        elif attr_type in ["domain", "hostname"]:
            indicators["domains"].append(attr)
        elif attr_type in ["ip-src", "ip-dst", "ip"]:
            indicators["ips"].append(attr)
        elif "hash" in attr_type.lower() or attr_type in ["md5", "sha1", "sha256"]:
            indicators["hashes"].append(attr)
        elif "email" in attr_type:
            indicators["emails"].append(attr)
        else:
            indicators["other"].append(attr)

    # Extract objects
    objects = event.get("Object", [])

    return {
        "uuid": uuid,
        "info": manifest_entry.get("info"),
        "date": manifest_entry.get("date"),
        "timestamp": manifest_entry.get("timestamp"),
        "analysis": manifest_entry.get("analysis"),
        "threat_level_id": manifest_entry.get("threat_level_id"),
        "tags": manifest_entry.get("Tag", []),
        "orgc": manifest_entry.get("Orgc", {}),
        "indicators": indicators,
        "objects": objects,
        "attribute_count": len(attributes),
        "full_event": event
    }


def main():
    """Main execution function."""
    # Create data directory
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    # Fetch manifest
    manifest = fetch_manifest()

    # Save manifest
    with open(data_dir / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nFound {len(manifest)} events in manifest")

    # Fetch all events
    enriched_events = []

    for uuid, manifest_entry in manifest.items():
        try:
            event_data = fetch_event(uuid)
            enriched = enrich_event_data(uuid, manifest_entry, event_data)
            enriched_events.append(enriched)

            # Save individual event
            with open(data_dir / f"{uuid}.json", "w") as f:
                json.dump(enriched, f, indent=2)

        except Exception as e:
            print(f"Error fetching event {uuid}: {e}")

    # Sort by date (newest first)
    enriched_events.sort(key=lambda x: x["date"], reverse=True)

    # Create index with all events
    with open(data_dir / "events_index.json", "w") as f:
        json.dump(enriched_events, f, indent=2)

    print(f"\nSuccessfully fetched {len(enriched_events)} events")
    print(f"Data saved to {data_dir.absolute()}")


if __name__ == "__main__":
    main()
