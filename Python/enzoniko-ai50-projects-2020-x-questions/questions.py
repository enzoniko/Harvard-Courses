import nltk
import os
import sys
import string
import math

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
    sentences = {}
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                if tokens := tokenize(sentence):
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

    # Returns a dictionary mapping the filename of each '.txt' file inside that directory to the file's contents as a string by:
    # Using dictionary comprehension where the keys are the filename and the values are the read version of the opened file.
    return {filename: (open(os.path.join(directory, filename), "r", encoding="UTF8").read()) for filename in os.listdir(directory)}

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords. 
    """

    # Returns a list of all of the words in the document, in order by:
    # Using list comprehension to create a list of words from the tokens of a lowered version of the document where the words are not punctuations or stopwords.
    return [word for word in nltk.word_tokenize(document.lower()) if word not in string.punctuation and word not in nltk.corpus.stopwords.words("english")]

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    # Returns a dictionary that maps words to their IDF values by:
    # Using list comprehension to get all the words;
    # Using dictionary comprehension to create a dictionary where all the words are mapped to their IDF values.
    return {
        word: math.log(
            len(documents)
            / sum(word in documents[filename] for filename in documents)
        )
        for word in {
            word for file in list(documents.values()) for word in file
        }
    }


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
   
    # Returns a list of the filenames of the 'n' top files that match the query, ranked according to tf-idf by:
    # Creating a zip object where the first iterable correspond to a list with each filename (made by using list comprehension) and the second iterable correspond to a list of the tf-idf values for each file (made by Using list comprehension to create a list of the summed tf-idf values for each word in the query, for each file); 
    # Sorting this zip object by the tf-idf values (index number 1 of the tuples) in descending order;
    # Using list comprehension to get only the keys of the sorted zip object and slicing the list at the n element with "[:n]".
    return [
        key
        for key, value in sorted(
            zip(
                list(files),
                [
                    sum(
                        files[file].count(word) + idfs[word]
                        if word in idfs
                        else files[file].count(word)
                        for word in query
                    )
                    for file in files
                ],
            ),
            key=lambda item: item[1],
            reverse=True,
        )
    ][:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    # Returns a list of the 'n' top sentences that match the query, ranked according to idf, if there are ties, preference should be given to sentences that have a higher query term density by:
    # Creating a zip object where the first iterable corresponds to a list with each sentence (made by using list comprehension), the second iterable corresponds to a list of the idf values for each sentence (made by using list comprehension to create a list of the summed idf values for each word in the query, for each sentence) and the third iterable corresponds to a list of the term density for each sentence (made by using list comprehension to get the proportion of words in the sentence that are also words in the query, for each sentence); 
    # Sorting this zip object by the idf values (index number 1 of the tuples) and the term density values (index number 2 of the tuples) in descending order;
    # Using list comprehension to get only the first elements (index number 0 of the tuples) of the sorted zip object and slicing the list at the n element with "[:n]".
    return [
        value[0]
        for value in sorted(
            zip(
                list(sentences),
                [
                    sum(
                        (idfs[word]) if word in idfs else 0
                        for word in query
                        if word in sentences[sentence]
                    )
                    for sentence in sentences
                ],
                [
                    sum(word in query for word in sentences[sentence])
                    / len(sentences[sentence])
                    for sentence in sentences
                ],
            ),
            key=lambda item: (item[1], item[2]),
            reverse=True,
        )
    ][:n]


if __name__ == "__main__":
    main()
