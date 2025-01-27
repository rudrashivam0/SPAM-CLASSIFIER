import streamlit as st
import nltk
import pickle
import os  # Add this import to check if files exist
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Ensure punkt tokenizer is downloaded (not punkt_tab)
try:
    nltk.data.find('tokenizers/punkt')  # This checks if the punkt tokenizer is already available
except LookupError:
    nltk.download('punkt', quiet=True)  # If missing, explicitly download punkt tokenizer

# Ensure stopwords are downloaded (used in text preprocessing)
try:
    nltk.data.find('corpora/stopwords')  # Check if stopwords are available
except LookupError:
    nltk.download('stopwords', quiet=True)  # If missing, explicitly download stopwords

# Define file paths
vectorizer_path = 'vectorizer.pkl'
model_path = 'model.pkl'

# Check if files exist
if not os.path.exists(vectorizer_path) or not os.path.exists(model_path):
    st.error("Required files 'vectorizer.pkl' and 'model.pkl' are missing.")
    if not os.path.exists(vectorizer_path):
        st.error(f"File not found: {vectorizer_path}")
    if not os.path.exists(model_path):
        st.error(f"File not found: {model_path}")
    exit(1)  # Exit if files are missing

# Initialize PorterStemmer
ps = PorterStemmer()

# Function to preprocess text
def transform_text(text):
    text = text.lower()  # Convert to lowercase
    tokens = text.split()
    # tokens = nltk.word_tokenize(text)  # Tokenize text
    tokens = [token for token in tokens if token.isalnum()]  # Remove non-alphanumeric tokens
    tokens = [token for token in tokens if token not in stopwords.words('english')]  # Remove stopwords
    tokens = [ps.stem(token) for token in tokens]  # Apply stemming
    return " ".join(tokens)

# Load vectorizer and model
with open(vectorizer_path, 'rb') as file:
    tfidf = pickle.load(file)
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Add dynamic port binding for Heroku
port = os.getenv("PORT", 8501)  # Get the dynamic port from Heroku

st.title("Email or SMS-SPAM Classifier")
input_sms = st.text_area("Enter the Email or SMS", placeholder="Type your message here...")

if st.button('Check for Spam'):
    # Preprocess input
    transformed_sms = transform_text(input_sms)
    # Vectorize input
    vector_input = tfidf.transform([transformed_sms])
    # Predict
    result = model.predict(vector_input)[0]

    # Display results
    if result == 1:
        st.header("🚨 Spam!")
    else:
        st.header("✅ Not Spam")
