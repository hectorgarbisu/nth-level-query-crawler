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

    def visit_children(url, visited_links=set(), level=1):
        if level > 4:
            return visited_links
        new_links = useful_links(url)
        prev_links = visited_links
        visited_links = {*visited_links, *new_links}
        print(len(visited_links), level, url)
        for link in new_links:
            if link not in prev_links:
                visited_links = visit_children(link, visited_links, level+1)
        return visited_links

    return visit_children(root)

if __name__=='__main__':
    urls = get_urls()

    with open('urls3.txt', 'w+') as file:
        for url in urls:
            file.write(f'{url}\n')