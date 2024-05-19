from flask import Flask, request, jsonify
import pandas as pd
import os
import joblib
import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dropout, Bidirectional, Dense, Embedding
from tensorflow.keras.models import Sequential
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)

# Load the dataset
file_path = r'C:\Users\Afnan\Desktop\MachineLearning\CommentToxicity-main\train.csv\train.csv'
df = pd.read_csv(file_path)

# Prepare the data
X = df['comment_text']
y = df[['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']]

# Tokenize the text
max_words = 20000
tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(X)
X_seq = tokenizer.texts_to_sequences(X)

# Pad sequences
max_sequence_length = 100
X_pad = pad_sequences(X_seq, maxlen=max_sequence_length)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_pad, y, test_size=0.2, random_state=42)

# Check if the model file exists
model_file_path = 'toxicity_classifier_model.pkl'  # Change the file path if needed

if not os.path.exists(model_file_path):
    # Define the model if the file doesn't exist
    model = Sequential([
        Embedding(max_words+1, 32, input_length=max_sequence_length),
        Bidirectional(LSTM(32, activation='tanh')),
        Dense(128, activation='relu'),
        Dense(256, activation='relu'),
        Dense(128, activation='relu'),
        Dense(6, activation='sigmoid')
    ])
    # Compile the model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    # Train the model
    history = model.fit(X_train, y_train, epochs=5, batch_size=64, validation_data=(X_test, y_test))
    # Save the trained model as a .pkl file using joblib
    joblib.dump(model, model_file_path)
else:
    # Load the saved model if it exists
    model = joblib.load(model_file_path)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    if 'comment' not in data:
        return jsonify({'error': 'Comment not found in request!'}), 400

    comment = data['comment']

    try:
        # Tokenize the new text
        new_text_seq = tokenizer.texts_to_sequences([comment])
        # Pad sequences
        new_text_pad = pad_sequences(new_text_seq, maxlen=max_sequence_length)
        # Make predictions
        new_predictions = model.predict(new_text_pad)
        # Threshold the predictions
        threshold = 0.5
        binary_predictions = (new_predictions > threshold).astype(int)
        # Map predictions to labels
        categories = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
        result = {label: bool(pred) for label, pred in zip(categories, binary_predictions[0])}
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Prediction error: {e}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
