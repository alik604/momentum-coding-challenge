# pylint: disable=locally-disabled, multiple-statements, fixme, line-too-long
import os

import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "<your API key if not set as env var>"))

model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                              # system_instruction="""You are an assistant working sales and customer calls,
                              # you transform it data into customer intelligence.
                              # Yours goals are to Capture forecast or churn risk,
                              # update Salesforce, share product feedback,
                              # and bring insights to your entire team. """
                              system_instruction="Generate data. Do not include no extra tags, comments, or records of actions such as ending calls, sighs or pauses.")

prompt = "I need you to generation a complete sales calling starting with the following data. The output should be at least 30 messages\n\n```\n00:00:00 Sam (openai.com): Hey there Staya.\n00:00:02 Satya  (microsoft.com): Hi Sam, how are you?\n00:00:05 Sam (openai.com): I'm doing good. Do you think you can give us 10000 more GPUs?\n00:00:06 Satya (microsoft.com): I'm sorry Sam we can't do 10000, how about 5000?\n```"

response = model.generate_content(prompt)

# output = response.text. #// Question: which do you prefer? I prefer what I had, despite it being redundant
print(response.text)

# write the output to a file. Use a more descriptive name for the file, best to include core metadata like name of saleperson and company
with open("sales_call_transcript.txt", "w") as f:
    f.write(response.text)
