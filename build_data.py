import json
import os
import re
import unicodecsv as csv

print "Loading database..."


batch_size = 1000
batches_count = 100

batch = []
batch_num = 0
vol = 0

d = './website/data/json/%s' % vol
os.mkdir(d)

with open('content.csv', 'rb') as content_csv:
    reader = csv.reader(content_csv, delimiter=';', quotechar='|', encoding='utf-8')
    for row in reader:
        title = row[0]
        duration = row[1]
        thumb_large = row[2]
        embed = row[3]
        direct_embed = row[4] == 'True'
        record = (title, duration, thumb_large, embed, direct_embed)

        batch.append(record)
        if len(batch) == batch_size:
            batch_path = './website/data/json/%s/%s.js' % (vol, batch_num)
            with open(batch_path, 'w') as f:
                f.write("if (typeof batches === 'undefined') batches = {}; batches['%s/%s'] = %s;" % (vol, batch_num, json.dumps(batch)))

            batch_num = batch_num + 1

            if batch_num == batches_count:
                batch_num = 0
                print "Volume %s complete. Last rec: %s" % (vol, record[2])


                vol = vol + 1
                d = './website/data/json/%s' % vol
                os.mkdir(d)

            batch = []

    if len(batch) > 0:
        batch_path = './website/data/json/%s/%s.js' % (vol, batch_num)
        with open(batch_path, 'w') as f:
            f.write("if (typeof batches === 'undefined') batches = {}; batches['%s/%s'] = %s;" % (vol, batch_num, json.dumps(batch)))
        print "Volume %s complete. Last rec: %s" % (vol, record[2])



with open('./website/data/json/latest.js', 'w') as f:
    latest = {'batch': batch_num, 'vol': vol}
    if batch_num == 0:
        latest = {'batch': 1000, 'vol': vol - 1}
    f.write("var content = %s;" % json.dumps(latest))


print "Well done. Enjoy!"
