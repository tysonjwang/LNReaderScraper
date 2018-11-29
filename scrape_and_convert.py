#! usr/bin/python3
from concurrent.futures import ThreadPoolExecutor
from lxml import html
import requests
from opencc import OpenCC
import os
# %%


def process_chapter(base_url, chap_name, rel_url, index):
    print(base_url)
    print(rel_url)
    url = base_url[:-5] + rel_url[9:]
    print(url)
    chap_get = requests.get(url)
    try:
        chap_get.raise_for_status()
        chap = html.fromstring(chap_get.content)
        chap_text = chap.xpath('//div[@id="contents"]/text()')
        full = chap_name + '\n' + '\n'.join(map(str.strip, chap_text)) + '\n'
        full = openCC.convert(full)
        with open('novelchapter{}.txt'.format(index), 'w') as file:
            file.write(full)
        print("Finished: {}".format(chap_name))
    except Exception as exc:
        print('Chapter: {} was not gotten due to error {}'.format(chap_name,
                                                                  exc))
# %%


openCC = OpenCC('custom')

def main(url):
    # Make sure the chapter url is from ztjxsw.cn
    # pool = ThreadPoolExecutor(max_workers=10)
    os.chdir('novels')
    homepage = url
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
    print(len(chapter_urls))
    print(len(chapter_names))
    for index, (url, name) in enumerate(zip(chapter_urls, chapter_names)):
        if url[:6] == '/html/':
            process_chapter(
                          homepage,
                          name,
                          url,
                    index
                    )
    # pool.shutdown()


if __name__ == '__main__':
    main(input('Novel Homepage:\n>'))
