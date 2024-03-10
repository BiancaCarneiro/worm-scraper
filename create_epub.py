# coding=utf-8
from scraper import Skitter, TABLE_OF_CONTENTS
from ebooklib import epub
from tqdm.auto import tqdm

NUM_BOOKS = 8
BOOKS_DIVIDERS = ["hive", "extermination", "plage", "colony", "queen", "imago", "sting", "last_book"]

def create_book(book_title:list, book_author:str, book_language:str, book_cover:str):
    crawling_bug = Skitter(TABLE_OF_CONTENTS)
    crawling_bug.get_links()
    
    for book_number in tqdm(range(NUM_BOOKS)):
        book = epub.EpubBook()

        book.set_identifier(book_title[book_number] + book_author)
        book.set_title(book_title[book_number])
        book.set_language(book_language)

        book.add_author(book_author)

        chapters = []
        links = []
        book.set_cover(book_cover[book_number], open(book_cover[book_number], 'rb').read())
        count = 0
        while crawling_bug.get_next_link() and BOOKS_DIVIDERS[book_number] not in crawling_bug.get_next_link():
            count+=1
            chapter_title, chapter_text = crawling_bug.get_next_chapters()
            content = u'<html><head></head><body><h1>' + chapter_title + u'</h1><p>' + "</p><p>".join(chapter_text) + u'</p></body></html>'
            title_file = chapter_title.replace(" ", "").replace(".", "").lower()
            _file_name = f"{title_file}_{count}.xhtml"
            chapter = epub.EpubHtml(title=chapter_title, file_name=_file_name, lang='hr')
            chapter.content=content

            chapters.append(chapter)
            book.add_item(chapter)
            links.append(epub.Link(_file_name, chapter_title, title_file))
            
        book.toc = (links)

        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        style = '''
@namespace epub "http://www.idpf.org/2007/ops";

body {
    font-family: Cambria, Liberation Serif, Bitstream Vera Serif, Georgia, Times, Times New Roman, serif;
}

h2 {
    text-align: left;
    text-transform: uppercase;
    font-weight: 200;     
}

ol {
        list-style-type: none;
}

ol > li:first-child {
        margin-top: 0.3em;
}


nav[epub|type~='toc'] > ol > li > ol  {
    list-style-type:square;
}


nav[epub|type~='toc'] > ol > li > ol > li {
        margin-top: 0.3em;
}

'''

        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
        book.add_item(nav_css)

        book.spine = ['cover', 'nav'] + chapters

        epub.write_epub(f'{book_title[book_number]}.epub', book, {})
    
if __name__ == '__main__':
    create_book([f"WORM vol {n+1}" for n in range(NUM_BOOKS)], "Wildbow", "en", [f"covers/cover_{n+1}.png" for n in range(NUM_BOOKS)])