from bs4 import BeautifulSoup
import requests, shutil
all_links = []
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0"}
url = raw_input("Enter a website to extract the URL's from: ")
r = requests.get(url, headers=headers)
data = r.text
soup = BeautifulSoup(data, "html.parser")
img_types = [".png", ".jpg", "jpeg", "gif"]
i = 0
for link in soup.find_all('img'):
    reference = link.get('src')
    # not all sources have file extension in the end
    # file_extension = reference[-4:]
    if reference[:len(url)] != url and reference[:4] != "http" and reference[:2] != "//":
        reference = url + reference
    elif reference[:2] == "//":
        reference = "http://" + reference[2:]
    img_response = requests.get(reference, stream=True)
    for img_type in img_types:
        if reference.find(img_type) != -1:
            file_extension = img_type
            # print("Downloading image from source: %s" % reference)
            with open("img %d %s" % (i, file_extension), 'wb') as out_file:
                shutil.copyfileobj(img_response.raw, out_file)
            del img_response
        else:
            print "image not found"
            print "source %r" % reference

    i += 1