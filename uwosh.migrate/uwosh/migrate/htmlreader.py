from HTMLParser import *

class HTMLReader(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.title = ""
        self.currentTag = ""

    def handle_starttag(self, tag, attrs):
        self.currentTag = tag

    def handle_data(self, data):
        if self.currentTag == "title":
            self.title = data
                
    def handle_endtag(self, tag):
        self.currentTag = ""
        
    def get_title(self):
        return self.title
    		