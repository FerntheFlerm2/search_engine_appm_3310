import scrapy
import xml.etree.ElementTree as ET
from os.path import exists
import json

# function to open json file and add document to text-data.json file using correct syntax.
def write_json(data, filename="text-data.json"):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        file_data["data"].append(data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)

# to run spider, navigate to directory above this one and run "scrapy crawl search".
class SearchSpider(scrapy.Spider):
    name = "search"

    def start_requests(self):
        # create text-data.json if it doesn't exist.
        if not exists("text-data.json"):
            with open("text-data.json", 'w') as file:
                file.write('{"data":[]}') # prime for data input.
        
        start_urls = [] # list of all encountered urls in order.

        # parse the sitemap XML file generated previously.
        print("Begin Parsing:")
        mytree = ET.parse('../sitemap.xml')
        myroot = mytree.getroot()
        for child in mytree.iter():
            #print(child.tag)
            if child.tag == "{http://www.sitemaps.org/schemas/sitemap/0.9}loc":
                print(child.text)
                start_urls.append(child.text)
        print("Parsing complete.")

        # start_urls now contains all urls for the corpus.

        i = 0
        for url in start_urls: # for every url, scrape usng the parse funciton.
            i += 1
            yield scrapy.Request(url=url, callback=self.parse, meta={'url': url, 'i': i})

    # parse a url function
    def parse(self, response):
        # print to console the document number
        self.log("I : " + str(response.meta.get('i')))
        ignore_tags = ['.menu-icon-text'] # classes and tags to ignore
        req_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'strong']
        # ^ all HTML tags to capture text from

        section_selector = response.css('body') # scrape from HTML tag body
        for section in section_selector: # iterate through all sections inside body
            texts = [] # list to hold texts
            for tag in section.css('*'): # for every tag in body
                if tag.root.tag in ignore_tags: # if the tag is in ignore tags, skip
                    tag.root.getparent().remove(tag.root) # remove all children from the tree
            for tag in section.css('*'): # for every tag in body
                if tag.root.tag in req_tags: # if the tag is one of the tags to capture from
                    texts = texts + tag.css('*::text').getall() # add all text to texts
            write_json({"url": response.meta.get('url'), "texts": texts}) # write the doc and al
                                                                          # saved data to the json
            
            self.log("logged")