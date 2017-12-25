import sys
import re
import unicodecsv as csv
import feedparser

print "Reading content index..."
records = []
try:
    progress = 0
    with open('content.csv', 'rb') as content_csv:
        reader = csv.reader(content_csv, delimiter=';', quotechar='|', encoding='utf-8')
        for row in reader:
            title = row[0]
            duration = row[1]
            thumb_large = row[2]
            embed = row[3]
            direct_embed = row[4] == '1'
            record = (title, duration, thumb_large, embed, direct_embed)
            records.append(record)
            progress = progress + 1
            if progress % 1000 == 0:
                print "Progress: %s" % progress
except IOError as e:
    print e
    sys.exit(1)


print "Accessing feed..."
r = feedparser.parse('https://www.pornhub.com/video/webmasterss')


def iframe_url(markup):
    r = re.match(r'(.+)src=\"([^\"]+)\"(.+)$', markup)
    if not r:
        raise Exception("Unknown format for embedded video.")
    return r.group(2)

new_records = [(item['title'], item['duration'], item['thumb_large'], iframe_url(item['embed']), 'blank.gif' in item['thumb_large']) for item in r['entries']]

known_embeds = map(lambda r: r[3], records)

print "Writing content index..."
with open('content.csv', 'ab') as content_csv:
    writer = csv.writer(content_csv, delimiter=';', quotechar='|', encoding='utf-8')
    unique_recs = filter(lambda r: r[3] not in known_embeds, new_records)
    [writer.writerow(r) for r in unique_recs]
    print "Added %s new videos." % len(unique_recs)
