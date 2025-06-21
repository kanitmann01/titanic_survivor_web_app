# 🚢 Titanic Survival Predictor Web App

A fun and interactive web application that predicts whether you would have survived the Titanic disaster based on your passenger profile. Built with Flask and machine learning using your optimized Random Forest model.

## 🏆 Kaggle Competition Results

**Score: 0.74401** on the Kaggle leaderboard - using Random Forest Classification

[![Star on GitHub](https://img.shields.io/github/stars/YOUR_USERNAME/titanic-survival-predictor?style=social)](https://github.com/YOUR_USERNAME/titanic-survival-predictor)

## ✨ Features

- **Interactive Form**: Easy-to-use form to input passenger details
- **Real-time Predictions**: Get instant survival predictions with probability scores
- **Beautiful UI**: Modern, responsive design with Bootstrap and custom CSS
- **Historical Context**: Learn about survival patterns from the actual Titanic data
- **Probability Visualization**: Interactive charts showing survival chances
- **Mobile Friendly**: Works perfectly on all devices

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Quick Start

1. **Clone or navigate to the project directory**
   ```bash
   cd /path/to/your/titanic-project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## 🎯 How to Use

1. **Fill in your passenger details:**
   - Choose your passenger class (1st, 2nd, or 3rd)
   - Select your gender
   - Enter your age
   - Input the ticket fare you would have paid
   - Specify number of siblings/spouse aboard
   - Specify number of parents/children aboard
   - Choose your port of embarkation

2. **Get your prediction:**
   - Click "Predict My Fate!" 
   - See your survival probability with detailed breakdown
   - Learn about historical survival patterns

3. **Try different scenarios:**
   - Experiment with different passenger profiles
   - See how class, gender, age, and family size affected survival

## 🧠 Machine Learning Model

The app uses a **Random Forest Classifier** with optimized hyperparameters:
- **Algorithm**: Random Forest with Gini criterion
- **N Estimators**: 100 trees
- **Max Depth**: 5 levels
- **Min Samples Split**: 3
- **Kaggle Score**: 0.77751 (solid performance)

### Features Used:
- Passenger Class (Pclass)
- Age
- Gender (Sex)
- Number of siblings/spouses aboard (SibSp)
- Number of parents/children aboard (Parch)
- Ticket fare (Fare)
- Port of embarkation (Embarked)

## 📊 Historical Insights

The model reveals fascinating patterns from the Titanic disaster:

- **Women & Children First**: 74% of women survived vs 19% of men
- **Class Disparity**: 1st class (63%), 2nd class (47%), 3rd class (24%)
- **Family Size**: Small families had better survival rates
- **Age Factor**: Children had higher survival rates than adults

## 🎨 Technical Details

### Backend:
- **Flask**: Python web framework
- **Pandas**: Data manipulation and analysis
- **Scikit-learn**: Machine learning model
- **NumPy**: Numerical computing

### Frontend:
- **Bootstrap 5**: Modern CSS framework
- **Chart.js**: Interactive probability charts
- **Font Awesome**: Beautiful icons
- **Custom CSS**: Gradient backgrounds and animations

### File Structure:
```
📁 titanic-survival-app/
├── 📄 app.py                 # Main Flask application
├── 📄 requirements.txt       # Python dependencies
├── 📄 README.md             # This file
├── 📁 templates/            # HTML templates
│   ├── 📄 base.html         # Base template with styling
│   ├── 📄 index.html        # Main form page
│   ├── 📄 result.html       # Results display page
│   └── 📄 error.html        # Error handling page
├── 📁 titanic/              # Original dataset
│   ├── 📄 train.csv         # Training data
│   ├── 📄 test.csv          # Test data
│   └── 📄 gender_submission.csv
└── 📄 data-cleaning.ipynb   # Original model development
```

## 🚀 Deployment Options

### Local Development:
```bash
python app.py
# Access at http://localhost:5000
```

### Free Cloud Deployment:
Your app is **ready for deployment** to free hosting platforms! 

**Quick Deploy (Recommended):**
```bash
./deploy.sh
# Follow the instructions to deploy to Railway
```

**Supported Platforms:**
- **🌟 Railway** - Best free tier (500 hours/month)
- **🌟 Render** - Great alternative (750 hours/month) 
- **🌟 PythonAnywhere** - Python-optimized hosting
- **🌟 Vercel** - Serverless deployment

📖 **See `DEPLOYMENT.md` for detailed deployment guides**

## 🎭 Fun Examples to Try

**Rich First-Class Lady:**
- Class: First Class
- Gender: Female
- Age: 30
- Fare: £100
- Family: 1 spouse
- Port: Southampton

**Poor Third-Class Man:**
- Class: Third Class
- Gender: Male
- Age: 25
- Fare: £7
- Family: None
- Port: Queenstown

**Child with Family:**
- Class: Second Class
- Gender: Male/Female
- Age: 8
- Fare: £25
- Family: 2 parents
- Port: Cherbourg

## 🤝 Contributing

Feel free to enhance the application:
- Add more visualizations
- Implement model comparison
- Add historical passenger stories
- Improve UI/UX design
- Add more statistical insights

## 📚 Educational Value

This project demonstrates:
- **Data Science**: Real-world machine learning application
- **Web Development**: Full-stack Flask application
- **Historical Analysis**: Understanding social patterns in disasters
- **User Experience**: Making complex data accessible

## 🎉 Credits

- **Original Dataset**: Kaggle Titanic Competition
- **Model Development**: Based on your data-cleaning.ipynb analysis
- **Historical Data**: Titanic passenger records
- **UI Design**: Modern web design principles

## ⭐ Support This Project

If you find this project helpful or interesting, please consider giving it a star on GitHub!

[![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/titanic-survival-predictor?style=for-the-badge&logo=github)](https://github.com/YOUR_USERNAME/titanic-survival-predictor)

**🚀 [View on GitHub](https://github.com/YOUR_USERNAME/titanic-survival-predictor)**

### Ways to Support:
- ⭐ **Star the repository** on GitHub
- 🍴 **Fork it** and contribute improvements
- 🐛 **Report bugs** or suggest features
- 📢 **Share it** with others interested in data science

---

**Enjoy exploring your fate aboard the Titanic! 🚢⚓**

*Kaggle Score: 0.77751 | Random Forest Classification | Interactive Web App*