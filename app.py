from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
import os
from analytics import analytics

app = Flask(__name__)

# Load and train the model (using the same logic from your notebook)
def load_and_train_model():
    # Load the training data
    train_data = pd.read_csv('./titanic/train.csv')
    
    # Data preprocessing (same as your notebook)
    train_data = train_data.dropna(subset=['Age'])
    train_data = train_data.drop(columns=['PassengerId', 'Name', 'Ticket', 'Cabin'])
    train_data['Embarked'] = train_data['Embarked'].fillna(train_data['Embarked'].mode()[0])
    
    # One-hot encoding
    train_data = pd.get_dummies(train_data, columns=['Sex', 'Embarked'], drop_first=True)
    train_data['Age'] = train_data['Age'].astype(int)
    
    # Prepare features and target
    X = train_data.drop(columns=['Survived'], axis=1)
    y = train_data['Survived']
    
    # Train the model using Random Forest (achieved 0.77751 Kaggle score)
    model = RandomForestClassifier(
        n_estimators=100,
        criterion='gini', 
        max_depth=5, 
        min_samples_split=3, 
        random_state=42
    )
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    
    return model, X.columns.tolist()

# Load the model
model, _ = load_and_train_model()

def preprocess_user_input(user_data):
    """Preprocess user input to match the training data format"""
    # Create a DataFrame with the user input
    df = pd.DataFrame([user_data])
    
    # Manually create one-hot encoded columns to match training data
    # Sex encoding: Sex_male (1 if male, 0 if female)
    df['Sex_male'] = 1 if user_data['Sex'] == 'male' else 0
    
    # Embarked encoding: Embarked_Q and Embarked_S (drop_first=True removes Embarked_C)
    df['Embarked_Q'] = 1 if user_data['Embarked'] == 'Q' else 0
    df['Embarked_S'] = 1 if user_data['Embarked'] == 'S' else 0
    
    # Remove original categorical columns
    df = df.drop(columns=['Sex', 'Embarked'])
    
    # Ensure all required columns are present in correct order
    feature_order = ['Pclass', 'Age', 'SibSp', 'Parch', 'Fare', 'Sex_male', 'Embarked_Q', 'Embarked_S']
    df = df[feature_order]
    
    return df

@app.route('/')
def index():
    # Track visit
    user_agent = request.headers.get('User-Agent')
    ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR'))
    analytics.track_visit(user_agent=user_agent, ip_address=ip_address)
    
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        user_data = {
            'Pclass': int(request.form['pclass']),
            'Age': int(request.form['age']),
            'SibSp': int(request.form['sibsp']),
            'Parch': int(request.form['parch']),
            'Fare': float(request.form['fare']),
            'Sex': request.form['sex'],
            'Embarked': request.form['embarked']
        }
        
        # Preprocess the input
        processed_data = preprocess_user_input(user_data)
        
        # Make prediction
        prediction = model.predict(processed_data)[0]
        probability = model.predict_proba(processed_data)[0]
        
        # Calculate survival probability
        survival_prob = probability[1] * 100  # Probability of survival
        death_prob = probability[0] * 100     # Probability of death
        
        result = {
            'survived': bool(prediction),
            'survival_probability': round(survival_prob, 1),
            'death_probability': round(death_prob, 1),
            'user_data': user_data
        }
        
        # Track the prediction
        analytics.track_prediction(
            survived=bool(prediction),
            passenger_class=user_data['Pclass'],
            gender=user_data['Sex']
        )
        
        return render_template('result.html', result=result)
    
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/analytics')
def analytics_dashboard():
    """Analytics dashboard to view usage statistics"""
    stats = analytics.get_stats()
    return render_template('analytics.html', stats=stats)

@app.route('/api/analytics')
def analytics_api():
    """API endpoint to get analytics data as JSON"""
    stats = analytics.get_stats()
    return jsonify(stats)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)