import os
import pickle
import argparse
import json
import jsonpickle

import google.generativeai as genai

from utils.data_reader import read_transcript
from utils.extractive_summarization import extractive_summarization

parser = argparse.ArgumentParser(description='CLI Argument Parser')
parser.add_argument('--transcript', type=str, help='File name with .txt extension of the sales call transcript',
                    default="sales_call_transcript.txt")
parser.add_argument('--question', type=str, help='Your question (prompt)',
                    default="What product was the customer interested in?")
parser.add_argument('--persist_chat_history', type=bool, help='Use chat history', default=False)
parser.add_argument('--session_id', type=str, help='Tracker session for chat persistence', default="1")
parser.add_argument('--include_background_context', type=bool, help='Include background context', default=False)
parser.add_argument('--background_context_file_name', type=str, help='Background context file name',
                    default="customerDocuments/design_doc.txt")

args = parser.parse_args()

if args.persist_chat_history:
    print("Caution: Using chat history is bugged! It will not work as expected.")

transcript = read_transcript(args.transcript)
# print(transcript)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "<your API key if not set as env var>"))

system_instruction = """You are an assistant working sales and customer calls,
                                you transform transcripts into customer intelligence.
                                Yours goals are to forecast, assess churn risk,
                                update Salesforce, share product feedback,
                                and bring insights to your the team.
                                
                                Our saleperson is named Satya and our comapny is Nvdia."""

if args.include_background_context:
    background_context = extractive_summarization(args.background_context_file_name)
    system_instruction += "\n" + "Here is some background context: " + "\n" + background_context

system_instruction += "\n" + transcript

model = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction=system_instruction)

chat = model.start_chat()

chat_history = None
if args.persist_chat_history:
    if os.path.exists(f'chat_history_{args.session_id}.pkl') and os.stat(
            f'chat_history_{args.session_id}.pkl').st_size > 1:
        with open(f'chat_history_{args.session_id}.pkl', "rb") as f:
            chat_history = pickle.load(f)  # print(f'chat_history is:\n {chat_history}')

        if chat_history:
            chat = model.start_chat(history=[chat_history])

response = chat.send_message(args.question)

print(response.text)

# Save the chat history https://stackoverflow.com/a/78474228/5728614
with open(f'chat_history_{args.session_id}.pkl', "wb") as f:
    # f.write(jsonpickle.encode(chat.history, True)) # 1st way
    # json.dump(jsonpickle.encode(chat.history, True), f) # 1.5st way
    pickle.dump(chat.history, f)  # 2nd way

# with open(f'chat_history_{SESSION_ID}.json', "a") as f:
## Second attempt - you dont need to update it, as it include the previous
# f.write(str(chat.history))

## First attempt
# if os.stat(f'chat_history_{SESSION_ID}.json').st_size == 0:
#     # If file is empty, write the first line
#     f.write(f'[\n')
# else:
#    # If file is not empty, remove the last line (']')
#     with open(f'chat_history_{SESSION_ID}.json', 'r') as file:
#         lines = file.readlines()
#     with open(f'chat_history_{SESSION_ID}.json', 'w') as file:
#         file.writelines(lines[:-1])

# f.write(f'parts {{\n text: "{prompt}"\n}}\n')
# f.write(f'role: "user,"\n')
# f.write(f'parts {{\n text: "{response.text}"\n}}\n')
# f.write(f'role: "model"\n')
# f.write(f']\n')
