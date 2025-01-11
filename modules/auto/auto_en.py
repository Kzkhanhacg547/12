import time
import random
import threading
import json
import requests
from zlapi.models import Message, ThreadType
from zlapi._message import Mention
with open('setting.json', 'r') as config_file:
    config = json.load(config_file)

API_URL = config.get("API", "")
API_URL = f"{API_URL}/ask?data="



def get_grammar_lesson():
    """Generate a unique English grammar lesson using the new API"""
    # Chọn ngẫu nhiên một chủ đề từ mảng grammar_topics
    grammar_topics = [
        "Explain the use of past simple tense with examples.",
        "Explain the use of future simple tense with examples.",
        "Explain the use of future continuous tense with examples.",
        "Explain the use of present perfect continuous tense with examples.",
        "Explain the use of past perfect continuous tense with examples.",
        "How to form future perfect tense with examples?",
        "What is the difference between present perfect and present perfect continuous tenses, with examples?",
        "What is the difference between past perfect and past perfect continuous tenses, with examples?",
        "Explain the use of the future perfect continuous tense with examples.",
        "Explain the use of present continuous tense with examples.",
        "Explain the use of past continuous tense with examples.",
        "What is the difference between present perfect and past simple tenses, with examples?",
        "How to use 'who' and 'whom' in sentences, with examples?",
        "Explain the use of 'at', 'in', and 'on' in prepositional phrases, with examples.",
        "Describe the difference between active and passive voice with examples.",
        "What are the uses of 'get' in different contexts, with examples?",
        "Explain the different types of conditional sentences in English.",
        "Describe how to use 'and', 'but', 'or', and 'so' in compound sentences.",
        "What is the difference between 'which' and 'that' in relative clauses?",
        "Provide examples of common phrasal verbs with 'take' and 'get'.",
        "Explain the difference between countable and uncountable nouns with examples.",
        "Give examples of direct and indirect questions in English.",
        "How do modal verbs like 'can', 'could', 'will', 'would' function in sentences?",
        "What are determiners, and how do we use them in English sentences?",
        "What are some exceptions when forming plurals in English?",
        "Explain the use of gerunds and infinitives with examples.",
        "What are the differences between formal and informal writing styles?",
        "How do we use 'some', 'any', 'much', 'many', 'few', and 'little'?",
        "What is the difference between 'used to' and 'be used to', with examples?",
        "Explain the use of present simple tense with examples",
        "Explain the use of past perfect tense with examples",
        "Give an example of direct and indirect speech in English",
        "Describe the difference between countable and uncountable nouns",
        "How to form conditionals in English, with examples"
    ]

    try:
        # Chọn ngẫu nhiên một chủ đề từ grammar_topics
        topic = random.choice(grammar_topics)

        # Gửi yêu cầu API với chủ đề ngẫu nhiên
        response = requests.get(API_URL, params={'data': topic})
        if response.status_code == 200:
            lesson_data = response.json()
            if lesson_data.get("answer"):
                formatted_lesson = f"📚 Daily English Learning\n\n{lesson_data['answer']}\n\n#EnglishGrammar #Learning"
                return formatted_lesson
            else:
                print(f"No answer found for topic: {topic}")
        else:
            print(f"Error with API response: {response.status_code}")
        return None
    except Exception as e:
        print(f"Error generating lesson: {e}")
        return None


def get_approved_groups():
    """Read approved groups from cache file"""
    try:
        with open("./modules/cache/duyetboxdata.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading approved groups: {e}")
        return []

def start_auto(client):
    while True:
        try:
            # Get the grammar lesson
            lesson = get_grammar_lesson()

            # Only proceed if we got a valid lesson
            if lesson:
                # Get approved groups
                approved_groups = get_approved_groups()

                # Send to all approved groups
                for thread_id in approved_groups:
                    try:
                        client.send(Message(text=lesson), thread_id, ThreadType.GROUP)
                        print(f"Sent lesson to group {thread_id}")
                        time.sleep(2)  # Small delay between sends
                    except Exception as e:
                        print(f"Error sending to group {thread_id}: {e}")
            else:
                print("Failed to generate lesson, will retry in next iteration")

            # Wait 15 minutes before next lesson
            time.sleep(900)  # 15 minutes

        except Exception as e:
            print(f"Error in auto command: {e}")
            time.sleep(10)
