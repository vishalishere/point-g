import re
import unicodecsv as csv
import feedparser

records = []
try:
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
except IOError:
    pass


r = feedparser.parse('https://www.pornhub.com/video/webmasterss')


def iframe_url(markup):
    r = re.match(r'(.+)src=\"([^\"]+)\"(.+)$', markup)
    if not r:
        raise Exception("Unknown format for embedded video.")
    return r.group(2)

new_records = [(item['title'], item['duration'], item['thumb_large'], iframe_url(item['embed']), 'blank.gif' in item['thumb_large']) for item in r['entries']]

known_embeds = map(lambda r: r[3], records)


with open('content.csv', 'ab') as content_csv:
    writer = csv.writer(content_csv, delimiter=';', quotechar='|', encoding='utf-8')
    unique_recs = filter(lambda r: r[3] not in known_embeds, new_records)
    [writer.writerow(r) for r in unique_recs]
    print "Added %s new videos." % len(unique_recs)
