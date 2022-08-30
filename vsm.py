
import glob
import math
import re
import sys
from collections import defaultdict
from functools import reduce

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

STOPWORDS = set(stopwords.words("english"))
CORPUS = "corpus/*"

# Each document has an id, and these are the keys in the following dict.
# The values are the corresponding filenames.
document_filenames = dict()

# The size of the corpus
N = 0

# vocabulary: a set to contain all unique terms (i.e. words) in the corpus
vocabulary = set()

postings = defaultdict(dict)

document_frequency = defaultdict(int)

length = defaultdict(float)


def main():
    # Get details about corpus
    get_corpus()

    # Initialise terms and postings for the corpus
    initialize_terms_and_postings()

    # Set document frequencies for all terms
    initialize_document_frequencies()

    # Set document vector lengths
    initialize_lengths()

    # Allow for search
    while True:

        # Retrieve sorted list of ranked documents
        scores = do_search()

        # Print the results in tabular format
        print_scores(scores)


def get_corpus():
    global document_filenames, N

    # Fetch list of document names in corpus
    documents = glob.glob(CORPUS)

    # Set size of corpus
    N = len(documents)

    # Dictionary having doc id as key and document name as value
    document_filenames = dict(zip(range(N), documents))


def initialize_terms_and_postings():
    """Reads in each document in document_filenames, splits it into a
    list of terms (i.e., tokenizes it)
    """
    global vocabulary, postings
    for id in document_filenames:

        # Read the document
        with open(document_filenames[id], "r") as f:
            document = f.read()

        # Remove all special characters from the document
        document = remove_special_characters(document)

        # Remove digits from the document
        document = remove_digits(document)

        # Tokenize the document
        terms = tokenize(document)

        # Remove duplicates from the terms
        unique_terms = set(terms)

        # Add unique terms to the vocabulary
        vocabulary = vocabulary.union(unique_terms)

        # For every unique term
        for term in unique_terms:

            # The value is the frequency of the term in the document
            postings[term][id] = terms.count(term)


def tokenize(document):

    # Tokenize text into terms
    terms = word_tokenize(document)

    # Remove stopwords and convert remaining terms to lowercase
    terms = [term.lower() for term in terms if term not in STOPWORDS]

    return terms


def initialize_document_frequencies():

    global document_frequency
    for term in vocabulary:
        document_frequency[term] = len(postings[term])


def initialize_lengths():
    """ Computes the length for each document """
    global length
    for id in document_filenames:
        l = 0
        for term in vocabulary:
            l += term_frequency(term, id) ** 2
        length[id] = math.sqrt(l)


def term_frequency(term, id):

    if id in postings[term]:
        return postings[term][id]
    else:
        return 0.0


def inverse_document_frequency(term):

    if term in vocabulary:
        return math.log(N / document_frequency[term], 2)
    else:
        return 0.0


def print_scores(scores):

    print("-" * 42)
    print("| %s | %-30s |" % ("Score", "Document"))
    print("-" * 42)

    for (id, score) in scores:
        if score != 0.0:
            print("| %s | %-30s |" % (str(score)[:5], document_filenames[id]))

    print("-" * 42, end="\n\n")


def do_search():

    query = tokenize(input("Search query >> "))

    # Exit if query is empty
    if query == []:
        sys.exit()

    scores = sorted(
        [(id, similarity(query, id)) for id in range(N)],
        key=lambda x: x[1],
        reverse=True,
    )

    return scores


def intersection(sets):

    return reduce(set.intersection, [s for s in sets])


def similarity(query, id):

    similarity = 0.0

    for term in query:

        if term in vocabulary:

            # For every term in query which is also in vocabulary,
            # calculate tf-idf score of the term and add to similarity
            similarity += term_frequency(term, id) * inverse_document_frequency(term)

    similarity = similarity / length[id]

    return similarity


def remove_special_characters(text):
    regex = re.compile(r"[^a-zA-Z0-9\s]")
    return re.sub(regex, "", text)


def remove_digits(text):
    regex = re.compile(r"\d")
    return re.sub(regex, "", text)


if __name__ == "__main__":
    main()