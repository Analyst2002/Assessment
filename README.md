# NewsBot - Headline Classifier

NewsBot is an NLP project for classifying news headlines into four categories:

- `TECHNO`
- `ENTERTAINMENT`
- `POLITICS`
- `BUSINESS`

The PDF says `TECHNO`, while the Kaggle dataset uses `TECH`. This project filters `TECH` rows from the dataset and renames that label to `TECHNO` so the output matches the assessment requirement.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m spacy download en_core_web_sm
```

## Train

```powershell
.\.venv\Scripts\python newsbot.py train --data "C:\Users\Manav\Downloads\archive (13)\News_Category_Dataset_v3.json"
```

The script:

1. Loads the newline-delimited JSON dataset.
2. Keeps only `TECH`, `ENTERTAINMENT`, `POLITICS`, and `BUSINESS`.
3. Loads spaCy's English model without parser, NER, textcat, or sentence components.
4. Lowercases, removes stopwords and punctuation, and lemmatizes headlines.
5. Builds `X` using `CountVectorizer(ngram_range=(1, 2), max_features=5000)`.
6. Splits the data with stratification so categories stay balanced.
7. Trains Logistic Regression with enough iterations.
8. Reports accuracy and saves the model to `models/newsbot_pipeline.joblib`.

The vocabulary is limited to 5000 features to keep the feature matrix smaller, reduce noise from rare words, and make training faster while still preserving the most useful unigram and bigram signals.

## Chatbot

```powershell
.\.venv\Scripts\python newsbot.py chat
```

Type headlines into the terminal. Type `quit` or `exit` to stop.

## Streamlit App

```powershell
.\.venv\Scripts\streamlit run app.py
```
