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

Set an os variable `GEMINI_API_KEY` with the API key

### Run the scripts

The project is 3 separate scripts, I kept the files basic

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
   a greater context (Hardcoded for the POC stage)
    2. This is currently hardcoded and wont stand up to different input data

## Supplemental features:

1. Extractive summarization of a document provided as a .txt file
    1. In real life, Slack & Gmail messages have additional docs for background context
    2. Attaching a PDF and sending it straight to the model is trivial
2. Persist chat history between user questions and AI responses to a database
    1. Partially implemented, the chat history is stored as a pickle. The (list) object gets read correctly, but the API isn't happy with it.
       At first, I suspected an object type that's proprietary to the API's package, then after using Pickle (despite the security risk), a potential object type change should be a non-issue.
       I don't see why it doesn't work. https://stackoverflow.com/a/25465148/5728614 see ("Chat
       conversations")[https://ai.google.dev/gemini-api/docs/get-started/tutorial?lang=python]
    3. I know when a bug takes 5 mins or a lot more, this is the latter case. So rather cut loses 20 mins

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

> The generated design doc is for the "InnovateX 5000 GPU". The customer never asked for this specific GPU, but thats a model-side issue. And on me for not making the design doc and text line up. I should have generated a better conversation in part1 by adding the design doc to the "System"


## Potential features:

1. Can send Gemini a PDF of a design doc. This will add more code without showing my abilities as any greater, which
   is why I did the text-based equivalent with the extractive summarization (shows I know NLP- I was a Data Scientist
   before)
2. I was planning on making a docker file
    1. Benefits
        1. **Docker Scout (host level security)**
        2. Portability
        3. Easy to deploy
    2. Cons
        1. Not sure which port I need to expose for the API call. Seems to be port 443
        2. Docker is broken on my local Windows, the fix for a few weeks back isn't working. Normally I'd code on my work Mac
3. **Add SAST & DAST (application level security)**
    1. ie, Bandit
    2. Regardless of having it in the CI/CD, the first step is having it as part of local testing (just like
       PyLint/Black/Flake8)
4. Use Latent Dirichlet Allocation (LDA) to show the various topic the chat. Use NLTK & Gensim.
    1. Can make a nice-ish word cloud with the topics as a visual representation
        1. Get
           topics: https://towardsdatascience.com/nlp-extracting-the-main-topics-from-your-dataset-using-lda-in-minutes-21486f5aa925 & https://stackoverflow.com/questions/59354365/how-to-extract-topics-from-existing-text-clusters
        2. Make word cloud: https://medium.com/@harinisureshla/wordclouds-basics-of-nlp-5b60be226414

## AI usage
I didn't use much AI beyond standard IntelliSense. It kept making up object properties. The only AI code was for reading/writing a txt file because I didn't memorize the context handler syntax   
