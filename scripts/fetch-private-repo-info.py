#!/usr/bin/env python3
"""
Fetch information about specific private repositories and update README.
This script is run during the GitHub Actions workflow with ACCESS_TOKEN.
"""

import os
import sys
import json
import requests
from datetime import datetime

# Repository to fetch
REPOS_TO_FETCH = [
    {"owner": "shelbeely", "name": "prj-illuminate"},
]

def fetch_repo_info(owner, repo_name, token):
    """Fetch repository information from GitHub API."""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    url = f"https://api.github.com/repos/{owner}/{repo_name}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 404:
        print(f"Repository {owner}/{repo_name} not found or no access", file=sys.stderr)
        return None
    
    response.raise_for_status()
    return response.json()

def fetch_repo_languages(owner, repo_name, token):
    """Fetch repository languages from GitHub API."""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    url = f"https://api.github.com/repos/{owner}/{repo_name}/languages"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 404:
        return {}
    
    response.raise_for_status()
    return response.json()

def get_primary_language(languages):
    """Get the primary language from languages dict."""
    if not languages:
        return "Not specified"
    
    # Find language with most bytes
    primary = max(languages.items(), key=lambda x: x[1])
    return primary[0]

def format_repo_section(repo_info, languages):
    """Format repository information for README."""
    name = repo_info.get("name", "Unknown")
    description = repo_info.get("description") or "A private project under active development"
    primary_language = get_primary_language(languages)
    is_private = repo_info.get("private", False)
    is_fork = repo_info.get("fork", False)
    created_at = repo_info.get("created_at", "")
    updated_at = repo_info.get("updated_at", "")
    
    # Format created date
    created_year = ""
    if created_at:
        try:
            created_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
            created_year = created_date.strftime("%B %Y")
        except:
            pass
    
    # Determine status
    status = "Active Development"
    repo_type = "Private Repository"
    if is_fork:
        repo_type += " (Fork)"
    
    # Build the section
    section = f"""### {name}
**{repo_type}** | **{status}**

{description}

- **Primary Language:** {primary_language}
- **Status:** {status}"""
    
    if created_year:
        section += f"\n- **Created:** {created_year}"
    
    section += f"""

**Contributions:** Part of my **18 private repositories** containing production code, experimental features, and client work. These private repos contribute to the overall statistics shown above, including code metrics and contribution counts.

> 💡 **Note:** Detailed information about private repositories is not publicly displayed to maintain confidentiality. The aggregate statistics include contributions from all repositories (public + private)."""
    
    return section

def update_readme(repo_sections):
    """Update README.md with repository information."""
    readme_path = "README.md"
    
    with open(readme_path, 'r') as f:
        content = f.read()
    
    # Find the Featured Private Projects section
    start_marker = "## 🔒 Featured Private Projects"
    end_marker = "\n---\n\n## 📈 This Year's Highlights"
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx == -1 or end_idx == -1:
        print("Could not find the Featured Private Projects section in README", file=sys.stderr)
        return False
    
    # Build new section content
    new_section = f"""{start_marker}

Working on private repositories that showcase specialized development work:

{repo_sections}

"""
    
    # Replace the section
    new_content = content[:start_idx] + new_section + content[end_idx:]
    
    with open(readme_path, 'w') as f:
        f.write(new_content)
    
    return True

def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN environment variable not set", file=sys.stderr)
        sys.exit(1)
    
    repo_sections = []
    
    for repo in REPOS_TO_FETCH:
        owner = repo["owner"]
        name = repo["name"]
        
        print(f"Fetching info for {owner}/{name}...")
        
        try:
            repo_info = fetch_repo_info(owner, name, token)
            if repo_info:
                languages = fetch_repo_languages(owner, name, token)
                section = format_repo_section(repo_info, languages)
                repo_sections.append(section)
                print(f"Successfully fetched info for {owner}/{name}")
            else:
                print(f"Skipping {owner}/{name} - not accessible")
        except Exception as e:
            print(f"Error fetching {owner}/{name}: {e}", file=sys.stderr)
            continue
    
    if not repo_sections:
        print("No repository information fetched", file=sys.stderr)
        sys.exit(0)  # Don't fail the workflow, just skip
    
    # Join all sections
    all_sections = "\n\n".join(repo_sections)
    
    # Update README
    if update_readme(all_sections):
        print("README updated successfully")
    else:
        print("Failed to update README", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
