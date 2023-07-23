from typing import List
from bs4 import BeautifulSoup

from logger import Logger


class Scrapper(Logger):
    def __init__(self, data) -> None:
        super().__init__()
        self.soup = self._get_parsed_html(data)
    
    def _get_parsed_html(self, data: str):
        try:
            parsed_html = BeautifulSoup(data, 'html.parser')
            return parsed_html
        except Exception:
            self.error('Error while parsing HTML')
    
    def get_tag_value(self, tag, tag_class='', recursive = False, return_raw_component = False)-> str:
        val = self.soup.find(tag, class_=tag_class, recursive=recursive) if tag_class else self.soup.find(tag)
        return val.text if not return_raw_component else val

    def get_all_tags(self, tag, tag_class='') -> List[str]:
        vals = self.soup.find_all(tag, class_=tag_class) if tag_class else self.soup.find_all(tag)
        return [val.text for val in vals]