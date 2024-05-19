import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
import warnings
#These lines import necessary libraries for working with data, building a linear regression model, 
#preprocessing data, performing cross-validation, and handling warnings.



df = pd.read_csv('Sleep_health_and_lifestyle_dataset.csv')
df.dropna(subset=['Age', 'Gender', 'DailySteps', 'Occupation', 'Sleep Disorder'], inplace=True)


label_encoders = {col: LabelEncoder().fit(df[col]) for col in ['Gender', 'Occupation', 'Sleep Disorder']}
#Label encoding is a process of converting categorical variables into numerical format.


df = df.apply(lambda col: label_encoders[col.name].transform(col) if col.name in label_encoders else col)
X = df[['Age', 'Gender', 'DailySteps', 'Occupation']]
y = df['Sleep Disorder']
#These lines separate the features ('Age', 'Gender', 'DailySteps', 'Occupation') into
#independent variable X, and the target variable ('Sleep Disorder') into dependent variable y.

#  model
model = LinearRegression()
model.fit(X, y)

# cross-validation
cv_scores = cross_val_score(model, X, y, cv=5)  
print("Cross-Validation Scores:", cv_scores)
print("Mean Cross-Validation Score:", cv_scores.mean())

print('Model trained successfully!')
warnings.filterwarnings("ignore", category=UserWarning)
while True:
    age = float(input("Enter Age: "))
    gender = input("Enter Gender (e.g., 'Male', 'Female'): ")
    daily_steps = float(input("Enter Daily Steps: "))
    occupation = input("Enter Occupation: ")
    gender_encoded = label_encoders['Gender'].transform([gender])[0]
    occupation_encoded = label_encoders['Occupation'].transform([occupation])[0]
    prediction = model.predict([[age, gender_encoded, daily_steps, occupation_encoded]])
    predicted_sleep_disorder = round(prediction[0])
    predicted_sleep_disorder = label_encoders['Sleep Disorder'].inverse_transform([predicted_sleep_disorder])[0]
    print(f'Predicted Sleep Disorder: {predicted_sleep_disorder}')
    if input("Do you want to make another prediction? (yes/no): ").lower() != 'yes':
        break
