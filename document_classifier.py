import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")  # You can replace with a more advanced model if needed

# Define the function to classify the document
def classify_document(text):
    # Process the text through the spaCy model
    doc = nlp(text)
    
    # Assuming you have a pre-trained classifier pipeline
    # We will use a simple rule-based classification for demonstration
    # If you have a custom classifier, you can use it instead.
    
    # Example: Classifying based on certain keywords or patterns in the text
    labels = ["Invoice", "Contract", "Report", "Letter"]  # Example categories
    scores = []

    # Dummy logic: Check for keywords in the text for classification
    for label in labels:
        score = sum(label.lower() in text.lower() for label in labels)  # Simple keyword match
        scores.append(score)
    
    # Get the index of the highest score
    doc_type = labels[scores.index(max(scores))]
    classification_result = {
        "labels": labels,
        "scores": scores
    }

    return doc_type, classification_result
