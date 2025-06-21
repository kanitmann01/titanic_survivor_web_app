# 🚀 GitHub Repository Setup Guide

This guide will help you set up your GitHub repository and update all the links in your Titanic Survival Predictor.

## 📝 Step 1: Create Your GitHub Repository

1. **Go to GitHub:**
   - Visit [https://github.com/new](https://github.com/new)
   - Sign in to your GitHub account

2. **Create Repository:**
   - **Repository name:** `titanic_survivor_web_app`
   - **Description:** `🚢 Titanic Survival Predictor - Interactive web app using Random Forest ML. Kaggle Score: 0.77751`
   - **Visibility:** Public (recommended for showcasing)
   - **Don't initialize** with README, .gitignore, or license (we already have these files)

3. **Create Repository**

## 🔗 Step 2: Update GitHub Links

Once you have your repository created, you need to replace `kanitmann01` with your actual GitHub username in these files:

### Files to Update:
- `templates/base.html` (2 places)
- `templates/result.html` (1 place)  
- `README.md` (3 places)

### Replace This:
```
kanitmann01/titanic_survivor_web_app
```

### With This:
```
your-actual-username/titanic_survivor_web_app
```

## ⚡ Step 3: Quick Find & Replace

Run this command in your project directory (replace `your-username` with your actual GitHub username):

```bash
# Replace kanitmann01 with your actual GitHub username
find . -name "*.html" -o -name "*.md" -exec sed -i 's/kanitmann01/your-username/g' {} +
```

**Or manually update each file:**

1. **templates/base.html:**
   - Line with GitHub star button
   
2. **templates/result.html:**
   - Line with GitHub star button
   
3. **README.md:**
   - GitHub star badge links (2 places)
   - View on GitHub link (1 place)

## 📤 Step 4: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "🚢 Initial commit: Titanic Survival Predictor

- Interactive Flask web app with Random Forest ML model
- Achieved 0.77751 score on Kaggle leaderboard  
- Beautiful UI with Bootstrap and Chart.js
- Ready for deployment to Railway, Render, etc.
- Complete documentation and deployment guides"

# Add remote (replace kanitmann01 with your actual username)
git remote add origin https://github.com/kanitmann01/titanic_survivor_web_app.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## 🎯 Step 5: Verify Setup

After pushing to GitHub:

1. **Check your repository:** `https://github.com/kanitmann01/titanic_survivor_web_app`
2. **Verify star button works** in your deployed app
3. **Test GitHub links** in README badges

## 🌟 Step 6: Add Repository Topics

In your GitHub repository:
1. Click the ⚙️ gear icon next to "About"
2. Add these topics:
   ```
   titanic machine-learning flask python data-science
   random-forest kaggle web-app bootstrap prediction
   ```

## 📊 Step 7: Enable GitHub Pages (Optional)

If you want to showcase your project:
1. Go to Settings → Pages
2. Choose source: "Deploy from a branch"
3. Select "main" branch
4. Your README will be visible at: `https://kanitmann01.github.io/titanic_survivor_web_app`

## ✅ Checklist

- [ ] Created GitHub repository
- [ ] Replaced all `kanitmann01` with actual username
- [ ] Pushed code to GitHub
- [ ] Verified star button works
- [ ] Added repository topics
- [ ] (Optional) Enabled GitHub Pages

---

**🎉 Your Titanic Survival Predictor is now properly configured with GitHub integration!**