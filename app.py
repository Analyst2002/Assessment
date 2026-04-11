import streamlit as st

from newsbot import MODEL_PATH, load_model, load_spacy_model, predict_category


@st.cache_resource
def get_resources():
    return load_model(MODEL_PATH), load_spacy_model()


st.set_page_config(page_title="NewsBot", page_icon="NB")
st.title("NewsBot")
st.write("Enter a news headline to classify it as TECHNO, ENTERTAINMENT, POLITICS, or BUSINESS.")

if not MODEL_PATH.exists():
    st.error("Model not found. Train it first with: python newsbot.py train")
    st.stop()

bundle, nlp = get_resources()
headline = st.text_input("Headline")

if headline:
    category = predict_category(headline, bundle, nlp)
    st.subheader(f"Predicted category: {category}")

st.caption(f"Last trained accuracy: {bundle.get('accuracy', 0):.2%}")
