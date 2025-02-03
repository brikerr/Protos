import random
import datetime
import speech_recognition as sr
from openai import OpenAI
from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play

client = OpenAI()
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Wake word
WAKE_WORD = "ai"

# Mood settings (user can customize)
MOOD = "cheerful"  # Options: cheerful, formal, funny, relaxed

# Wake-up responses by time of day
WAKE_RESPONSES = {
    "morning": ["Good morning! How can I help?", "Rise and shine! What’s the plan today?"],
    "afternoon": ["Good afternoon! What do you need?", "Hope your day is going well. What’s up?"],
    "evening": ["Good evening! How can I assist?", "Evening! AI is ready to help."],
    "night": ["It’s late! Need anything before you rest?", "Night owl mode activated! What’s up?"]
}

# Seasonal responses
SEASONAL_RESPONSES = {
    "winter": ["Brrr! It's cold! Need help?", "Winter vibes! What do you need?"],
    "spring": ["Spring is here! How can I assist?", "Fresh season, fresh tasks! What’s up?"],
    "summer": ["It’s sunny! What do you need?", "Summer mode activated! How can I help?"],
    "fall": ["Leaves are falling, AI is calling! What’s up?", "Cozy fall vibes! How can I assist?"]
}

# Holiday responses
HOLIDAY_RESPONSES = {
    "New Year": ["Happy New Year! Ready to start fresh?", "New year, new tasks! What's up?"],
    "Valentine's Day": ["Happy Valentine's Day! Need any love advice?", "Feeling romantic today?"],
    "Easter": ["Happy Easter! Hope you’re having an egg-cellent day!", "Easter vibes! What can I do?"],
    "Halloween": ["Boo! Just kidding. How can I assist?", "Spooky season! Need help with anything eerie?"],
    "Thanksgiving": ["Happy Thanksgiving! What are you grateful for today?", "Turkey day vibes! What’s up?"],
    "Christmas": ["Merry Christmas! Feeling festive?", "Christmas cheer is here! How can I help?"]
}

# Mood-based responses
MOOD_RESPONSES = {
    "cheerful": ["Hey there, superstar! How can I help?", "What’s up, friend? AI is here!"],
    "formal": ["Hello. How may I assist you?", "Good day. What do you need assistance with?"],
    "funny": ["Ah, you woke me up! What’s up, boss?", "AI is online—don't break me!"],
    "relaxed": ["Hey, what’s up? I’m all ears.", "Chill mode activated. What do you need?"]
}

def text_to_speech(text):
    """Convert text to speech and play the response."""
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(model="tts-1", voice="alloy", input=text)
    response.stream_to_file(speech_file_path)
    play(AudioSegment.from_mp3(speech_file_path))

def get_current_season():
    """Determine the current season."""
    month = datetime.datetime.now().month
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:
        return "fall"

def get_current_holiday():
    """Return a holiday greeting if today is a special day."""
    today = datetime.datetime.now().strftime("%m-%d")
    holiday_dict = {
        "01-01": "New Year",
        "02-14": "Valentine's Day",
        "04-17": "Easter",  # Fixed date; actual Easter changes each year
        "10-31": "Halloween",
        "11-28": "Thanksgiving",  # Approximate
        "12-25": "Christmas",
    }
    return holiday_dict.get(today, None)

def get_time_based_response():
    """Choose a response based on time of day, season, holiday, and mood."""
    current_hour = datetime.datetime.now().hour
    current_season = get_current_season()
    current_holiday = get_current_holiday()

    # If today is a holiday, prioritize holiday responses
    if current_holiday:
        return random.choice(HOLIDAY_RESPONSES[current_holiday])

    # Randomly use a seasonal greeting 30% of the time
    if random.random() < 0.3:
        return random.choice(SEASONAL_RESPONSES[current_season])

    # Choose a time-based greeting
    if 5 <= current_hour < 12:
        base_response = random.choice(WAKE_RESPONSES["morning"])
    elif 12 <= current_hour < 18:
        base_response = random.choice(WAKE_RESPONSES["afternoon"])
    elif 18 <= current_hour < 23:
        base_response = random.choice(WAKE_RESPONSES["evening"])
    else:
        base_response = random.choice(WAKE_RESPONSES["night"])

    # Apply mood-based customization
    mood_response = random.choice(MOOD_RESPONSES[MOOD])
    return f"{mood_response} {base_response}"

def listen_for_wake_word():
    """Listen for the wake word 'AI' and respond with a customized greeting."""
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening for wake word...")

        while True:
            try:
                audio = recognizer.listen(source, timeout=10)
                text = recognizer.recognize_google(audio).lower()

                if WAKE_WORD in text.split():
                    response = get_time_based_response()
                    print(f"Wake word '{WAKE_WORD}' detected. Responding with: {response}")
                    text_to_speech(response)
                    return True
            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                continue
            except sr.WaitTimeoutError:
                print("Timeout reached while waiting for wake word.")
                continue

def listen_for_command():
    """Listen for a user's command after wake word is detected."""
    with microphone as source:
        print("Listening for command...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        return None

def get_gpt_response(prompt):
    """Generate AI response using GPT."""
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "Your name is Speaker, you answer all kinds of questions for me."},
                  {"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content

def main():
    """Main loop for wake word detection and AI interaction."""
    while True:
        if listen_for_wake_word():
            while True:
                user_input = listen_for_command()
                if not user_input:
                    break
                gpt_response = get_gpt_response(user_input)
                print(f"GPT says: {gpt_response}")
                text_to_speech(gpt_response)

if __name__ == "__main__":
    main()