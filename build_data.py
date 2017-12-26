import json
import os
import re
import unicodecsv as csv

print "Loading database..."


batch_size = 1000
batches_count = 100

print "Dry run..."
count = 0
records = []
try:
    with open('content.csv', 'rb') as content_csv:
        reader = csv.reader(content_csv, delimiter=';', quotechar='|', encoding='utf-8')
        for row in reader:
            count = count + 1
except IOError:
    pass

print "Totally %s records found." % count

print "Building filesystem for the index..."


n = int(count / (batches_count * batch_size))

for i in range(n + 1):
    d = './website/data/json/%s' % i
    os.mkdir(d)

print "Filesystem tree successfully built."


batch = []

batch_num = 1

latest = {'idx': len(records) - 1, 'batch': 0, 'vol': 0}

k = 0

vol = 0

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
            latest['batch'] = batch_num
            latest['vol'] = vol
            with open(batch_path, 'w') as f:
                f.write("if (typeof batches === 'undefined') batches = {}; batches['%s/%s'] = %s;" % (vol, batch_num, json.dumps(batch)))

            batch_num = batch_num + 1

            print "Batch %s/%s processed." % (vol, batch_num)

            if batch_num == batches_count:
                batch_num = batch_num - batches_count
                vol = vol + 1

            batch = []

        k = k + 1


with open('./website/data/json/latest.js', 'w') as f:
    f.write("var content = %s;" % json.dumps(latest))


print "Well done. Enjoy!"
