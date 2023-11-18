import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text = "Today, the world is the world of information and telecommunication. Everyday new technology and inventions are being made in the area of information, processing, and travelling. There is hardly any area which had not been affected by this. Due to all this, the word distance sounds ironic in the present day context."

def summarizer(rawdocs):
    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')  # Corrected the model name
    doc = nlp(rawdocs)

    tokens = [token.text for token in doc]
    
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    max_freq = max(word_freq.values())

    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq

    sent_tokens = [sent for sent in doc.sents]

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]  # Corrected the addition logic
                else:
                    sent_scores[sent] += word_freq[word.text]

    select_len = int(len(sent_tokens) * 0.3)
    summary = nlargest(select_len, sent_scores, key=sent_scores.get)  # Corrected 'keys' to 'key'

    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)

    return summary, doc, len(tokens), len(final_summary)  # Corrected variable names and added missing variables

# Call the function
summary, docs, len_rawdocs, len_summary = summarizer(text)

#print("Original text:", text)
#print("Summary:", summary)
#print("Length of original text:", len_rawdocs)
#print("Length of summary text:", len_summary)
