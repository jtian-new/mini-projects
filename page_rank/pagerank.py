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
    print(corpus)
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
    prob_dict = {}
    total_pages = len(corpus)
    num_links = len(corpus[page])
    
    if num_links == 0:
        for i in corpus.keys():
            prob_dict[i] = 1/total_pages
    else:
        for i in corpus.keys():
            if i in corpus[page]:
                prob_dict[i] = (1-damping_factor)/total_pages + + damping_factor/num_links
            else:
                prob_dict[i] = (1-damping_factor)/total_pages 
    
    return prob_dict

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    total_pages = len(corpus)
    prob = {}
    sample_dist = {}
    
    for p in corpus.keys():
        prob[p] = 1/total_pages
        sample_dist[p] = 0
    
    for i in range(0,n):
        current_page = random.choices(list(corpus.keys()), weights=list(prob.values()))[0]
        sample_dist[current_page] += 1
        prob = transition_model(corpus, current_page, damping_factor)
    
    for k in sample_dist.keys():
        sample_dist[k] = sample_dist[k]/n
        
    return sample_dist


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    new_prob = {}
    prev_prob = {}
    total_pages = len(corpus)
    max_diff = 0.0011
    
    for p in corpus.keys():
        prev_prob[p] = -1
        new_prob[p] = 1/total_pages

    while max_diff > 0.001:
        prev_prob = new_prob.copy()
        max_diff = 0
        for p in corpus.keys():
            sum_pri = 0 
            for i in corpus.keys():
                if len(corpus[i]) == 0:
                    sum_pri += prev_prob[i]/total_pages
                    continue
                if p in corpus[i]:
                    sum_pri += prev_prob[i]/len(corpus[i])
                    
            new_prob[p] = (1-damping_factor)/total_pages + damping_factor*sum_pri
            
            max_diff = max(max_diff, abs(new_prob[p]-prev_prob[p]))     

    return new_prob


if __name__ == "__main__":
    main()
