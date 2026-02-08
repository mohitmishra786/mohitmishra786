# AGENTS.md

This is a GitHub profile repository (`mohitmishra786/mohitmishra786`) containing an automated README with dynamic content.

## Repository Overview

- **Type**: GitHub Profile README with automated workflows
- **Main Files**: `README.md`, workflow files in `.github/workflows/`
- **Assets**: SVG visualizations stored in `assets/`

## Automated Workflows

All workflows are triggered on schedule, push to main/master, or manually via `workflow_dispatch`:

### 1. LOC Statistics (`.github/workflows/loc-stats.yml`)
- **Schedule**: Daily at midnight UTC (`0 0 * * *`)
- **Purpose**: Counts lines of code across all user repositories
- **Outputs**: Updates `README.md` with badge and detailed stats in `loc_results/`
- **Manual trigger**: `gh workflow run loc-stats.yml`

### 2. Blog Posts (`.github/workflows/blog-post-workflow.yml`)
- **Schedule**: Daily at midnight UTC
- **Purpose**: Fetches latest blog posts from Medium and TheCoreDump RSS feeds
- **Updates**: README.md section between `<!-- BLOG-POST-LIST:START -->` and `<!-- BLOG-POST-LIST:END -->`

### 3. 3D Contribution Graph (`.github/workflows/profile-3d.yml`)
- **Schedule**: Daily at 18:00 UTC
- **Purpose**: Generates 3D contribution visualization
- **Outputs**: `assets/profile-3d-contrib/*.svg`

### 4. Snake Animation (`.github/workflows/snake.yml`)
- **Schedule**: Every 12 hours
- **Purpose**: Generates contribution grid snake animation
- **Outputs**: `assets/github-snake.svg`, `assets/github-snake-dark.svg`

## Development Commands

Since this is a profile repository without traditional build/test cycles:

```bash
# Validate workflow files
gh workflow list

# Run a specific workflow manually
gh workflow run <workflow-file>

# View workflow status
gh run list

# Install dependencies locally (for Python scripts)
pip install -r requirements.txt  # Contains: feedparser
```

## Code Style Guidelines

### Markdown (README.md)
- Use HTML comments as markers: `<!-- MARKER-START -->` / `<!-- MARKER-END -->`
- Maintain centered div containers for visual elements
- Use Shields.io badges for stats: `https://img.shields.io/badge/...`
- Keep profile badges consistent with for-the-badge style

### YAML (Workflows)
- Use 2-space indentation
- Quote cron expressions
- Include `workflow_dispatch` for manual triggers
- Set appropriate timeouts (default 10 min for snake workflow)
- Use `actions/checkout@v4` consistently

### Git Conventions
- Commit messages: Use present tense, descriptive
- Automated commits use: `github-actions[bot]` or `github-actions`
- Always rebase before push: `git pull origin main --rebase --autostash`

### File Organization
```
├── README.md                 # Main profile content
├── requirements.txt          # Python dependencies
├── assets/                   # Generated visualizations
│   ├── github-snake.svg
│   ├── github-snake-dark.svg
│   ├── github-user-stats.svg
│   └── profile-3d-contrib/
├── loc_results/             # LOC statistics output
│   ├── stats.json
│   ├── summary.md
│   ├── detailed_results.csv
│   ├── language_summary.csv
│   └── repo_summary.csv
└── .github/workflows/       # Automation workflows
```

## Security

- Use `secrets.GH_PAT` for private repository access
- Use `secrets.GITHUB_TOKEN` for public operations
- Grant minimal permissions (`contents: write`)
- Never hardcode tokens in workflow files

## External API Status (Verified 2026-02-08)

### Working APIs (200 OK)
- `readme-typing-svg.herokuapp.com` - Typing animation
- `skillicons.dev` - Tech stack icons
- `capsule-render.vercel.app` - Header/footer animations
- `github-profile-summary-cards.vercel.app` - Stats cards
- `github-readme-activity-graph.vercel.app` - Activity graph
- `github-readme-streak-stats.herokuapp.com` - Streak stats
- `komarev.com/ghpvc` - Profile view counter
- `visitor-badge.laobi.icu` - Visitor badge
- `hits.sh` - Hit counter
- `shields.io` - All shields badges

### Broken/Unavailable APIs (503/Deprecated)
- `github-profile-trophy.vercel.app` - DEPLOYMENT_PAUSED (removed from README)
- `github-readme-stats.vercel.app` - DEPLOYMENT_PAUSED (avoid using)

## Maintenance Notes

- Workflows auto-commit changes; manual edits to generated sections will be overwritten
- RSS feeds must remain accessible for blog post updates
- LOC stats require GitHub API access via PAT with repo scope
- Profile view badges update dynamically via external services
- Test APIs with `curl -sI <url>` before adding new visualizations

## RSS Feeds

Current blog sources:
- `https://medium.com/feed/@mohitmishra786687`
- `https://mohitmishra786.github.io/TheCoreDump/feed.xml`

## Dependencies

- `feedparser`: For RSS feed parsing in local scripts
- `cloc`: For line counting (installed in workflows via apt)
- `jq`: For JSON processing in workflows
