import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import MaxAbsScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score

# Load your dataset
df = pd.read_csv(r'C:\Users\Afnan\Desktop\MachineLearning\CommentToxicity-main\train.csv\train.csv')

# Preprocess text data
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['comment_text'])

# Split data into features (X) and target (y)
y = df[['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the input data (using MaxAbsScaler for sparse matrices)
scaler = MaxAbsScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

classifiers = {
    'Logistic Regression': LogisticRegression(max_iter=1000, solver='saga')  # Use 'saga' solver
}

results = {}
for name, clf in classifiers.items():
    # Cross-validation scores
    cv_scores = cross_val_score(clf, X_train_scaled, y_train['toxic'], cv=5)
    results[name] = {
        'Accuracy': cv_scores.mean(),
        'Precision': precision_score(y_train['toxic'], clf.fit(X_train_scaled, y_train['toxic']).predict(X_train_scaled)),
        'Recall': recall_score(y_train['toxic'], clf.fit(X_train_scaled, y_train['toxic']).predict(X_train_scaled)),
        'F1-Score': f1_score(y_train['toxic'], clf.fit(X_train_scaled, y_train['toxic']).predict(X_train_scaled))
    }

results_df = pd.DataFrame(results).T
print(results_df)

for name, clf in classifiers.items():
    y_pred = clf.fit(X_train_scaled, y_train['toxic']).predict(X_test_scaled)
    cm = confusion_matrix(y_test['toxic'], y_pred)
    print(f"Confusion Matrix - {name}:")
    print(cm)
