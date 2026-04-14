import argparse
import json
from pathlib import Path

import joblib
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


DEFAULT_DATA_PATH = Path(r"C:\Users\Manav\Downloads\archive (13)\News_Category_Dataset_v3.json")
MODEL_PATH = Path("models/newsbot_pipeline.joblib")
TARGET_CATEGORIES = {"TECH", "ENTERTAINMENT", "POLITICS", "BUSINESS"}
CATEGORY_LABELS = {"TECH": "TECHNO"}


def load_spacy_model():
    """Load only the components needed for tokenization and lemmatization."""
    try:
        return spacy.load(
            "en_core_web_sm",
            disable=["parser", "ner", "textcat", "senter"],
        )
    except OSError as exc:
        raise RuntimeError(
            "spaCy model 'en_core_web_sm' is not installed. Run: "
            "python -m spacy download en_core_web_sm"
        ) from exc


def normalize_category(category):
    return CATEGORY_LABELS.get(category, category)


def load_dataset(path):
    headlines = []
    labels = []

    with Path(path).open("r", encoding="utf-8") as dataset:
        for line in dataset:
            if not line.strip():
                continue

            row = json.loads(line)
            category = row.get("category")
            headline = (row.get("headline") or "").strip()

            if category in TARGET_CATEGORIES and headline:
                headlines.append(headline)
                labels.append(normalize_category(category))

    return headlines, labels


def preprocess_headlines(headlines, nlp):
    cleaned = []

    for doc in nlp.pipe(headlines, batch_size=500):
        tokens = [
            token.lemma_.lower().strip()
            for token in doc
            if not token.is_stop and not token.is_punct and not token.is_space
        ]
        cleaned.append(" ".join(token for token in tokens if token))

    return cleaned


def train(data_path=DEFAULT_DATA_PATH, model_path=MODEL_PATH):
    print("Loading dataset...")
    headlines, labels = load_dataset(data_path)
    print(f"Loaded {len(headlines)} rows across {sorted(set(labels))}.")

    print("Loading spaCy English model...")
    nlp = load_spacy_model()

    print("Preprocessing headlines...")
    processed = preprocess_headlines(headlines, nlp)

    print("Vectorizing with CountVectorizer unigrams+bigrams and max_features=5000...")
    vectorizer = CountVectorizer(ngram_range=(1, 2), max_features=5000)
    x = vectorizer.fit_transform(processed)
    y = labels

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    print("Training Logistic Regression...")
    model = LogisticRegression(max_iter=1000, class_weight="balanced")
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)

    print(f"Accuracy: {accuracy:.4f}")
    print(classification_report(y_test, predictions))

    model_path = Path(model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "model": model,
            "vectorizer": vectorizer,
            "accuracy": accuracy,
            "categories": sorted(set(labels)),
        },
        model_path,
    )
    print(f"Saved model to {model_path.resolve()}")


def load_model(model_path=MODEL_PATH):
    return joblib.load(model_path)


def predict_category(headline, bundle=None, nlp=None):
    if bundle is None:
        bundle = load_model()
    if nlp is None:
        nlp = load_spacy_model()

    processed = preprocess_headlines([headline], nlp)
    features = bundle["vectorizer"].transform(processed)
    return bundle["model"].predict(features)[0]


def chat(model_path=MODEL_PATH):
    bundle = load_model(model_path)
    nlp = load_spacy_model()

    print("NewsBot is ready. Type a headline, or type 'quit'/'exit' to stop.")
    while True:
        headline = input("Headline: ").strip()
        if headline.lower() in {"quit", "exit"}:
            print("Goodbye.")
            break
        if not headline:
            print("Please enter a headline.")
            continue

        print(f"Predicted category: {predict_category(headline, bundle, nlp)}")


def main():
    parser = argparse.ArgumentParser(description="Train or run NewsBot.")
    parser.add_argument("command", choices=["train", "chat"])
    parser.add_argument("--data", default=str(DEFAULT_DATA_PATH), help="Path to the JSON lines dataset.")
    parser.add_argument("--model", default=str(MODEL_PATH), help="Path to save/load the model.")
    args = parser.parse_args()

    if args.command == "train":
        train(args.data, args.model)
    else:
        chat(args.model)


if __name__ == "__main__":
    main()
