import pandas
import ipdb
import pytz
from dateutil import parser
import json
import networkx as nx
with open('emails.json') as a:
    mails = []
    for mail in a:
        mails.append(json.loads(mail))

froms=[a['headers']['From'] for a in mails]
tos=[a['headers']['To'] for a in mails if 'To' in a['headers'].keys()]
    
def remove_strings(mystr, strings_to_remove=' \n\r\t'):
    """
This is a helper function which takes a string and removes all occurances
of a set of characters (given by "string_to_remove")
    """
    for string in strings_to_remove:
        mystr=mystr.replace(string,'')
    return mystr

def field_to_set(field):
    """
This is a helper function which takes the "from" or "cc" type fields, with
a bunch of strings of emails, and splits them up and returns a set.
    """
    output = set([])
    for email in remove_strings(field).split(','):
        output.add(email)
    return output
def add_new_email_count(G, f, t, d):
    """
This function adds a new date to the list of dates associated with 
emails from address f to address d
    """
    try:
        # If there are already edges, add to this edge array
        G.edge[f][t]['dates'].append(parser.parse(d))
    except KeyError:
	G.add_edge(u=f, v=t, 
		attr_dict={'dates':[parser.parse(email['headers']['Date'])]})
    return G

def get_subgraph(emails,from_date, to_date, numdays=None, center=''):
    """
This will create a graph with only emails sent between from_date and to_date
    """
    fd = pytz.UTC.localize(parser.parse(from_date))
    if numdays:
        # If there is a numdays argument, update by this many days
        td = pytz.UTC.localize(parser.parse(from_date) + datetime.timedelta(days=numdays))
    else:
        td = pytz.UTC.localize(parser.parse(to_date))
    G = nx.DiGraph()
    print(fd)
    print(td)
    count = 0
    for i in range(len(emails)):
        if parser.parse(mails[i]['headers']['Date']) >= fd and parser.parse(mails[i]['headers']['Date']) <= td:
            email = mails[i]
            from_email = email['headers']['From']
            count += 1
            if 'To' in email['headers']:
                to_emails = [a for a in field_to_set(email['headers']['To'])]
                for to_email in to_emails:
                    G = add_new_email_count(G, from_email, to_email, email['headers']['Date'])
    
    
    print('There were %d emails meeting criteria' % count)
    set_lengths(G)
    return G

G = nx.DiGraph()
for i in range(8):
    email = mails[i]
    from_email = email['headers']['From']
    to_emails = [a for a in field_to_set(email['headers']['To'])]
    for to_email in to_emails:
        add_new_email_count(G, from_email, to_email, email['headers']['Date'])
    #G.add_node(from_email)
    # G.add_edge(u=from_email, v=to_email, attr_dict={'dates':[parser.parse(email['headers']['Date']])})

for e in G.edges():
    attr=G[e[0]][e[1]]
    attr['length']=len(attr['dates'])
# This loop generates the "length" attribute which is the number of distinct dates where emails were sent from the from address to the to address

def set_lengths(G):
    for e in G.edges():
        attr=G[e[0]][e[1]]
        attr['length']=len(attr['dates'])
# Now, you can calculate the number of times where individuals received vs sent emails with G.out_degree(weight='length'), which returns a dictionary of email: number of results

G2= get_subgraph(mails, '2000-10-1','2000-11-01')
# get the graph of emails over the period of october 2000

G2.node
G2.edge
# print all the nodes/edges for this subgraph (a mess!)

# The code below generates a data frame
output = pandas.DataFrame(index= pandas.date_range('2000-06-01', periods=5, freq='M'))
output['today'] = output.index
def graph_row(row, freq='M'):
    ds= pandas.date_range(str(row.name), periods=2, freq=freq)
    tomorrow = ds[1]
    #try:
    outgraph = get_subgraph(mails, str(row.name), str(tomorrow))
    #except ValueError:
        #outgraph= None
    return outgraph
output['graphs']=output.apply(graph_row, axis=1)['today']
output['out'] = output.graphs.apply(lambda x: x.out_degree('eric.bass@enron.com', weight='length')).astype(float)
output['in'] = output.graphs.apply(lambda x: x.in_degree('eric.bass@enron.com', weight='length')).astype(float)
output['ratio'] = output['in']/output['out']


output[['in','out', 'ratio']].to_csv('eric.bass.csv')
