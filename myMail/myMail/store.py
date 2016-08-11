from datetime import datetime
import ujson as json
import pymongo
from GmailFetcher import GmailFetcher

__author__ = 'calsaverini'


def fix_encoding(message):
    try:
        return message.decode('utf8')
    except UnicodeDecodeError:
        return message.decode('latin1')


if __name__ == '__main__':
    fetcher = GmailFetcher('<mymail>@gmail.com', '<mypassword>')
    conn = pymongo.Connection()
    t0 = datetime.now()
    errors = open("errfile", "w")
    for k, (uid, message) in enumerate(fetcher.fetch_raw()):
        unicode_msg = fix_encoding(message)
        try:
            conn.mymail.raw.insert({'raw': unicode_msg})
        except Exception, e:
            print >> errors, uid, type(e), e.message
            errors.flush()
        if (k + 1) % 25 == 0:
            print (k+1), datetime.now() - t0
