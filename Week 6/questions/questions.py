import nltk
import sys
import os
import string
from nltk.tokenize import word_tokenize
import numpy as np

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = {}

    for filename in os.listdir(directory):

        f = os.path.join(directory, filename)

        if os.path.isfile(f):
            
            text = open(f, "r")
            files[filename] = text.read()

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens = word_tokenize(document.lower())

    words = []
    for token in tokens:
        if token not in string.punctuation and token not in nltk.corpus.stopwords.words("english"):
            words.append(token)

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    total_num_docs = len(documents)

    idfs = {}

    for doc in documents:
        for word in documents[doc]:
            if word not in idfs:
                idfs[word] = 0

    for doc in documents:
        for word in idfs:
            if word in documents[doc]:
                idfs[word] += 1

    for word in idfs:
        idfs[word] = np.log(total_num_docs / idfs[word])

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    files_idfs = {}

    for filename, filecontent in files.items():

        total_tf_idf = 0
        for word in query:
            total_tf_idf += filecontent.count(word) * idfs[word]

        files_idfs[filename] = total_tf_idf

    top_files = [n for (n,c) in sorted(files_idfs.items(), key=lambda x: x[1], reverse=True)]

    return top_files[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_idfs = {}

    for sent, sent_content in sentences.items():

        total_idf = 0
        word_count = 0

        for word in query:
            if word in sent_content:
                total_idf += idfs[word]
                word_count += 1

        density = word_count / len(sent_content)

        sentence_idfs[sent] = (total_idf, density)

    top_sentences = [n for (n,c) in sorted(sentence_idfs.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)]
    
    return top_sentences[:n]

if __name__ == "__main__":
    main()
