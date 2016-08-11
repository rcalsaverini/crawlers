import chardet
import email
import imaplib

__author__ = 'calsaverini'


class GmailFetcher(object):
    def __init__(self, usr, password):
        self.address = 'imap.gmail.com'
        self.connection = self.connect(usr, password)

    def connect(self, usr, password):
        connection = imaplib.IMAP4_SSL(self.address)
        connection.login(usr, password)
        return connection

    def fetch_by_uid(self, uid):
        _, data = self.connection.uid('fetch', uid, "(RFC822)")
        mail_obj = email.message_from_string(data[0][1])
        return get_message(mail_obj)

    def get_uids(self):
        _, data = self.connection.uid('search', None, "ALL")
        uids = data[0].split()
        return uids

    def fetch_raw(self):
        self.connection.select("[Gmail]/All Mail")
        uids = self.get_uids()
        for uid in uids:
            _, data = self.connection.uid('fetch', uid, "(RFC822)")
            yield uid, data[0][1]



    def fetch_all(self):
        self.connection.select("[Gmail]/All Mail")
        uids = self.get_uids()
        for uid in uids:
            yield uid, self.fetch_by_uid(uid)



def get_message(mail_obj):
    message = fix_fields(mail_obj)
    message['text'] = get_text(mail_obj)
    return message


def get_text(mail_obj):
    main_type = mail_obj.get_content_maintype()
    if main_type == 'text':
        text = mail_obj.get_payload()
        return text
    elif main_type == 'multipart':
        text = ""
        for part in mail_obj.get_payload():
            text += "\n" +  get_text(part)
        return text
    else:
        return ""


def fix_fields(mail_obj):
    fields = {}
    for (k,v) in mail_obj.items():
        if v is not None:
            fields.update({k.lower(): v})
    return fields

def fix_encoding(text):
    encoding = chardet.detect(text)['encoding'] or 'utf-8'
    return text.decode(encoding)
