from openai import OpenAI
import shelve
import os
import time
import logging
import re
import datetime
import sys

enable_logging = False

if enable_logging : logging.basicConfig(level=logging.INFO)


def read_api_key_from_file(file_path, start_with):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Find the keypair
                if line.startswith(start_with):
                    # Extract the  key
                    api_key = line.strip().split(':')[1].strip()
                    return api_key
        # If no API key line is found matching the specified pattern
        raise ValueError(f"key not found starting with '{start_with}' in file '{file_path}'") 

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)  # Exit
    except ValueError as e:
        print(str(e))
        sys.exit(1)  # Exit with error code 1 if key not found


assistant_id = read_api_key_from_file('keys.txt','OPENAPI_ASSISTANT:')
client = OpenAI(api_key=read_api_key_from_file('keys.txt','OPENAPI:'))

def remove_all_threads():
    try:
        with shelve.open("threads_db") as threads_shelf:
            for sr_id, thread_id in threads_shelf.items():
                print(f"<log> Deleting thread {thread_id} for SR ID {sr_id}")
                # Delete the thread from OpenAI
                client.beta.threads.delete(thread_id)
                # Delete the record from shelve
                del threads_shelf[sr_id]
            print("<log> All threads and records have been deleted.")
    except Exception as e:
        print(f"<log> Error occurred while deleting threads: {e}")

def run_assistant(thread):
    assistant = client.beta.assistants.retrieve(assistant_id)
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )
    while run.status != "completed":
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    new_message = messages.data[0].content[0].text.value
    return new_message

def check_if_thread_exists(sr_id):
    with shelve.open("threads_db") as threads_shelf:
        return threads_shelf.get(sr_id, None)

def store_thread(sr_id, thread_id):
    with shelve.open("threads_db", writeback=True) as threads_shelf:
        threads_shelf[sr_id] = thread_id

def generate_respond(message_body, sr_id, name):
    thread_id = check_if_thread_exists(sr_id)

    if thread_id is None:
        if enable_logging : logging.info(f"Creating a new thread for {name} with sr_id {sr_id}")
        thread = client.beta.threads.create()
        store_thread(sr_id, thread.id)
        thread_id = thread.id
    else:
        if enable_logging : logging.info(f"Retrieving an existing thread for {name} with sr_id {sr_id}")
        thread = client.beta.threads.retrieve(thread_id)

    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_body,
    )

    new_message = run_assistant(thread)
    return new_message

def get_user_input_and_respond():
    name = input("Enter your name: ")
    sr_id = input("Enter your Support Ticket ID: ")

    while True:
        message_body = input("Enter the message to ask our Support(type 'exit' to quit): ").strip()

        if message_body.lower() == 'exit':
            print("Exiting...")
            break
        message_body = f"MsgDateTime:{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" + message_body
        if enable_logging : print(message_body)
        new_message = generate_respond(message_body, sr_id, name)
        pattern = r'【\d+:\d+†source】' #need to find better way, now still not perfect
        cleaned_text = re.sub(pattern, '', new_message)
        print("-------Response from AI Agent-- this is a test, NOT REAL-----\n\n" + cleaned_text + "\n\n---------End of AI Agent Response--------")

get_user_input_and_respond()
remove_all_threads()