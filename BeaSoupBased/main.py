from bs4 import BeautifulSoup, Tag


if __name__ == '__main__':
    soup = BeautifulSoup(open('./xinwen.html'), 'lxml')
    div = soup.find_all(id='xlmain')
    assert 1 == len(div)
    div: Tag = div[0]
    content = ''
    for s in div.stripped_strings:
        content += s
    print(content)
