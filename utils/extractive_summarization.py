'''
I have a back ground in Data Science & Machine Learning for Sequential Data (Financial forcating, Text ("NLP"), EEG signal ("BioMed signal processing")).
One way to save costs is to use textRank to summarize large documents. This is Extractive summarization, It can miss information/context, but it is NOT generative and hence does not hallucinations. (Think of a unethical news reporter cherry picking- Thats the worse case scenario for extractive summarization)

Conversly, Abstractive summarization (Transformers, as in the T in GPT) are generative and can hallucinate information. The risk of error is multiplitive in nature (expontial)!!! 

https://www.geeksforgeeks.org/text-summarization-in-nlp/
https://spacy.io/universe/project/spacy-pytextrank

---
Another way is to project text to an Embedding Space (GloVe), use cosine similarity to find the most similar sentences (weights between sentances), and plug this into NetworkX to make it into a Graph and run pageRank.
https://github.com/agc-shubham/Text-Summarization/blob/main/TestRank_Text_Summarization.ipynb

ive done this type of work in 2 Jobs + when I was a mentor / team-lead at Vancouver Datajam 2023

'''

import spacy
import pytextrank
# Caution: import pytextrank must be above. Autoformatter will remove it. https://github.com/DerwenAI/pytextrank/issues/148#issuecomment-811103712

def extractive_summarization(file_name: str = 'customerDocuments/design_doc.txt'):
    nlp = spacy.load("en_core_web_sm")  # or en_core_web_lg
    nlp.add_pipe("textrank")

    # we can use biasedtextrank to have the summerization be biased towards a specific word/topic. This can be a summarization, or useful to remove irrelevant information.

    # Works best on a big blob of text. Works worse on texts that is headings-heavy (ie, my sample text from the file)
    example_text = """My day is doing very good. Thanks for Asking! Deep learning (also known as deep structured learning) is part of a
    broader family of machine learning methods based on artificial neural networks with 
    representation learning. Learning can be supervised, semi-supervised or unsupervised. 
    Deep-learning architectures such as deep neural networks, deep belief networks, deep reinforcement learning, 
    recurrent neural networks and convolutional neural networks have been applied to
    fields including computer vision, speech recognition, natural language processing, 
    machine translation, bioinformatics, drug design, medical image analysis, material
    inspection and board game programs, where they have produced results comparable to 
    and in some cases surpassing human expert performance. Artificial neural networks
    (ANNs) were inspired by information processing and distributed communication nodes
    in biological systems. ANNs have various differences from biological brains. Specifically, 
    neural networks tend to be static and symbolic, while the biological brain of most living organisms
    is dynamic (plastic) and analogue. The adjective "deep" in deep learning refers to the use of multiple
    layers in the network. Early work showed that a linear perceptron cannot be a universal classifier, 
    but that a network with a nonpolynomial activation function with one hidden layer of unbounded width can.
    Deep learning is a modern variation which is concerned with an unbounded number of layers of bounded size, 
    which permits practical application and optimized implementation, while retaining theoretical universality 
    under mild conditions. In deep learning the layers are also permitted to be heterogeneous and to deviate widely 
    from biologically informed connectionist models, for the sake of efficiency, trainability and understandability, 
    whence the structured part."""

    # import text from file
    with open(file_name, 'r') as file:
        example_text = file.read()

    doc = nlp(example_text)

    # docs arnt showing in VS code. https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L797
    # limit_sentences means how many sentences to include in the summary
    sentences = example_text.replace('..', '.').replace('..', '.').count('.')
    print('sentences:', sentences)
    wanted_sentences = sentences
    if wanted_sentences > 3:
        wanted_sentences = wanted_sentences // 3
    wanted_sentences = min(wanted_sentences, 10)
    print('wanted sentences:', wanted_sentences)

    summary = ""
    count = 0
    for i, sentence in enumerate(
            doc._.textrank.summary(limit_phrases=10, limit_sentences=wanted_sentences, preserve_order=True)):
        char_count = sum(len(x) for x in sentence)
        count += char_count

        # print(f'[Summary] part {i+1}/{wanted_sentences} Length: {char_count}:')
        # print(str(sentence) + '\n')
        summary += str(sentence) + '\n'

    print('Original Document Size:', len(example_text))
    print(f'Summarized Document Size: {count}')

    return summary


if __name__ == '__main__':
    print(extractive_summarization())
