import requests
from zlapi.models import Message
from colorama import Fore

# Module description
des = {
    'version': "1.0.0",
    'credits': "YourName",
    'description': "Fetch a response from GPT API"
}

def get_gpt_response(user_message):
    """Fetch a response from the GPT API based on user input."""
    url = "https://chatgpt-api8.p.rapidapi.com/"
    payload = [
        {
            "content": "Hello! I'm an AI assistant bot based on ChatGPT 3. How may I help you?",
            "role": "system"
        },
        {
            "content": user_message,
            "role": "user"
        }
    ]
    headers = {
        "x-rapidapi-key": "63386379b5msh92b3b1b130c7b35p12feacjsn21149355f3c9",  # Replace with a valid key
        "x-rapidapi-host": "chatgpt-api8.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()

        # Check for 'text' key in the response dictionary
        if 'text' in data:
            return data['text']
        else:
            print(f"{Fore.RED}Unexpected response format: {data}")
            return "Sorry, I couldn't process your request at the moment."

    except requests.exceptions.HTTPError as http_err:
        print(f"{Fore.RED}HTTP error occurred: {http_err}")
        return "Sorry, there was a problem with the request."
    except requests.exceptions.RequestException as req_err:
        print(f"{Fore.RED}Request error occurred: {req_err}")
        return "Sorry, there was a problem with the network request."
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}")
        return "Sorry, an unexpected error occurred."

def handle_gpt_command(message, message_object, thread_id, thread_type, author_id, client):
    """Handle the gpt command to get a response from GPT and reply to the message."""
    content = message_object.content.strip()
    command_parts = content.split(maxsplit=1)
    user_message = command_parts[1].strip() if len(command_parts) > 1 else ""

    if not user_message:
        send_error_message(thread_id, thread_type, client, "Vui lòng nhập nội dung.")
        return

    try:
        gpt_response = get_gpt_response(user_message)
        client.replyMessage(
            Message(text=gpt_response),
            message_object,
            thread_id=thread_id,
            thread_type=thread_type
        )
    except Exception as e:
        client.replyMessage(
            Message(text="Đã xảy ra lỗi khi xử lý lệnh GPT."),
            message_object,
            thread_id=thread_id,
            thread_type=thread_type
        )
        print(f"{Fore.RED}Error handling gpt command: {e}")

def send_error_message(thread_id, thread_type, client, error_message="Lỗi."):
    client.send(Message(text=error_message), thread_id=thread_id, thread_type=thread_type)

def get_szl():
    """Register GPT module."""
    return {
        'gpt': handle_gpt_command
    }
