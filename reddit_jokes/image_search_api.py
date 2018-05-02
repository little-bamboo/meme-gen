import requests
import re
import json


class image_search_api(object):

    def __init__(self):
        self.searching = False

    def search(self, keywords, max_results=None):
        url = 'https://duckduckgo.com/'
        params = {
            'q': keywords
        }

        #   First make a request to above URL, and parse out the 'vqd'
        #   This is a special token, which should be used in the subsequent request
        res = requests.post(url, data=params)
        searchObj = re.search(r'vqd=(\d+)\&', res.text, re.M | re.I)

        if searchObj:
            headers = {
                'dnt': '1',
                'accept-encoding': 'gzip, deflate, sdch, br',
                'x-requested-with': 'XMLHttpRequest',
                'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6,ms;q=0.4',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'referer': 'https://duckduckgo.com/',
                'authority': 'duckduckgo.com',
            }

            params = (
                ('l', 'wt-wt'),
                ('o', 'json'),
                ('q', keywords),
                ('vqd', searchObj.group(1)),
                ('f', ',,,'),
                ('p', '2')
            )

            requestUrl = url + "i.js"

            res = requests.get(requestUrl, headers=headers, params=params)
            data = json.loads(res.text)

            return data["results"]

        else:
            return

    def printJson(self, objs):
        for obj in objs:
            print "Width {0}, Height {1}".format(obj["width"], obj["height"])
            print "Thumbnail {0}".format(obj["thumbnail"])
            print "Url {0}".format(obj["url"])
            print "Title {0}".format(obj["title"].encode('utf-8'))
            print "Image {0}".format(obj["image"])
            print "__________"
