import requests
from bs4 import BeautifulSoup
from typing import List, Tuple, Any
from datetime import datetime, timezone

import app.config as config
from app.texts import project_message


class Project:
    def __init__(self, id: int, url: str, title: str, price: str, description: str, publish_date: datetime, tags: List[str]):
        self.id = id
        self.url = url
        self.title = title
        self.price = price
        self.description = description
        self.publish_date = publish_date
        self.tags = tags

    def __str__(self):
        return project_message.format(url=self.url, title=self.title, price=self.price, description=self.description, publish_date=self.publish_date.strftime('%H:%M %d.%m'))


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

    @classmethod
    def parse_category_rss(cls, category_name: str) -> List[Project]:
        parsed_projects = []

        page = requests.get(cls._join_url(
            f'/rss/projects.xml?category={config.categories[category_name]}'), headers=cls.headers)

        soup = BeautifulSoup(page.text, "xml")

        projects = soup.find_all('item')

        for project in projects:
            project_object = cls._parse_project_page(project, category_name)

            if project_object is not None:
                parsed_projects.append(project_object)

        return sorted(parsed_projects, key=lambda x: x.publish_date)

    @classmethod
    def _parse_project_page(cls, project_item: BeautifulSoup, category_name: str) -> Any:
        project_url = project_item.find('link').text

        id = int(project_url.split('/')[-2])

        title, price = Parser.separate_price(project_item.find('title').text)

        if price is None:
            price = 'По договорённости'

        description = project_item.find('description').text

        tags = [tag.strip() for tag in project_item.find('category').text.split(' / ')]

        if category_name not in tags:
            return None

        publish_date = datetime.strptime(project_item.find('pubDate').text, '%a, %d %b %Y %H:%M:%S %Z').replace(
            tzinfo=timezone.utc)  # очистка даты публикации от лишних данных

        project = {
            'id': id,
            'url': project_url,
            'title': title,
            'description': description,
            'price': price,
            'publish_date': publish_date,
            'tags': tags
        }

        return cls._make_project_object(project)

    @classmethod
    def _join_url(cls, path: str) -> str:
        return cls.url + path

    @staticmethod
    def separate_price(text: str) -> Tuple[str, Any]:
        try:
            return text[:text.index('(Бюджет: ')], text[text.index('Бюджет: '):].split()[1]
        except ValueError:  # substring not found
            return text, None

    @staticmethod
    def _make_project_object(project: dict) -> Project:
        for key in project:
            if isinstance(project[key], str):
                project[key] = project[key].strip()
        return Project(**project)
