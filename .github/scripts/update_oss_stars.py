#!/usr/bin/env python3
import json
import os
import re
import sys
import urllib.request


REPOSITORIES = (
    "ueberdosis/tiptap",
    "matomo-org/matomo",
    "SimonZeng7108/efficientsam3",
    "liebe-magi/pyzaim",
)


def fetch_star_counts(token):
    counts = {}
    for repository in REPOSITORIES:
        request = urllib.request.Request(
            f"https://api.github.com/repos/{repository}",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {token}",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        with urllib.request.urlopen(request) as response:
            counts[repository] = json.load(response)["stargazers_count"]
    return counts


def update_readme(readme, counts):
    lines = []
    for line in readme.splitlines(keepends=True):
        updated = line
        for repository, stars in counts.items():
            if f"https://github.com/{repository})" in line:
                cells = line.rstrip("\n").split("|")
                cells[2] = f" {stars:,} "
                updated = "|".join(cells) + ("\n" if line.endswith("\n") else "")
                break
        lines.append(updated)
    return "".join(lines)


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN is required")

    readme_path = os.environ.get("README_PATH", "README.md")
    with open(readme_path, encoding="utf-8") as readme_file:
        readme = readme_file.read()
    updated = update_readme(readme, fetch_star_counts(token))
    if updated != readme:
        with open(readme_path, "w", encoding="utf-8") as readme_file:
            readme_file.write(updated)


if __name__ == "__main__":
    main()
