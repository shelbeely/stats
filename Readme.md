# GitHub Stats Template

This repository serves as a template for creating your own GitHub statistics dashboard. It includes a scheduled GitHub Action that automatically collects comprehensive GitHub stats daily, including **historical data** and **private repository contributions**.

## ✨ Features

- 📊 **Complete Historical Data**: Contribution history from account creation to present
- 🔒 **Private Repository Support**: Includes statistics from private repos (when properly configured)
- 📈 **Comprehensive Metrics**: Commits, PRs, issues, code statistics, and more
- 🤖 **Automatic Updates**: Runs daily via GitHub Actions
- 📱 **Ready-to-Use**: Template repository with pre-configured workflow

## 🚀 Quick Start

### 1. Use This Template

Click the **"Use this template"** button at the top of this repository to create your own copy.

### 2. Configure Your Personal Access Token

**Important**: To collect historical data and private repository statistics, you need a properly configured Personal Access Token.

📖 **[Read the Complete Setup Guide →](SETUP.md)**

#### Quick Token Setup (TL;DR)

1. Create a [Personal Access Token](https://github.com/settings/tokens/new) with these scopes:
   - ✅ `repo` (for private repos and historical data)
   - ✅ `read:user` (for profile data)
2. Add it as a repository secret named `ACCESS_TOKEN`

For detailed instructions, including how to ensure private repos and historical data are included, see **[SETUP.md](SETUP.md)**.

### 3. Enable Actions

1. Go to the **Actions** tab in your repository
2. Click **"I understand my workflows, go ahead and enable them"**
3. Manually trigger the workflow or wait for the scheduled run (daily at 12:00 UTC)

### 4. View Your Stats

After the action runs, check:
- `github-user-stats.json` - Raw data (includes private repo stats)
- `README.md` - Your public profile stats

## 📋 What Data is Collected?

### With Proper Token Configuration

✅ **Historical Data**
- All contributions from account creation to present
- Monthly breakdown by year
- Contribution streaks and patterns

✅ **Private Repository Data**
- Private repo count and statistics
- Contributions from private repos
- Code statistics including private repos
- Languages used across all repos

✅ **Public Repository Data**
- Public repo statistics
- Stars, forks, and views
- Top repositories

✅ **Code & Activity Metrics**
- Lines of code added/deleted
- Language breakdown
- Pull requests, issues, reviews
- And much more!

## 🔧 Customization

### Update Schedule

Edit `.github/workflows/generate-stats.yaml` to change the collection frequency:

```yaml
on:
  schedule:
    - cron: "0 12 * * *"  # Daily at 12:00 UTC
```

### Customize README

The profile README (`README.md`) is auto-generated. To customize it:
1. Modify the stats-action configuration
2. Or manually edit after generation (changes will be overwritten on next run)

## 📖 Documentation

- **[SETUP.md](SETUP.md)** - Complete setup guide for historical data and private repos
- **[Stats Action Docs](https://github.com/LukeHagar/stats-action)** - Action documentation

## 🔒 Privacy & Security

- **Private Data**: `github-user-stats.json` contains all your data (public + private)
- **Public README**: Only displays public statistics
- **Token Security**: Never commit your PAT; always use repository secrets
- **Data Control**: You control what gets displayed publicly

## 🐛 Troubleshooting

### Issue: Missing Historical Data or Private Repos

See the [Troubleshooting section in SETUP.md](SETUP.md#troubleshooting) for solutions.

Common issues:
- Token missing `repo` scope
- Token expired
- Fine-grained token not set to "All repositories"

## 📅 Workflow Schedule

- **Automatic**: Daily at 12:00 UTC
- **Manual**: Trigger anytime from the Actions tab

## 🤝 Contributing

This template uses the [LukeHagar/stats-action](https://github.com/LukeHagar/stats-action). For issues or feature requests related to data collection, please open an issue on that repository.

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---

**Remember**: Keep your PAT safe and never share it with anyone. It's like a password for your GitHub account!
