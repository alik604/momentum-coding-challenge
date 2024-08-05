import argparse
import os

import google.generativeai as genai

from utils.data_reader import read_transcript

parser = argparse.ArgumentParser(description='CLI Argument Parser')
parser.add_argument('--transcript', type=str, help='File name with .txt extension of the sales call transcript',
                    default="sales_call_transcript.txt")
args = parser.parse_args()

transcript = read_transcript(args.transcript)
# print(transcript)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "<your API key if not set as env var>"))

model = genai.GenerativeModel(model_name='gemini-1.5-flash', system_instruction="""You are an assistant working sales and customer calls,
                                you transform transcripts into customer intelligence.
                                Yours goals are to forecast, assess churn risk,
                                update Salesforce, share product feedback,
                                and bring insights to your the team.
                                
                                Our salesperson is named Satya and our comapny is Nvdia."""
                              # TODO hardcoded is a bad idea if we get some other input. But I want this here for demoing purposes
                              )

response = model.generate_content(transcript)
print(response.text)
