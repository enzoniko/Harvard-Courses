import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print("PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = {}

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = {link for link in pages[filename] if link in pages}


    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # Get all links that are linked to by the current page
    linked_pages = corpus[page]

    # New dictionary
    probability_random_visit = {}

    # For each page in the corpus create a key in the new dictionary and assign it a value
    for page in corpus:

        # If the page is one of the linked pages
        if page in linked_pages:

            # The value is going to be the damping factor divided by the number of linked pages plus,
            # 1 minus the damping factor divided by the number of pages in the corpus
            probability_random_visit[page] = round(damping_factor / len(linked_pages) + (1 - damping_factor) / len(corpus), 5)

        # If the page isn't one of the linked pages
        if page not in linked_pages:

            # The value is going to be 1 minus the damping factor divided by the number of pages in the corpus
            probability_random_visit[page] = round((1 - damping_factor) / len(corpus), 5)

    # Returns the dictionary
    return probability_random_visit
    
def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # The page we are checking, start with a page at random
    page = random.choice(list(corpus.keys()))

    samples = [page]
    # Do a loop over the number of samples we want, it starts with zero so it is n - 1
    for _ in range(n - 1):
        # Probabilities for the next page given the current page to the transition model
        probability_distribution_for_page = transition_model(corpus, page, damping_factor)

        # Get the next page using the probabilities from the transition model
        # Random.choice returns a k sized list of elements chosen from the keys of the probabilities above
        # If a weights sequence is specified, selections are made according to the relative weights, here the weight sequence is the values from the probabilities above
        # The pop() method removes the item at the given index from the list and returns the removed item.
        page = random.choices(list(probability_distribution_for_page.keys()), weights = list(probability_distribution_for_page.values()), k = 1).pop()

        # Append the new page to the samples list
        samples.append(page)

    # Returns the page ranks
    return {key: samples.count(key) / n for key in corpus.keys()}

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Page ranks dictionary
    pageRanks = {
        page: 1 / len(list(corpus.keys())) for page in list(corpus.keys())
    }


    # Converged starts as false
    converged = False

    # Loop while converged is false
    while not converged:

        # Get the previous page ranks
        previous_page_ranks = dict(pageRanks)

        # Initialize a list with the page ranks difference
        page_ranks_difference = []

        # For each page in the corpus
        for sub_page in list(corpus.keys()):

            # Start with a partial probability for this page
            # This partial probability is the second part of the background formula
            # For the second condition, we need to consider each possible page i that links to page p. 
            # For each of those incoming pages, let NumLinks(i) be the number of links on page i. 
            # Each page i that links to p has its own PageRank, PR(i), representing the probability that we are on page i at any given time. 
            # And since from page i we travel to any of that page’s links with equal probability, we divide PR(i) by the number of links NumLinks(i) to get the probability that we were on page i and chose the link to page p.
            partial_probabilities = 0

            # For each page in the corpus again
            for super_page in list(corpus.keys()):

                # But this time only if we are checking different pages
                if super_page != sub_page:

                    # If the sub page is one of the links from the super page
                    # With probability d, the surfer followed a link from a page i to page p.
                    if sub_page in corpus[super_page]:

                        # Add in the partial probabilities var the previous page rank for the super page divided by the number of links the super page contains
                        partial_probabilities += previous_page_ranks[super_page] / len(corpus[super_page])

                    # If the number of links from the super page is zero 
                    # With probability 1 - d, the surfer chose a page at random and ended up on page p.
                    elif len(corpus[super_page]) == 0:

                        # Add to the partial probabilities var 1 divided by the number of pages
                        partial_probabilities += 1 / len(corpus.keys())

            # Create a key in the page ranks dictionary with the name of the super page and the result of the formula as the value
            # Formula: PAGE_RANK(PAGE) = 1 - DAMPING_FACTOR / NUMBER OF PAGES + DAMPING_FACTOR * partial_probabilities
            pageRanks[sub_page] = (1 - damping_factor) / len(corpus.keys()) + (damping_factor * partial_probabilities)

            # Appends the difference between the previous and the current page rank for the sub page to the page ranks difference list
            page_ranks_difference.append(abs(previous_page_ranks[sub_page] - pageRanks[sub_page]))

        # For each value in the page ranks difference list
        for value in page_ranks_difference:

            # If the value is less than or equal to 0.001
            if value <= 0.001:

                # The values converged
                converged = True

    # Returns the page ranks
    return pageRanks

if __name__ == "__main__":
    main()
