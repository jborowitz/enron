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

b=coll.find({'subFolder':'tw_imbalances'}, fields='body',limit=50)
# Look at every mesage in folder 'tw-imbalances', but only bring back the
# body of the message
one=coll.find_one()
# Get a single message from the db
sentences = nltk.sent_tokenize(one['body'])
# tokenize a message into sentences using the recommended tokenizer
#out = []
#for s in sentences:
    #out = out + [f.strip(' \t\n') for f in s.split('\n\n')]
## extra tokenization by double line breaks (common in email, not done in
## nltk)

wordTokenizedSentences = [nltk.word_tokenize(sentence) for sentence in out]
# Tokenize sentences into words using recommended tokenizer

partOfSpeechTaggedSentences = [nltk.pos_tag(sentence) for sentence in wordTokenizedSentences]
# Tag parts of speech using recommended tokenizer

namedEntities = [nltk.ne_chunk(sentence) for sentence in partOfSpeechTaggedSentences]

# Begin working on other examples

# Regex search of body
b=client.enron_mail.messages.find({'body': { '$regex' : '.*settled.*'}})
# This code does a (slow) regex search for times when the string
# "settled" appears somewhere in the body
b.count()
# This is the number of email bodies where 'settled' appears.

