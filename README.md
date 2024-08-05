# A basic AI chatbot for sales calls

## Running

### Create a virtual environment

`python -m venv momentum`

### Activate the virtual environment

`.\momentum\Scripts\activate`

### Install the required packages

`pip install -r requirements.txt`

The following is required for the extractive summarization feature. Cautions this is over 500mb

`python -m spacy download en_core_web_sm`

### Set key

To get the key here: https://aistudio.google.com/app/apikey

Set a os variable `GEMINI_API_KEY` with the API key

### Run the scripts

Project is 3 separate scripts, I kept the files basic

1. `python part1.py`
2. `python part2.py --transcript "sales_call_transcript.txt"`
3. `python part3.py --transcript "sales_call_transcript.txt" --question "What product was the customer interested in?"`

For Part3.py, the following are the optional arguments. All have a default value for testing convenience.

```
optional arguments:
  -h, --help            show this help message and exit
  --transcript TRANSCRIPT
                        File name with .txt extension of the sales call transcript
  --question QUESTION   Your question (prompt)
  --persist_chat_history PERSIST_CHAT_HISTORY
                        Use chat history
  --session_id SESSION_ID
                        Tracker session for chat persistence
  --include_background_context INCLUDE_BACKGROUND_CONTEXT
                        Include background context
  --background_context_file_name BACKGROUND_CONTEXT_FILE_NAME
                        Background context file name
```

## Design decisions

For Part2,

1. I think removing the time stamps & company name gives better results while reducing cost

For Part 2 & 3
1. Need to Improve System_instruction: It should mention the name of the salesperson and our company, so the model has
   greater context (Hardcoded for POC stage)
    2. This is currently hardcoded and wont stand up to different input data

## Supplemental features:

1. Extractive summarization of a document provided as a .txt file
    1. In real life, Slack & Gmail messages have additional docs for background context
    2. Attaching a pdf and sending straight to the model is trivial
2. Persist chat history between user questions and AI responses to a database
    1. Partially implemented, the chat history is stored as a pickle. I get an error is reading. At first I suspected in
       a proprietary obj type, but using Pickle (despite the security risk), should be sorting it as the original object
       type. I don't see why it doesn't work. https://stackoverflow.com/a/25465148/5728614 see ("Chat
       conversations")[https://ai.google.dev/gemini-api/docs/get-started/tutorial?lang=python]
    2. I know when a bug takes 5 mins or a lot more, this is the latter case. So rather cut loses 20 mins
3. PyLint on main 3 files

Without extractive summarization being sent to System

```
The customer, Sam, was interested in purchasing **GPUs (Graphics Processing Units)** from Nvidia. 
```

With extractive summarization being sent to System

```
sentences: 115
wanted sentences: 10
Original Document Size: 13586
Summarized Document Size: 2538
The customer, Sam, was interested in the **InnovateX 5000 GPU**. He requested a large quantity (10,000) of these GPUs for his project. 
```

> The generated design doc is for the "InnovateX 5000 GPU". The customer never asked for this specific GPU, but thats a
> issue on the model side.


Potential features:

1. Can send gemini a PDF of a design doc. This is will add more code without showing my abilities as any greater, which
   is why I did the text based equivalent with the extractive summarization (shows I know NLP.. I was a data Scientist
   before)
2. I was planed on making a docker file
    1. Benefits
        1. **Docker Scout (host level security)**
        2. Portability
        3. Easy to deploy
    2. Cons
        1. Not sure which port I need to expose for the API call. Seems to be 443
        2. My local windows install is broken. Normally I'd code on my work Mac
3. **Add SAST & DAST (application level security)**
    1. ie, Bandit
    2. Regardless of having it in the CI/CD, first step is having it as part of local testing (just like
       PyLint/Black/Flake8)
4. Use Latent Dirichlet Allocation (LDA) to show the various topic the chat. Use NLTK & Gensim.
    1. Can make a nice-ish word cloud with the topics as a visual representation
        1. Get
           topics: https://towardsdatascience.com/nlp-extracting-the-main-topics-from-your-dataset-using-lda-in-minutes-21486f5aa925 & https://stackoverflow.com/questions/59354365/how-to-extract-topics-from-existing-text-clusters
        2. Make word cloud: https://medium.com/@harinisureshla/wordclouds-basics-of-nlp-5b60be226414