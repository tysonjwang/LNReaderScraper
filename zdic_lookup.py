import requests
from lxml import html


def get_page(word):
    url = 'https://www.mdbg.net/chinese/dictionary?page=worddict&wdrst=0&wdqb={}'.format(word)
    webpage = requests.get(url)
    try:
        webpage.raise_for_status()
    except:
        return 'An Error Occured'
        return None
    if 'No results found searching for' in webpage.text:
        return 'No Definition Found'
    else:
        webtree = html.fromstring(webpage.content)
        for definition in webtree.xpath('//div[@class="defs"]/text()'):
            return definition


if __name__ == '__main__':
    while True:
        word = input('Enter a word')
        get_page(word)
