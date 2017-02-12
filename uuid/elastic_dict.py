#!/usr/bin/python3
'Sends words to elasticsearch'

import uuid
import json
import requests

filename = '../common/words'
batch_size = 10000
bulk_index_header = '{ "index" : { } }\n'
elastic_url = 'http://localhost:9200'
elastic_bulk_endpoint = '/dict_uuid/word/_bulk'

def get_uuid():
    'Produces a uuid4 string'
    return str(uuid.uuid4())

def send_to_elastic(message):
    'Sends to elastic'
    r = requests.put(elastic_url+elastic_bulk_endpoint, data=message)
    # print(r.text)

uuids = []

total_message_count = 0
with open(filename, 'rt') as raw_words:
    counter = 0
    bulk_index_records = ''
    for raw_word in raw_words:
        counter += 1
        word_uuid = get_uuid()
        uuids.append(word_uuid)
        record = {"uuid" : word_uuid, "word": raw_word.strip()}
        json_record = json.dumps(record) + '\n'
        bulk_index_record = bulk_index_header + json_record
        bulk_index_records += bulk_index_record
        if counter == batch_size:
            total_message_count += 1
            print('Sending message {}'.format(total_message_count))
            send_to_elastic(bulk_index_records)
            counter = 0
            bulk_index_records = ''
    print('Closing...')
    send_to_elastic(bulk_index_records) # Don't forget to send the last batch that might be < batch_size

with open('ids.txt', 'wt') as uuidd_file:
    for i in uuids:
        uuidd_file.write('"{}",\n'.format(i))



