from htmlreader import HTMLReader
import urllib
from Products.PortalTransforms.transforms.safe_html import scrubHTML
from HTMLParser import HTMLParseError

class PageMigrater:

    def __init__(self, context):
        self.__BAD_ID_CHARS = (' ', '\'', '"', '&', '/', '\\')
        self.__inital_context = context
        self.__current_context = context
        self.__errors = list()
        self.__log = list()
        
    def get_errors(self):
        return self.__errors
        
    def get_log(self):
        return self.__log
        
    def __convert_to_id(self, text):
        text = text.lower()
        for char in self.__BAD_ID_CHARS:
            text = text.replace(char, '-')
        return text
        
    def __create_folder(self, title):
        if not hasattr(self.__current_context, title):
            self.__current_context.invokeFactory('Folder', title)
            newFolder = self.__current_context[title]
            newFolder.setTitle(title)
            self.__log.append("Folder: " + title + " created successfully.")
        else:
            self.__errors.append("Folder: " + title + " already exists.")
    
    def __create_page(self, filename, title, content):
        name = self.__convert_to_id(title)
        if hasattr(self.__current_context, name):
            if filename == "" or hasattr(self.__current_context, filename):
                self.__errors.append("Page: " + filename + " already exists.")
                return
            else: 
                name = filename
        
        self.__current_context.invokeFactory('Document', name)
        newPage = self.__current_context[name]
        newPage.setTitle(title)
        newPage.setText(content)
        newPage.reindexObject();
        self.__log.append("Page: " + newPage.Title() + " created successfully.")
        
    def migrate_pages(self, urls, root_url):
        for url in urls:
            self.__current_context = self.__inital_context
    
            folders = url[len(root_url):].split('/')
            folders.pop()
            while '' in folders:
                folders.remove('')

            for folder in folders:
                self.__create_folder(folder)
                self.__current_context = self.__current_context[folder]
            
            try:
                downloaded_html = urllib.urlopen(url)
            except IOError:
                self.__errors.append("Error connecting to: " + url)
                continue
                
            html = downloaded_html.read()
            reader = HTMLReader()
            
            try:
                reader.feed(html)
            except HTMLParseError:
                self.__errors.append("Error parsing: " + url)
            else:
                title = reader.get_title()
                filename = url.split('/').pop()
                cleanedHTML = scrubHTML(html, raise_error=False)
                self.__create_page(filename, title, cleanedHTML)     