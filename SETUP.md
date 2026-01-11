# GitHub Setup Guide

This guide will help you publish this project to GitHub.

## Prerequisites

1. **GitHub Account**: Create one at [github.com](https://github.com) if you don't have one
2. **Git Installed**: Download from [git-scm.com](https://git-scm.com/)

## Step 1: Initialize Git Repository

Open PowerShell in your project folder and run:

```powershell
git init
git add .
git commit -m "Initial commit: AI image generation tool"
```

## Step 2: Create GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `ai-image-generation-tool` (or your preferred name)
3. Description: "AI-powered image generation tool using Stable Diffusion"
4. Choose **Public** (so anyone can use it)
5. **Do NOT** initialize with README (we already have one)
6. Click "Create repository"

## Step 3: Connect and Push to GitHub

After creating the repository, GitHub will show you commands. Run these in PowerShell:

```powershell
# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR-USERNAME/ai-image-generation-tool.git

# Push your code
git branch -M main
git push -u origin main
```

Replace `YOUR-USERNAME` with your actual GitHub username.

## Step 4: Verify Upload

1. Go to your repository on GitHub
2. You should see all files including README.md
3. The README will automatically display on your repository page

## Step 5: (Optional) Add Topics/Tags

On your GitHub repository page:
1. Click the gear icon next to "About"
2. Add topics: `stable-diffusion`, `ai`, `image-generation`, `python`, `pytorch`, `machine-learning`
3. Save changes

## Authentication Options

### Option A: HTTPS with Personal Access Token (Recommended)

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (full control)
4. Generate and copy the token
5. Use this token as your password when pushing

### Option B: SSH (More Secure)

```powershell
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy public key
Get-Content ~/.ssh/id_ed25519.pub | clip

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
```

Then use SSH URL instead:
```powershell
git remote set-url origin git@github.com:YOUR-USERNAME/ai-image-generation-tool.git
```

## Common Git Commands

```powershell
# Check status
git status

# Add specific files
git add filename.py

# Add all changes
git add .

# Commit changes
git commit -m "Description of changes"

# Push to GitHub
git push

# Pull latest changes
git pull

# View commit history
git log
```

## Making Updates

After making changes to your code:

```powershell
git add .
git commit -m "Description of what you changed"
git push
```

## Creating a Good Repository

### Add a Banner/Logo
Create a banner image and add it to the top of README.md:
```markdown
![Banner](assets/banner.png)
```

### Add Example Images
Create an `examples/` folder with sample outputs:
```markdown
## Examples
![Example 1](examples/example1.png)
```

### Add Shields/Badges
Add status badges to your README:
```markdown
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
```

## Enabling GitHub Pages (Optional)

If you want a website for your project:
1. Go to repository Settings → Pages
2. Source: Deploy from branch
3. Branch: main, folder: / (root)
4. Save

## Troubleshooting

### "Permission denied" error
- Check authentication method (token/SSH)
- Verify token has correct permissions

### "Remote origin already exists"
```powershell
git remote remove origin
git remote add origin YOUR-URL
```

### "Failed to push some refs"
```powershell
git pull --rebase origin main
git push
```

## Resources

- [GitHub Guides](https://guides.github.com/)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub CLI](https://cli.github.com/) - Alternative command-line tool

---

Need help? Open an issue or check GitHub's documentation!
