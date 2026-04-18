import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Training dataset
data = {
    "text": [
        "pizza", "burger", "restaurant",
        "uber", "bus", "train",
        "movie", "netflix",
        "rent", "house rent"
    ],
    "category": [
        "Food", "Food", "Food",
        "Transport", "Transport", "Transport",
        "Entertainment", "Entertainment",
        "Rent", "Rent"
    ]
}

df = pd.DataFrame(data)

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df["text"])

model = MultinomialNB()
model.fit(X, df["category"])

def predict_category(text):
    X_test = vectorizer.transform([text])
    return model.predict(X_test)[0]