import requests
from bs4 import BeautifulSoup

TABLE_OF_CONTENTS = "https://parahumans.wordpress.com/table-of-contents/"

class Skitter:
    def __init__(self, url):
        self.url = url
        self.links = []

    def get_links(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for section in soup.find_all("strong"):
            for link in section.find_all('a'):
                self.links.append(link.get('href'))

    def print_links(self):
        for link in self.links:
            print(link)
            
    def get_next_link(self) -> str:
        if len(self.links) > 0:
            return self.links[0]
        else:
            return None
        
    def get_next_chapters(self) -> (str, list):
        link = self.links.pop(0)
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = ""
        for header in soup.find_all("h1", class_="entry-title"):
            title = header.text
        paragraphs = []
        for chapter in soup.find_all("div", class_="entry-content"):
            for paragraph in chapter.find_all("p"):
                if "next chapter" not in paragraph.text.lower() and "last chapter" not in paragraph.text.lower():
                    paragraphs.append(paragraph.text)
        return title, paragraphs

    
                
if __name__ == "__main__":
    skitter = Skitter(TABLE_OF_CONTENTS)