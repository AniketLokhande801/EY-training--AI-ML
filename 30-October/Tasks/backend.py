# import os
# import requests
# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
#
# # Load environment variables
# load_dotenv()
#
# # Get API keys from environment variables
# SERP_API_KEY = os.getenv("SERP_API_KEY")
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# base_url ="https://openrouter.ai/api/v1"
#
#
#
# # 1. Itinerary Builder Agent (Using OpenRouter)
# def generate_itinerary(vacation_city, trip_type, number_of_days):
#     prompt = f"Create a {trip_type}  short itinerary for {vacation_city} for {number_of_days} days. Include activities, restaurants, and sightseeing spots."
#
#     llm = ChatOpenAI(
#         model="openai/o3-mini",
#         temperature=0.4,
#         max_tokens=256,
#         api_key=OPENROUTER_API_KEY,
#         base_url=base_url,
#     )
#     response=llm.invoke(prompt)
#
#     return response.content
#
#
# import requests
#
#
# def fetch_flights(current_city, vacation_city, start_date):
#     query = f"flights from {current_city} to {vacation_city} starting {start_date}"
#     url = f"https://serpapi.com/search?q={query}&api_key={SERP_API_KEY}"
#
#     response = requests.get(url)
#     flight_data = response.json()
#
#     if "organic_results" not in flight_data:
#         return []
#
#     flights = []
#     for result in flight_data.get("organic_results", []):
#         flight = {
#             "airline": result.get("airline", "N/A"),
#             "price": result.get("price", "N/A"),
#             "departure_time": result.get("departure_time", "N/A")
#         }
#         flights.append(flight)
#
#     return flights
#
#
# def fetch_hotels(vacation_city, check_in, check_out):
#     query = f"hotels in {vacation_city} from {check_in} to {check_out}"
#     url = f"https://serpapi.com/search?q={query}&api_key={SERP_API_KEY}"
#
#     response = requests.get(url)
#     hotel_data = response.json()
#
#     if "organic_results" not in hotel_data:
#         return []
#
#     hotels = []
#     for result in hotel_data.get("organic_results", []):
#         hotel = {
#             "hotel_name": result.get("hotel_name", "N/A"),
#             "price": result.get("price", "N/A"),
#             "rating": result.get("rating", "N/A"),
#             "address": result.get("address", "N/A")
#         }
#         hotels.append(hotel)
#
#     return hotels
#
#
# # 4. YouTube Vlog Recommender Agent (Using SERP API)
# def fetch_youtube_vlogs(vacation_city, trip_type):
#     query = f"Youtube travel vlog {vacation_city} {trip_type}"
#     url = f"https://serpapi.com/search?q={query}&api_key={SERP_API_KEY}"
#
#     response = requests.get(url)
#     youtube_data = response.json()
#
#     if "video_results" not in youtube_data:
#         return []
#
#     vlogs = []
#     for result in youtube_data.get("video_results", []):
#         vlog = {
#             "title": result.get("title", "N/A"),
#             "url": result.get("link", "N/A"),
#             "channel": result.get("channel", "N/A")
#         }
#         vlogs.append(vlog)
#
#     return vlogs
#

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.7,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)

# Prompt for sentiment analysis
prompt_sentiment_analysis = ChatPromptTemplate.from_template(
    "<s>[INST] Analyze the sentiment of the following feedback. "
    "If the sentiment is positive, return 'positive'. If the sentiment is negative, return 'negative'. "
    "Feedback: {feedback} [/INST]"
)

# Prompt to generate a response for positive feedback
prompt_positive_sentiment_response = ChatPromptTemplate.from_template(
    "<s>[INST] Given the positive sentiment in the feedback, generate a thank you response to the user. dont give your faithfully/regards and all that  give just message  "
    "Feedback: {feedback} [/INST]"
)

# Prompt to generate a response for negative feedback
prompt_negative_sentiment_response = ChatPromptTemplate.from_template(
    "<s>[INST] Given the negative sentiment in the feedback, generate an apology response. "
    "Also, analyze the tone of the feedback (e.g., frustrated, neutral, disappointed) and respond accordingly  dont give your faithfully/regards and all that give just message "
    "Feedback: {feedback} [/INST]"
)

parser = StrOutputParser()


def get_sentiment(feedback: str, conversation_history: str) -> str:
    """Get the sentiment of the feedback (positive/negative) considering conversation history."""
    conversation_input = {
        "feedback": feedback,
        "conversation_history": conversation_history
    }
    chain = prompt_sentiment_analysis | llm | parser
    sentiment = chain.invoke(conversation_input)
    return sentiment.strip().lower()


def positive_sentiment_response_generator(feedback: str, conversation_history: str) -> str:
    """Generate a thank-you response for positive feedback considering conversation history."""
    conversation_input = {
        "feedback": feedback,
        "conversation_history": conversation_history
    }
    chain = prompt_positive_sentiment_response | llm | parser
    response = chain.invoke(conversation_input)
    return response.strip()


def negative_sentiment_response_generator(feedback: str, conversation_history: str) -> str:
    """Generate an apology response for negative feedback considering conversation history."""
    conversation_input = {
        "feedback": feedback,
        "conversation_history": conversation_history
    }
    chain = prompt_negative_sentiment_response | llm | parser
    response = chain.invoke(conversation_input)
    return response.strip()


def conversation():
    conversation_history = ""  # To keep track of previous feedback and responses
    print("Welcome to the feedback assistant. Please provide your feedback.")

    while True:
        # Collecting feedback from user
        feedback = input("\nPlease provide your feedback (type 'exit' to quit): ")

        if feedback.lower() == "exit":
            print("Thank you for using the Feedback Assistant!")
            break

        # Analyze sentiment of the feedback, including conversation history
        sentiment = get_sentiment(feedback, conversation_history)

        if sentiment == "positive":
            response = positive_sentiment_response_generator(feedback, conversation_history)
        elif sentiment == "negative":
            response = negative_sentiment_response_generator(feedback, conversation_history)
        else:
            response = "Sorry, I couldn't understand the sentiment of your feedback."

        print("\nResponse to Your Feedback: ")
        print(response)

        # Update conversation history (feedback + response)
        conversation_history += f"User: {feedback}\nAssistant: {response}\n"


if __name__ == "__main__":
    conversation()

