# GitHub Stats Setup Guide

This guide explains how to configure your Personal Access Token (PAT) to ensure comprehensive data collection, including **historical data** and **private repository statistics**.

## Why a Personal Access Token is Required

The GitHub Action uses the `LukeHagar/stats-action` which requires a Personal Access Token (PAT) instead of the default `GITHUB_TOKEN` because:

1. **Historical Data**: The GitHub contribution calendar and historical statistics require authentication as the actual user
2. **Private Repositories**: Access to private repository data requires explicit permissions
3. **Repository Views**: View counts require push access across repositories
4. **Viewer Query**: The GraphQL `viewer` query returns data for the token owner

## Required Token Scopes

Your PAT must have the following scopes to collect **all historical data including private repos**:

| Scope | Purpose | Impact on Data Collection |
|-------|---------|---------------------------|
| `read:user` | Access user profile data | ✅ Profile info, followers, following |
| `repo` | **Full repository access** | ✅ Public repos<br>✅ **Private repos**<br>✅ Repository views<br>✅ **Historical contributions from private repos** |

### Important Notes About Private Repositories

- **Without `repo` scope**: Only public repository contributions are counted
- **With `repo` scope**: All contributions (public + private) are included in historical data
- The action will include private repos in statistics but marks them as `isPrivate: true` in the JSON output
- Private repo data in the JSON is only accessible to you and won't be exposed in public READMEs unless you explicitly include it

## Setting Up Your Personal Access Token

### Option 1: Fine-Grained Personal Access Token (Recommended)

Fine-grained tokens provide more granular control and better security.

1. Go to [GitHub Settings → Developer settings → Personal access tokens → Fine-grained tokens](https://github.com/settings/tokens?type=beta)
2. Click **"Generate new token"**
3. Configure the token:
   - **Token name**: `GitHub Stats Action`
   - **Expiration**: Choose based on your security preferences (90 days recommended)
   - **Repository access**: Select **"All repositories"** to include private repos
   - **Permissions**:
     - Repository permissions:
       - **Contents**: Read (to access repository data)
       - **Metadata**: Read (automatic, for basic repo info)
     - Account permissions:
       - **Starring**: Read (for stars given/received)
4. Click **"Generate token"**
5. **Copy the token immediately** (you won't be able to see it again)

### Option 2: Classic Personal Access Token

Classic tokens are simpler but provide broader access.

1. Go to [GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)](https://github.com/settings/tokens)
2. Click **"Generate new token (classic)"**
3. Configure the token:
   - **Note**: `GitHub Stats Action`
   - **Expiration**: Choose based on your security preferences
   - **Select scopes**:
     - ✅ `repo` (Full control of private repositories)
       - This automatically includes all sub-scopes needed for private repos
     - ✅ `read:user` (Read ALL user profile data)
4. Click **"Generate token"**
5. **Copy the token immediately** (you won't be able to see it again)

## Adding the Token to Your Repository

1. Go to your repository settings
2. Navigate to **"Secrets and variables"** → **"Actions"**
3. Click **"New repository secret"**
4. Configure the secret:
   - **Name**: `ACCESS_TOKEN` (this must match the workflow file)
   - **Value**: Paste your PAT
5. Click **"Add secret"**

## Verifying Your Setup

### Check Token Permissions

To verify your token has the right permissions:

1. Go to the **Actions** tab in your repository
2. Manually trigger the workflow using **"Run workflow"**
3. Check the workflow run results
4. Review the generated `github-user-stats.json` file:
   - Look for `privateRepos` count > 0 (if you have private repos)
   - Check `contributionStats.monthlyBreakdown` for historical data going back to your account creation

### What Gets Collected

With the correct token permissions, the action collects:

#### Historical Data (All Years)
- ✅ Contribution counts by year, month, and day
- ✅ Contribution streaks (current and longest)
- ✅ Monthly breakdown from account creation to present
- ✅ Most active day and productivity patterns

#### Private Repository Data
- ✅ Private repo count and statistics
- ✅ Contributions from private repos included in totals
- ✅ Code statistics from private repos
- ✅ Languages used in private repos

#### Public Repository Data
- ✅ Public repo statistics and stars
- ✅ Fork counts
- ✅ Repository views (last 14 days)
- ✅ Top repositories by stars

#### Code Statistics
- ✅ Total lines of code added/deleted
- ✅ Language breakdown with percentages
- ✅ Code size in bytes

## Troubleshooting

### Issue: Missing Historical Data

**Symptom**: `monthlyBreakdown` only shows recent months

**Solution**:
1. Check that your token has `read:user` scope
2. Verify the action is running successfully (check Actions tab)
3. Look for rate limit errors in the action logs

### Issue: Private Repos Not Included

**Symptom**: `privateRepos: 0` but you have private repositories

**Solution**:
1. Verify your token has `repo` scope (not just `public_repo`)
2. For fine-grained tokens, ensure "All repositories" is selected
3. Regenerate the token if needed and update the secret

### Issue: Token Expired

**Symptom**: Workflow fails with authentication error

**Solution**:
1. Generate a new token following the steps above
2. Update the `ACCESS_TOKEN` secret in repository settings
3. Re-run the workflow

### Issue: Rate Limit Errors

**Symptom**: Action fails with rate limit exceeded

**Solution**:
- The action automatically handles rate limits with exponential backoff
- If you have many repositories, the action may take longer but should complete
- Consider running less frequently if hitting limits (e.g., weekly instead of daily)

## Security Best Practices

1. **Use Fine-Grained Tokens**: Provides better security with specific repository access
2. **Set Expiration**: Tokens should expire and be rotated regularly
3. **Minimal Permissions**: Only grant the required scopes (`read:user` and `repo`)
4. **Keep Tokens Secret**: Never commit tokens to your repository
5. **Monitor Usage**: Review the Actions logs periodically
6. **Rotate Tokens**: Update tokens before they expire

## What's Collected and What's Public

### Collected in JSON (Private to You)
- All repository data (public + private)
- Private repository names and statistics
- Complete contribution history
- Repository views

### Displayed in Public README
- Only public repository statistics
- Aggregated contribution numbers
- Public language statistics
- Non-sensitive profile information

The `github-user-stats.json` file contains all data, but the README.md only displays public information. You control what gets displayed by editing the README template.

## Showcasing Private Repository Work

While the stats action collects data from all your repositories (public + private), the automated README only displays the top 10 repositories by stars. If you want to highlight specific private projects:

### Option 1: Automated Private Repository Info (Recommended)

This repository includes a Python script that automatically fetches information about specific private repositories using the GitHub API during the workflow run.

**To add a private repository:**

1. Edit `scripts/fetch-private-repo-info.py`
2. Add your repository to the `REPOS_TO_FETCH` list:
   ```python
   REPOS_TO_FETCH = [
       {"owner": "your-username", "name": "your-repo-name"},
   ]
   ```
3. Commit and push the changes
4. The workflow will automatically fetch repository details (name, description, language, creation date) and update the README

**Benefits:**
- Automatically pulls real repository data (description, language, creation date)
- Updates on every workflow run
- Only exposes non-sensitive metadata (no code or commit details)
- Works with both personal and forked repositories

**What gets displayed:**
- Repository name and description
- Primary programming language
- Creation date
- Private/Fork status
- Active development indicator

### Option 2: Manual Section (For Custom Descriptions)

Add a dedicated section to your README.md to describe private work without exposing sensitive details:

```markdown
## 🔒 Featured Private Projects

### my-private-project
**Private Repository** | **Active Development**

Description of the project focus and technologies used, without exposing confidential information.
```

**Benefits:**
- Full control over what information is shared
- Can highlight specific projects regardless of star count
- Maintains confidentiality while showing active work

### Option 3: Understanding the Data

The `topRepos` array in `github-user-stats.json` includes both public and private repositories, sorted by stars. Private repos are marked with `"isPrivate": true`. You can:

1. Review the `github-user-stats.json` file (not committed to public repos by default)
2. See which private repos have the most activity
3. Manually add descriptions of those projects to your README

**Important:** Be cautious about exposing private repository names or details in your public README. The aggregate statistics (contribution counts, language usage, etc.) already include your private repository activity.

## Support

If you encounter issues:

1. Go to the **Actions** tab in your repository and check the workflow runs for error messages
2. Review the [stats-action documentation](https://github.com/LukeHagar/stats-action)
3. Verify your token scopes match the requirements above
4. Ensure your token hasn't expired

## Schedule

The workflow runs:
- **Automatically**: Daily at 12:00 UTC
- **Manually**: Click "Run workflow" in the Actions tab

Historical data is collected on every run, so your statistics are always up-to-date with your complete GitHub history.
