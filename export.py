import pymongo
import json
import pandas
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

datas = set([])
email_file = open('emails.json','r')
with open('emails.json') as email_file:
    for line in email_file:
        data = json.loads(line)
        headers = data.pop('headers')
        for f in data.keys():
            datas.add(f)
        for f in headers.keys():
            datas.add(f)
        # Within this loop, we are reading in one line at a time.
        # This will avoid having all 500k emails in memory


# The code below writes the loaded data to a spreadsheet, replacing
# carriage returns with the string [newline]
written = False
a = pandas.DataFrame(index=[0], columns=datas)
with open('emails.json') as email_file:
    for line in email_file:
        mail = json.loads(line)
        for f in data.keys():
	    a.at[0,f] = mail[f].replace('\n','[newline]')
        for f in headers.keys():
            try:
                a.at[0,f] = mail['headers'][f].replace('\n','[newline]')
            except:
                continue
        if not written:
            a.to_csv('file.csv', index=False, encoding='utf-8')
            written=True
        else:
            a.to_csv('file.csv', index=False, mode='a', header=False, encoding='utf-8')


