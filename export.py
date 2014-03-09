import pymongo
import json
client = pymongo.MongoClient()
enron = client.enron_mail
# use the enron_mail database
coll = enron.messages
# look at the messages collection inside that database

b = coll.find({}, limit = 10000)
# Find a subset of the emails using the coll.find command
myfile= open('emails.json','w')
#emails = [email for email in b]
# Put these emails into an array
for email in b:
    email.pop('_id')
    myfile.write(json.dumps(email)+'\n')
myfile.close()

email_file = open('emails.json','r')
with open('emails.json') as email_file:
    for line in email_file:
        data = json.loads(line)
        # Within this loop, we are reading in one line at a time.
        # This will avoid having all 500k emails in memory

# If you wanted all the data in memory, you could do:
# emails = [json.loads(line) for line in open('emails.json').readlines()]
