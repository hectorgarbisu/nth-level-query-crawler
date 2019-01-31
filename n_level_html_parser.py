# n level parser
from urllib.request import urlopen, urljoin
from urllib.parse import urlparse
from bs4 import BeautifulSoup


"""
returns: a tree of links
[link1, link2, link3]
link1 = (text, url, [link1_1, link1_2, link1_3, ... ])
link1_1 = (text, url, [link1_1_1, link1_1_2, link1_1_3, ... ])
...

return is as a generator object, each new level of depth is also a generator

an optional list of queries can be passed as argument
query examples (https://stackoverflow.com/questions/24801548/how-to-use-css-selectors-to-retrieve-specific-links-lying-in-some-class-using-be):

soup.select('div')
All elements named <div>

soup.select('#author')
The element with an id attribute of author

soup.select('.notice')
All elements that use a CSS class attribute named notice

soup.select('div span')
All elements named <span> that are within an element named <div>

soup.select('div > span')
All elements named <span> that are directly within an element named <div>, with no other element in between

soup.select('input[name]')
All elements named <input> that have a name attribute with any value

soup.select('input[type="button"]')
All elements named <input> that have an attribute named type with value button

the default query for all levels is a["href"] (all links)
"""


def tree_of_links(url = '', numlevels=1, queries=['a[href]']):
    parsed_uri = urlparse(url)
    base_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

    """ in case a url is inaccesible """
    try:
        page = urlopen(url)
    except:
        return []

    """ the default query is any link """
    if queries:
        query, *remaining_queries = queries
    else:
        query = 'a[href]'
        remaining_queries = None
    
    soup = BeautifulSoup(page, 'html.parser')
    findings = soup.select(query)
    
    """ [(link_text, link_url), ...] """
    tuples = ((anchor.text, urljoin(base_url, anchor['href']) ) for anchor in findings)

    if numlevels<2 :
        return tuples
    else:
        return ((
                    link_text,
                    link_url, 
                    tree_of_links(link_url, numlevels - 1, remaining_queries)
                )
        for link_text, link_url in tuples)

def in_depth_print(tree_of_links):
    if tree_of_links:
        for name, url, *subtree in tree_of_links:
            if subtree:
                in_depth_print(subtree)
            print(name, url)

def link_tree_to_csv(tree_of_links, parent_prefix = ''):
    for name, url, *subtree in tree_of_links:
        if parent_prefix:
            new_prefix = f'{parent_prefix},{name}'
        else:
            new_prefix = name
        yield f'{new_prefix},{url}'
        if subtree:
            yield from link_tree_to_csv(subtree[0], parent_prefix = new_prefix)

def test():
    link_tree = tree_of_links("https://es.wikipedia.org/wiki/Wikipedia:Portada",
    2,
    [
        'div.main-wrapper a[href]',
        'div#bodyContent a[href]',
    ])

    in_depth_print(link_tree)
    
    for csv_line in link_tree_to_csv(link_tree):
        print(csv_line)


if __name__=="__main__":
    test()



