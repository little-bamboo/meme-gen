import sys

import praw
import time

import pymongo
from bson.objectid import ObjectId

import boto3
import json
import image_search_api
import meme_maker


class JokeCollector(object):

    def __init__(self):

        reddit_auth = json.loads(open('../config/reddit_auth.json', 'r').read())

        self.meme_maker = meme_maker.MemeGenerator()

        self.collecting = False
        self.comprehend = boto3.client(service_name='comprehend', region_name='us-west-2')
        self.images = image_search_api.image_search_api()
        self.reddit = praw.Reddit(client_id=reddit_auth['client_id'],
                                  client_secret=reddit_auth['client_secret'], password=reddit_auth['password'],
                                  user_agent=reddit_auth['user_agent'], username=reddit_auth['username'])

    def comprehend_joke(self, title):
        key_phrases = self.comprehend.detect_key_phrases(Text=title, LanguageCode='en')

        phrase_list = []
        for phrase in key_phrases['KeyPhrases']:
            phrase_list.append(phrase['Text'].encode('utf-8'))

        return ' '.join(phrase_list)

    def collect(self):

        subreddit = self.reddit.subreddit('jokes')

        hot_jokes = subreddit.hot()

        mongo_client = pymongo.MongoClient()
        db = mongo_client.reddit_joke_bot
        print db

        for submission in hot_jokes:
            joke_object = {}
            if len(submission.selftext) < 60:

                phrases = self.comprehend_joke(submission.title)

                images_returned = self.images.search(phrases)

                if images_returned:
                    joke_image = images_returned[0]
                else:
                    # Skip over current loop if there is no image returned
                    continue

                joke_object['title'] = submission.title
                joke_object['punchline'] = submission.selftext
                joke_object['key_phrases'] = phrases
                joke_object['image'] = joke_image
                joke_object['created'] = submission.created
                joke_object['author'] = submission.author.name
                joke_object['over_18'] = submission.over_18
                joke_object['permalink'] = submission.permalink
                joke_object['score'] = submission.score
                joke_object['id'] = submission.id
                joke_object['num_comments'] = submission.num_comments

                try:

                    self.meme_maker.make_meme(
                                    joke_object['title'], joke_object['punchline'], joke_object['image'])
                    print json.dumps(joke_object, indent=1)
                    print('---------------')
                    db.reddit_jokes.update({'id':submission.id}, joke_object, upsert=True)

                except pymongo.errors.DuplicateKeyError, e:
                    print "Duplicate Key Error: {0}".format(e)
                except Exception, err:
                    print "Something else went wrong on the mongodb insert: {0}".format(err)

                time.sleep(2)

        return db.reddit_jokes.count()


if __name__ == '__main__':
    jokes = JokeCollector()
    total_jokes_collected = jokes.collect()
    print total_jokes_collected
