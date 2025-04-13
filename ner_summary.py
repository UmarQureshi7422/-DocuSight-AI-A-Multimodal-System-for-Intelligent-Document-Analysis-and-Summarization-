import spacy
from transformers import pipeline

nlp = spacy.load("en_core_web_sm")

def generate_summary(text):
    return summarizer(text, max_length=150, min_length=40, do_sample=False)[0]['summary_text']

def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities


summarizer = pipeline("summarization")

