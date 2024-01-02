from bs4 import BeautifulSoup
from flask import *
import requests
import json
import time
import os

def scraper():
    END = '\033[0m' if os.name != 'nt' else ''
    UNDERLINE = '\033[4m' if os.name != 'nt' else ''

    url = "https://edition.cnn.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    news1 = soup.find('h2', class_='container__title_url-text container_lead-package__title_url-text')
    news2 = soup.find_all('div', class_='container__headline container_lead-package__headline')
    news3 = soup.find_all('span', class_='container__headline-text')

    import re

    print(UNDERLINE + "HEADLINE" + END + "\n")

    for item1 in news1:
        news1regex = re.search(r'>(.*?)<', str(item1))
        print(str(item1))

    news2regex = ''

    for item2 in news2:
        match = re.search(r'>(.*?)<', str(item2))
        if match:
            news2regex_line = match.group(1)
            if news2regex_line.strip():
                news2regex += str(news2regex_line) + "\n"

    print(str(news2regex))
    print("\n" + UNDERLINE + "TRENDING TOPICS" + END + "\n")

    news3regex = ''

    for index, item3 in enumerate(news3, start=1):
        match = re.search(r'>(.*?)<', str(item3))
        if match:
            news3regex_line = match.group(1)
            if news3regex_line.strip():
                news3regex += str(news3regex_line) + "\n"
                if index == 8:
                    news3regex += "\n" + UNDERLINE + "MORE DETAILED NEWS\n" + END + "\n"

    return news2regex

app = Flask(__name__)
@app.route('/api/headlines/', methods=['GET'])

def headlinesAPI():
    headlines_number = int(request.args.get('count', 5))
    headlines = scraper().splitlines()[:headlines_number]

    response_data = {
        'Headlines': headlines,
        'GeneratedAt': time.ctime(),
        'Timestamp': time.time(),
    }

    return json.dumps(response_data)

if __name__ == '__main__':
    app.run(port=7777)
