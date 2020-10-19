import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP | VP | NP VP | VP NP | S Conj S

AP -> Adj | Adj AP
NP -> N | Det N | Det AP N | NP PP  
PP -> P NP 
VP -> V | V NP | V PP | Adv VP | VP Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    # Returns a token list by using list comprehension to:
    # Go through a list created by using nltk's word_tokenize function in a lowered version of the sentence;
    # Retrieve any words that at least contains one alphabetical character.
    # https://www.nltk.org/api/nltk.html#nltk.tree.Tree.subtrees
    # https://www.nltk.org/api/nltk.tokenize.html#nltk.tokenize.punkt.PunktLanguageVars.word_tokenize
    return [word for word in nltk.word_tokenize(sentence.lower()) if any(character.isalpha() for character in word)]


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """

    # Returns a list of all noun phrases chunks in the sentence tree by:
    # Using list comprehension to retrieve all parents of all the nouns in a ParentedTree version of the tree; 
    # ParentedTree is a subclass of Tree that automatically maintains parent pointers for single-parented trees; 
    # So we use the function nltk.tree.ParentedTree.convert(tree) to convert the input tree into a ParentedTree; 
    # This way, we can use the parent() method to create a list of all the parents of each noun in the sentence and return this list.
    # https://www.nltk.org/api/nltk.html#nltk.tree.ParentedTree
    # https://www.nltk.org/api/nltk.html#nltk.tree.ImmutableProbabilisticTree.convert
    return [nouns.parent() for nouns in nltk.tree.ParentedTree.convert(tree).subtrees(lambda subtree: subtree.label() == "N")]


if __name__ == "__main__":
    main()
