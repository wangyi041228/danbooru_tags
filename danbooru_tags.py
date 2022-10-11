from ez_aio.aio import get
from ez_aio import proxy0, header0
from bs4 import BeautifulSoup
from json import dumps, loads

ur = f'https://danbooru.donmai.us'


def main():
    a = get('https://danbooru.donmai.us/wiki_pages/tag_groups', proxy=proxy0, headers=header0)[0]
    tree = BeautifulSoup(a, 'lxml')
    body = tree.find('div', {'id': 'wiki-page-body'})
    data = []
    try:
        for item0 in body:
            _name0 = item0.name
            _string0 = item0.string
            if _name0 == 'h5':
                data.append([_string0, ])
            elif _name0 == 'h6':
                data[-1].append([_string0, ])
            elif _name0 == 'ul':
                for item1 in item0:
                    _name1 = item1.name
                    if _name1 == 'li':
                        a = item1.find('a')
                        if not isinstance(data[-1][-1], list):
                            data[-1].append(['', ])
                        if a:
                            _s = ''
                            for item2 in item1:
                                _s += item2.string
                            _sub = sub(ur + a['href'])
                            data[-1][-1].append([_s, ur + a['href'], _sub])
                        else:
                            data[-1][-1].append([item1.string])
                    elif _name1 == 'ul':
                        data[-1][-1].append([])
                        for item2 in item1:
                            _name2 = item2.name
                            if _name2 == 'li':
                                a = item2.find('a')
                                _sub = sub(ur + a['href'])
                                data[-1][-1][-1].append([a.string, ur + a['href'], _sub])
    finally:
        with open('e.json', 'w', encoding='utf-8') as f:
            print(dumps(data, indent=4, ensure_ascii=False), file=f)


def sub(url):
    print(url)
    a = get(url, proxy=proxy0, headers=header0)[0]
    tree = BeautifulSoup(a, 'lxml')
    body = tree.find('div', {'id': 'wiki-page-body'})
    data = []
    try:
        for item0 in body:
            _name0 = item0.name
            _string0 = item0.string
            if _name0 == 'h4':
                data.append([_string0, ])
            elif _name0 == 'h5':
                data[-1].append([_string0, ])
            elif _name0 == 'ul':
                for item1 in item0:
                    _name1 = item1.name
                    if _name1 == 'li':
                        a = item1.find('a')
                        if not isinstance(data[-1][-1], list):
                            data[-1].append(['', ])
                        if a:
                            _s = ''
                            for item2 in item1:
                                _s += item2.string
                            data[-1][-1].append([_s, ur + a['href']])
                        else:
                            data[-1][-1].append([item1.string])
                    elif _name1 == 'ul':
                        data[-1][-1].append([])
                        for item2 in item1:
                            _name2 = item2.name
                            if _name2 == 'li':
                                a = item2.find('a')
                                data[-1][-1][-1].append([a.string, ur + a['href']])
    finally:
        return data


def md():
    def pr(d, ll):
        r = ''
        for item in d:
            if isinstance(item, list):
                if len(item) == 1 and isinstance(item[0], str):
                    r += f"{' ' * (ll + 2)}* {item[0]}\n"
                elif len(item) == 2 and isinstance(item[0], str) and isinstance(item[1], str):
                    r += f"{' ' * (ll + 2)}* {item[0]}\n"
                else:
                    r += pr(item, ll + 2)
            else:
                if item and not item.startswith('https://'):
                    r += f"{' ' * ll}* {item}\n"
        return r

    with open('e.json', 'r', encoding='utf-8') as f:
        data = loads(f.read())
    ppp = pr(data, -2)
    with open('e.md', 'w', encoding='utf-8') as f:
        print(ppp, file=f, end='')


if __name__ == '__main__':
    # main()
    md()
