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
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

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
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # store each page to the probability distribution with initial probability of 0.
    distribution = {}
    for pg in corpus:
        distribution[pg] = 0


    for pg in corpus:

        # using damping factor
        if pg == page:

            # page has no outgoing links
            if not corpus[pg]:
                for p in distribution:
                    distribution[p] = 1 / len(corpus)
                return distribution

            # page has outgoing links
            for p in corpus[pg]:
                distribution[p] += (damping_factor / len(corpus[pg])) 

        # using 1 - damping factor
        distribution[pg] += ((1 - damping_factor) / len(corpus))

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    rankings = {}
    for page in corpus:
        rankings[page] = 0

    # first page chosen at random
    first_page = random.choice(list(corpus.keys()))

    # add to rankings
    rankings[first_page] += 1 / SAMPLES

    # probability distribution for the next page
    distr = transition_model(corpus, first_page, damping_factor)
    
    for i in range(n-1):

        # list of pages
        pages = list(distr)

        # list of each pages' probabilities
        probabilities = list(distr.values())

        # randomly choose the next page based on probabilities
        next_page = random.choices(pages, weights=probabilities)[0]

        rankings[next_page] += 1 / SAMPLES

        distr = transition_model(corpus, next_page, damping_factor)
        
    return rankings


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rankings = {}

    # PageRank for all pages is initially 1/N 
    for page in corpus:
        rankings[page] = 1 / len(corpus)


    while True: 
        count = 0
        for key in corpus: 
            sigma = 0

            for page in corpus:
                if key in corpus[page]:
                    sigma += rankings[page] / len(corpus[page])

            rank = (1 - damping_factor) / len(corpus) + damping_factor * sigma

            # check if rank value changes by less than 0.001
            if abs(rankings[key] - rank) < 0.0005:
                count += 1

            rankings[key] = rank

        if count == len(corpus):
            break

    return rankings


if __name__ == "__main__":
    main()

















