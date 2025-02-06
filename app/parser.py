import requests
from bs4 import BeautifulSoup
from typing import List, Tuple, Any
from datetime import datetime, timezone

from app.texts import project_message


class Project:
    def __init__(self, id: int, url: str, title: str, price: str, time: str, description: str, publish_date: datetime, tags: List[str]):
        self.id = id
        self.url = url
        self.title = title
        self.price = price
        self.time = time
        self.description = description
        self.publish_date = publish_date
        self.tags = tags

    def __str__(self):
        return project_message.format(url=self.url, title=self.title, price=self.price, time=self.time, description=self.description, publish_date=self.publish_date.strptime('%H:%M %d.%m'))


class Parser:
    url = 'https://www.fl.ru'
    st_accept = "text/html"
    st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
    headers = {
        "Accept": st_accept,
        "User-Agent": st_useragent
    }

    right_div_search = 'div.py-32.text-right.unmobile.flex-shrink-0.ml-auto.mobile'
    publish_date_search = 'b-layout__txt b-layout__txt_padbot_30 mt-32'

    categories = {
        'Сайты': 2,
        'Тексты': 8,
        'Дизайн': 3,
        'Программирование': 5
    }

    @classmethod
    def parse_category_rss(cls, category_id: int) -> List[Project]:
        parsed_projects = []

        page = requests.get(cls._join_url(
            f'/rss/projects.xml?category={category_id}'), headers=cls.headers)

        soup = BeautifulSoup(page.text, "xml")

        projects = soup.find_all('item')

        for project in projects:
           # link = project.find('link').text

            parsed_projects.append(cls._parse_project_page(project))

        """
        import json
        with open('data.json', 'w', encoding='UTF-8') as file:
            json.dump(parsed_projects, file, ensure_ascii=False)
        """

        return parsed_projects

    @classmethod
    def _parse_project_page(cls, project_item: BeautifulSoup) -> List[Project]:
        #page = requests.get(project_url, headers=cls.headers)

        #soup = BeautifulSoup(page.text, "lxml")

        #try:
        project_url = project_item.find('link').text

        id = int(project_url.split('/')[-2])

        title, price = Parser.separate_price(project_item.find('title').text)

        if price is None:
            price = 'По договорённости'

        #except AttributeError:
        #    open('dump.txt', 'w').write(page.text)
        #    raise AttributeError()

        #right_div = project_item.select_one(cls.right_div_search).findAll('span')
        #price = right_div[0].text
        #time = right_div[-1].text

        description = project_item.find('description').text

        #print(project_item.find('category'))
        tags = project_item.find('category').text.split('/')

        publish_date = datetime.strptime(project_item.find('pubDate').text, '%a, %d %b %Y %H:%M:%S %Z').replace(tzinfo=timezone.utc) # очистка даты публикации от лишних данных

        project = {
            'id': id,
            'url': project_url,
            'title': title,
            'description': description,
            'price': price,
            'time': '', # TODO: убрать костыль
            'publish_date': publish_date,
            'tags': tags
        }

        return cls._make_project_object(project)
#Wed, 05 Feb 2025 05:17:36 GMT
    @classmethod
    def _join_url(cls, path: str) -> str:
        return cls.url + path
    
    @staticmethod
    def clear_tag_text(text: str) -> str:
        print(text)
        return text[text.rindex('[') + 1:text.index(']')]
    
    @staticmethod
    def separate_price(text: str) -> Tuple[str, Any]:
        try:
            return text[:text.index('(Бюджет: ')], text[text.index('Бюджет: '):].split()[1]
        except ValueError: # substring not found
            return text, None

    @staticmethod
    def _make_project_object(project: dict) -> Project:
        for key in project:
            if isinstance(project[key], str):
                project[key] = project[key].strip()
        return Project(**project)
