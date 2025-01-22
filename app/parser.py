import grequests
from bs4 import BeautifulSoup
from typing import List


class Project:
    def __init__(self, id: int, url: str, title: str, price: str, time: str, description: str, publish_date: str, tags: List[str]):
        self.id = id
        self.url = url
        self.title = title
        self.price = price
        self.time = time
        self.description = description
        self.publish_date = publish_date
        self.tags = tags


class AsyncParser:
    url = 'https://www.fl.ru'
    st_accept = "text/html"
    st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
    headers = {
        "Accept": st_accept,
        "User-Agent": st_useragent
    }

    right_div_search ='div.py-32.text-right.unmobile.flex-shrink-0.ml-auto.mobile'
    publish_date_search = 'b-layout__txt b-layout__txt_padbot_30 mt-32'

    @classmethod
    async def parse_projects_page(cls) -> List[Project]:
        parsed_projects = []

        page = await grequests.get(cls._join_url('/projects/?kind=1'), headers=cls.headers)

        soup = BeautifulSoup(page.text, "html.parser")

        projects = soup.find_all('div', class_='b-post__grid')

        for project in projects:
            link = project.find('h2').find('a')['href']

            parsed_projects.append(cls._parse_project_page(cls._join_url(link)))

        """
        with open('data.json', 'w', encoding='UTF-8') as file:
            json.dump(parsed_projects, file, ensure_ascii=False)
        """

        return parsed_projects


    @classmethod
    async def _parse_project_page(cls, project_url: str) -> List[Project]:
        project = Project()

        id = project_url.split('/')[-2]

        page = await grequests.get(project_url, headers=cls.headers)

        soup = BeautifulSoup(page.text, "html.parser")

        title = soup.find('h1', id=f'prj_name_{id}').text

        right_div = soup.select_one(cls.right_div_search).findAll('span')
        price = right_div[0].text
        time = right_div[-1].text

        description = soup.find('div', id=f'projectp{id}').text

        tags = [tag.text.strip() for tag in soup.find_all('a', attrs={"data-id": "category-spec"})]

        publish_date = soup.find('div', class_=cls.publish_date_search).find('div', 'text-5').text

        project = {
            'id': int(id),
            'title': title,
            'description': description,
            'price': price,
            'time': time,
            'publish_date': publish_date,
            'tags': tags
        }

        return cls._make_project_object(project)

    @classmethod
    def _join_url(cls, path: str) -> str:
        return cls.url + path

    @staticmethod
    def _make_project_object(project: dict) -> Project:
        for key in project:
            if isinstance(project[key], str):
                project[key] = project[key].strip()
        return Project(**project)
