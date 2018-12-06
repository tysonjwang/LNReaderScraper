#! usr/bin/python3
from concurrent.futures import ThreadPoolExecutor
from lxml import html
import requests
from opencc import OpenCC
import os
# %%

# This is the main file, defines the Qt Window, etc.


def process_chapter(base_url, chap_name, rel_url, index, completed, remaining):
    if chap_name in completed:
        print("{} Already Completed, Skipping.".format(chap_name))
        return remaining
    url = base_url[:-5] + '/' + os.path.basename(rel_url)
    print(url)
    chap_get = requests.get(url)
    try:
        chap_get.raise_for_status()
        chap = html.fromstring(chap_get.content)
        chap_text = chap.xpath('//div[@id="contents"]/text()')
        print(len(chap_text))
        full = chap_name + '\n' + '\n'.join(map(str.strip, chap_text)) + '\n'
        full = openCC.convert(full)
        with open('novelchapter{}.txt'.format(index), 'w') as file:
            file.write(full)
        print("Finished: {}".format(chap_name))
        completed.add(chap_name)
        return remaining - 1
    except Exception as exc:
        print('Chapter: {} was not gotten due to error {}'.format(chap_name,
                                                                  exc))
        return remaining
# %%


def find_url_from_name(name):
    try:
        requests.get(name)
        return name
    except requests.exceptions.MissingSchema:
        search_get = requests.get('https://www.ztjxsw.cn/class/all.html?keyword='
                                  + name)
        search = html.fromstring(search_get.content)
        url = search.xpath("//a[text()='{}']/@href".format(name))
        if len(url) == 0:
            print('Novel Not Found!')
            return None
        else:
            return 'https://www.ztjxsw.cn' + url[0]

openCC = OpenCC('custom')

def main(url, remaining):
    # Make sure the chapter url is from ztjxsw.cn
    # pool = ThreadPoolExecutor(max_workers=10)
    os.chdir('novels')
    homepage = find_url_from_name(url)
    if homepage is None:
        return None
    homepage_get = requests.get(homepage)
    homepage_get.raise_for_status()
    hometree = html.fromstring(homepage_get.content)
    novel_name = hometree.xpath('//h1/text()')[0]
    if novel_name not in os.listdir('.'):
        os.mkdir(novel_name)
    os.chdir(novel_name)
    # os.chdir('novels')
    # os.mkdir('{}'.format(novel_name))
    # os.chdir('./{}'.format(novel_name))
    chapter_names = hometree.xpath('//div[@class="body "]/ul/li/a/text()')
    chapter_urls = hometree.xpath('//div[@class="body "]/ul/li/a/@href')
    try:
        completed = open('index', 'r').read()
        completed = set(completed.splitlines())
    except FileNotFoundError:
        completed = set()
    for index, (url, name) in enumerate(zip(chapter_urls, chapter_names)):
        if url[:6] == '/html/':
            remaining = process_chapter(
                          homepage,
                          name,
                          url,
                    index, completed, remaining
                    )
            if remaining == 0:
                break
    with open('index', 'w') as file:
        file.write('\n'.join(list(completed)))
    # pool.shutdown()


if __name__ == '__main__':
    main(input('Novel Homepage:\n>'))
