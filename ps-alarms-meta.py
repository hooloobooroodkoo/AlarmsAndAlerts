# The code looks for the most recent data for each tested node
# It scans all INDICES = ['ps_packetloss', 'ps_owd', 'ps_throughput', 'ps_trace'] and extracts the host, ip, site
# Then looks for additional data in ps_meta
# Finally, it stores one record for each IP address along with the following fields: 
# ['host', 'site', 'netsite', 'administrator', 'email', 'lat', 'lon', 'site_meta']

from elasticsearch.helpers import bulk
from data_objects.MetaData import MetaData
import utils.helpers as hp


meta_obj = MetaData()
df = meta_obj.metaDf

df = df[~(df['ip'].isnull()) & ~(df['netsite'].isnull())]

# prepare the data for ES - adding _id to send in bulk
df['_id'] = df['ip']+df['netsite']
df.fillna('',inplace=True)
dataDict = df.to_dict('records')

def sendToES(data):
    for d in data:
        try:
            bulk(hp.es, [d], index='ps_alarms_meta')
        except Exception as e:
            print(d,e)
    print(f'Inserted {len(data)} documents')

sendToES(dataDict)
