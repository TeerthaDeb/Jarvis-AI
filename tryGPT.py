import spacy

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Define a context (some text to ask questions about)
context = """
Hugging Face is a company based in New York City that specializes in natural language processing. 
Their open-source library, Transformers, provides thousands of pre-trained models for various NLP tasks.
"""

while True:
    # Get user input
    question = input("Ask a question (or type 'exit' to quit): ")

    if question.lower() == "exit":
        break

    # Tokenize the context and question
    context_tokens = [token.text.lower() for token in nlp(context)]
    question_tokens = [token.text.lower() for token in nlp(question)]

    best_match = None
    best_similarity = 0.0

    # Compare question tokens to context tokens and find the best match
    for sent in nlp(context).sents:
        sent_tokens = [token.text.lower() for token in sent]
        similarity = len(set(sent_tokens) & set(question_tokens)) / float(len(set(sent_tokens) | set(question_tokens)))

        if similarity > best_similarity:
            best_similarity = similarity
            best_match = sent.text

    if best_match and best_similarity > 0.5:  # Adjust the similarity threshold as needed
        print(f"Answer: {best_match}")
    else:
        print("Sorry, I couldn't find an answer in the context.")
