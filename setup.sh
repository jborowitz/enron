wget https://s3.amazonaws.com/mongodb-enron-email/enron_mongo.tar.bz2
tar jxf enron_mongo.tar.bz2
nohup mongod --dbpath /mnt/enron/dump/ &
#mongod --dbpath /mnt/enron/dump/
mongorestore dump
