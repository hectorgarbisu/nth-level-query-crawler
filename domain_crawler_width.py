from urllib.request import urlopen, urljoin
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def get_urls():
    root = 'https://support.google.com/a#topic=7570177'
    root_domain = 'https://support.google.com/a/'
            
    def url_no_params(url):
        return '{p.scheme}://{p.netloc}{p.path}'.format(p = urlparse(url))

    def useful_links(url):
        parsed_uri = urlparse(url)
        base_url = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        try:
            page = urlopen(url)
        except:
            return []
        query = '.main-content a[href]'
        soup = BeautifulSoup(page, 'html.parser')
        findings = soup.select(query)
        links = {url_no_params(urljoin(base_url, anchor['href'])) for anchor in findings}
        return {link for link in links if link.startswith(root_domain)}
    
    # New bag for each level. The oldest bag carries all 'expanded' nodes.
    # Expanding a node removes it from available_links and puts all its children in available_links.
    # Available links are nodes ready to be expanded
    def expand(explored_links=set(), available_links=set()):
        level_links = set()
        for url in available_links:
            if url not in explored_links:
                for new_url in useful_links(url):
                    if new_url not in available_links:
                        level_links.add(new_url)
                explored_links.add(url)
        return explored_links, level_links

    explored, available = set(), {root}
    level = 0
    while available != set():
        print(level, len(explored), len(available))
        explored, available = expand(explored, available)
        level += 1
    return explored

if __name__=='__main__':
    urls = get_urls()

    with open('urls4.txt', 'w+') as file:
        for url in urls:
            file.write(f'{url}\n')