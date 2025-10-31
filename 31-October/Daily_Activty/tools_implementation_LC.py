import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
import requests

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
weather_api_key = os.getenv("WEATHER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")

llm = ChatOpenAI(
    model="mistralai/mistral-7b-instruct",
    temperature=0.4,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)


def weather(city: str) -> str:
    url_1 = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}&aqi=no"
    response_1 = requests.get(url_1)

    if response_1.status_code == 200:
        data = response_1.json()


        temp_c = data["current"]["temp_c"]


        temp_f = data["current"]["temp_f"]

        return f"The temperature of {city} is {temp_c}°C ({temp_f}°F)."

    else:
        return f"Error: {response_1.status_code}"



memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

print("\n=== Start chatting with your Agent ===")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("\nConversation ended.")
        break

    if "what" in user_input.lower() and "weather" in user_input.lower():
        try:
            city = user_input.split("in")[-1].strip()
            if not city:
                print("Agent: Please specify a city name. Example: dubai")
            city_weather = weather(city)
            print(city_weather)
            memory.save_context({"input": user_input}, {"output": city_weather})
            continue
        except Exception as e:
            print("Agent: Could not find the temperature:", e)
            continue

    try:
        response = llm.invoke(user_input)
        print("Agent:", response.content)
        memory.save_context({"input": user_input}, {"output": response.content})
    except Exception as e:
        print("Error:", e)