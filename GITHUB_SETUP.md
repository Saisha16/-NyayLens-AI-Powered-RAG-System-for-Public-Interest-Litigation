# 🚀 GitHub Setup Guide for NyayLens

## ✅ Files Created for Security

1. **`.gitignore`** - Prevents sensitive files from being committed
2. **`.env.example`** - Template for environment variables (safe to commit)
3. **`LICENSE`** - MIT License (allows others to use your code)
4. **`SECURITY.md`** - Security guidelines and policies

## 🔒 What's Been Hidden (Protected)

Your **`.env`** file is now in `.gitignore` and will NOT be uploaded to GitHub. This protects:
- ✅ Your OpenAI API key
- ✅ JWT secret key
- ✅ Database credentials
- ✅ Any other sensitive configuration

## 📝 What is MIT License?

**MIT License** is:
- ✅ **Free & Open**: Anyone can use, modify, and distribute your code
- ✅ **Permissive**: Very few restrictions
- ✅ **No Warranty**: You're not liable if something breaks
- ✅ **Popular**: Used by React, Node.js, jQuery, etc.

**Is it required?** No, but **highly recommended** because:
- It protects you legally
- Tells others how they can use your code
- Makes your project more professional
- Increases trust and adoption

**Alternatives:**
- **Apache 2.0**: Like MIT but with patent protection
- **GPL**: Users must open-source their modifications
- **No License**: Nobody can legally use your code (not recommended)

## 🎯 Steps to Push to GitHub

### 1. Initialize Git (if not already done)
```bash
git init
```

### 2. Add all files (safe now with .gitignore)
```bash
git add .
```

### 3. Commit your code
```bash
git commit -m "Initial commit: NyayLens AI-Powered RAG System for PIL"
```

### 4. Create GitHub repository
- Go to https://github.com/new
- Name: `nyaylens` or `nyaylens-rag-pil`
- Description: "AI-Powered RAG System for Public Interest Litigation using Indian Law"
- Make it **Public** (to share) or **Private** (to keep secret)
- **Don't** initialize with README (you already have one)

### 5. Connect to GitHub
```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/nyaylens.git
git branch -M main
git push -u origin main
```

## ⚠️ Important: Before Pushing

### Check what will be uploaded:
```bash
git status
```

**Make sure you DON'T see:**
- ❌ `.env` file
- ❌ `*.log` files in `logs/` folder
- ❌ `__pycache__/` folders
- ❌ Any `.db` files

**You SHOULD see:**
- ✅ `.env.example` (safe template)
- ✅ `LICENSE`
- ✅ `README.md`
- ✅ All `.py` files
- ✅ `requirements.txt`

### Test your .gitignore:
```bash
# This should show .env is ignored
git check-ignore .env
```

## 🔐 Security Checklist

Before pushing:
- [ ] `.env` file is in `.gitignore`
- [ ] Real API keys are only in `.env` (not `.env.example`)
- [ ] Logs folder is ignored
- [ ] Database files are ignored
- [ ] No hardcoded secrets in code files
- [ ] `.env.example` has placeholder values only

## 🎨 Recommended Repository Settings

After creating the repo on GitHub:

1. **Add Topics** (helps discoverability):
   - `rag`
   - `legal-tech`
   - `ai`
   - `india`
   - `pil`
   - `legal-documents`
   - `fastapi`
   - `nlp`

2. **Add Description**:
   > "NyayLens: AI-powered RAG system for generating Public Interest Litigation drafts using Indian Constitutional Law, BNS, and legal precedents"

3. **Enable Issues** (for bug reports and feature requests)

4. **Add README badges** (optional but professional):
   ```markdown
   ![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
   ![License](https://img.shields.io/badge/license-MIT-green.svg)
   ![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-teal.svg)
   ```

## 📱 For Collaborators

When someone clones your project, they should:

1. Clone the repository
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Fill in their own API keys in `.env`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the application

## 🆘 If You Accidentally Committed Secrets

If you already committed `.env` with real secrets:

1. **Revoke/Rotate** the exposed API keys immediately
2. Remove from Git history:
   ```bash
   git filter-branch --force --index-filter \
   "git rm --cached --ignore-unmatch .env" \
   --prune-empty --tag-name-filter cat -- --all
   ```
3. Force push:
   ```bash
   git push origin --force --all
   ```

## ✨ Next Steps

After pushing to GitHub:
1. Add a `CONTRIBUTING.md` file for contributors
2. Create a `docs/` folder for documentation
3. Set up GitHub Actions for CI/CD (optional)
4. Add a demo video or screenshots to README
5. Share on social media/LinkedIn!

---

**Need Help?** Check:
- GitHub Docs: https://docs.github.com
- Git Basics: https://git-scm.com/book/en/v2
- MIT License: https://choosealicense.com/licenses/mit/
