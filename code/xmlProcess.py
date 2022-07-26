import xml.etree.ElementTree as ET
#NOTES:
# https://www.edureka.co/blog/python-xml-parser-tutorial/
#https://docs.python.org/3/library/xml.etree.elementtree.html
#https://stackoverflow.com/questions/17530471/get-all-text-from-an-xml-document
#https://stackoverflow.com/questions/21074361/how-to-recursively-iterate-over-xml-tags-in-python-using-elementtree

#TO USE:
# to instlal virtual env: python3 -m pip install --user virtualenv
# activate virtualenviroemnt using: 'source . venv/bin/activate'


print("Begin Parsing:")
mytree = ET.parse('sitemap.xml')
myroot = mytree.getroot()
for child in mytree.iter():
    #print(child.tag)
    if child.tag == "{http://www.sitemaps.org/schemas/sitemap/0.9}loc":
        print(child.text)

# linkString = ET.tostring(mytree.getroot(),method='text', encoding='utf-8')
# # linkString = linkString.replace('\n', '')
# # linkString = linkString.strip()
# print(linkString)