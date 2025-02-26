import os

import openai
from dotenv import load_dotenv

load_dotenv()

# OpenRouter setup
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"
import os
import openai
import tweepy
import time
from dotenv import load_dotenv

load_dotenv()

# Configure for DeepSeek-V3
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"
# MODEL_NAME = "deepseek/deepseek-r1"  # Verified working model
MODEL_NAME = "deepseek/deepseek-chat:free"  # Better for simple jokes

PRIMERI = ["- DOBOJ JE UZ: Sve rupe na svojim ulicama!\n"
           "- DOBOJ JE UZ: Debele golubove u parku\n"
           "- DOBOJ JE UZ: Obavezno korišćenje rakije kao dezinfekcije u ambulanti\n"
           "- DOBOJ JE UZ: Taksiste koji pitaju \"Gde je ta Vukojebina?\n"
           "- DOBOJ JE UZ: Kengure\n"
           "- DOBOJ JE UZ: Budjav lebac\n"
           "- DOBOJ JE UZ: Lutalice koje traže papriku za ajvar! 🌶️\n"
           "- DOBOJ JE UZ: Svinjski roštilj na stepeništima! 🐷🔥"]

SYSTEM_CONTENT = '''
Ti si komičar koji pravi krate šale na srpskom, a tema je Doboj grad koji podrzava sve zivo.
Izbjegavaj religiju i nacionalizam.
Šale neka budu poglupe i apsurdne.
'''


def generate_doboj_joke(max_retries=3):
    prompt = (
            "Generiši jednu smešnu tvrdnju o Doboju na srpskom. MORAŠ POČETI SA 'DOBOJ JE UZ: '. "
            "Maksimalno 8 reči. Primeri:\n"
            "Nemoj puno razmisljati lupi prvu recenicu koja ti padne na pamet:\n"
            f"Primeri:\n" + '\n'.join([f"- {primer}" for primer in PRIMERI])
    )

    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_CONTENT},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.8
            )

            print(response, 'response')

            if response.choices and (content := response.choices[0].message.content.strip()):
                if not content.startswith("DOBOJ JE UZ:"):
                    content = f"DOBOJ JE UZ: {content}"
                return content

            print(f"Pokušaj {attempt + 1}/{max_retries} - prazan odgovor")
            time.sleep(1)

        except Exception as e:
            print(f"Greška (pokušaj {attempt + 1}/{max_retries}):", str(e))
            time.sleep(2)

    return None


# Rest of the Twitter functions remain the same...


def create_twitter_api():
    return tweepy.Client(
        bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_SECRET_KEY"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    )


def post_tweet(api, message):
    try:
        response = api.create_tweet(text=message)
        print("Tweet objavljen! ID:", response.data['id'])
    except Exception as e:
        print("Greška pri tweetovanju:", e)


if __name__ == "__main__":
    joke = generate_doboj_joke()

    if joke:
        print("Generisana šala:", joke)
        twitter_api = create_twitter_api()
        if twitter_api:
            post_tweet(twitter_api, joke)
    else:
        print("Nije uspelo generisanje šale - nijedan tweet nije poslat")
