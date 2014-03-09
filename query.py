#!/bin/python
import nltk
import pymongo
client = pymongo.MongoClient()
# This will connect to the mongodb database if it's running under default
# configs
enron = client.enron_mail
# use the enron_mail database
coll = enron.messages
# look at the messages collection inside that database

b=coll.find({'headers':{'From':'michael.simmons@enron.com'}}, limit=50)
# Find emails with 'michael.simmons@enron.com' in the From field.
# This returns an iterator, which you can either use directly in a loop
# or you can put into an array of dicts with:
# a_of_d = [email for email in b]

b=client.enron_mail.messages.find({'body': { '$regex' : '.*settled.*'}})
# Find emails with the word 'settled' anywere in the body

