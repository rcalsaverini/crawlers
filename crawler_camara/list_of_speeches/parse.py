import bs4


def list_of_speeches(html):
    soup = bs4.BeautifulSoup(html, 'lxml')
    table = soup.find("tbody", class_='coresAlternadas')
    return [
        parse_speech(tr)
        for tr in table.findAll("tr")
        if not tr.attrs.get('id', 'no').startswith('Suma')
    ]


def parse_speech(tr):
    data = [td for td in tr.findAll('td')]
    if len(data) != 8:
        raise Exception("Failed to parse 8 fields from row")
    output = {
        'date': data[0].text.strip(),
        'session': data[1].text.strip(),
        'phase': data[2].text.strip(),
        'speech_url': process_speech_url(data[3].find('a').attrs['href']),
        'orator': data[5].text.strip().split(',')[0],
        'party': data[5].text.strip().split(',')[1].split('-')[0],
        'state': data[5].text.strip().split(',')[1].split('-')[1],
        'hour': data[6].text.strip(),
        'publication': data[7].text.strip()
    }
    print(output)
    return output


def process_speech_url(url):
    return "".join([part.strip() for part in url.split("\n")])
