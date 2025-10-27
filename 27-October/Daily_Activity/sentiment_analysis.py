from transformers import pipeline
import os

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
# Initialize the sentiment analysis pipeline with DistilBERT model
sentiment_analyzer = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')

# Continuous loop for user input
while True:
    user_input = input("Enter a sentence for sentiment analysis (or type 'exit' to quit): ")

    # If user types 'exit', break the loop
    if user_input.lower() == 'exit':
        print("Exiting the sentiment analysis tool.")
        break

    # Analyze the sentiment
    result = sentiment_analyzer(user_input)

    print(result)
