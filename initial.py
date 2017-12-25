import re
import unicodecsv as csv

def iframe_url(markup):
    r = re.match(r'(.+)src=\"([^\"]+)\"(.+)$', markup)
    if not r:
        raise Exception("Unknown format for embedded video.")
    return r.group(2)

num = 0


with open('content.csv', 'wb') as content_csv:
    writer = csv.writer(content_csv, delimiter=';', quotechar='|', encoding='utf-8')

    with open('./pornhub.com-db.csv') as f:
        for line in f:
            num = num + 1
            chunks = line.split('|')

            embed = iframe_url(chunks[0])
            thumb_large = chunks[1]
            title = chunks[3]
            duration = int(chunks[7])
            direct_embed = 'blank' in thumb_large

            record = (title, duration, thumb_large, embed, direct_embed)

            writer.writerow(record)
            print "\rProgress: %s" % num
