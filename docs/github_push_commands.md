# GitHub Push Commands

## 1. Unzip and enter the project folder

```bash
cd path/to/agentic_sionna_link_adaptation
```

## 2. Initialize Git

```bash
git init
git add .
git commit -m "Initial commit: Agentic Sionna Link Adaptation Mini-Lab"
```

## 3. Create a new empty repo on GitHub

Suggested name:

```text
agentic-sionna-link-adaptation
```

Do not initialize it with a README because this package already includes one.

## 4. Connect and push

Replace `YOUR_USERNAME` with your GitHub username.

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/agentic-sionna-link-adaptation.git
git push -u origin main
```

## If remote already exists

```bash
git remote -v
git remote set-url origin https://github.com/YOUR_USERNAME/agentic-sionna-link-adaptation.git
git push -u origin main
```
