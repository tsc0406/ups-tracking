import requests
import json
from pytz import timezone
import datetime
import threading
tz = timezone('EST')

class Webhook:

    def __init__(self):
        pass

    def embed(self, link, title, webhook_status, image, quick, path):
        text_file = open(path, 'r')
        datas = json.load(text_file)
        text_file.close()
        proxy = None
        def send(webhook,footer,logo,color):
            payload = {
                'embeds': [
                    {
                        'title': title,
                        'url': link,
                        'color': color,
                        'description': "Package Tracker",
                        'fields': [
                            {'name': 'Status',
                             'value': webhook_status,
                             'inline': False},
                            {'name': 'Tracking Link',
                             'value': link,
                             'inline': False}],
                        'image': {},
                        'author': {},
                        'timestamp': now,
                        'thumbnail': {'url': image},
                        'footer': {'text': footer, 'icon_url': logo},
                        }
                    ]
                }
            requests.post(webhook, data=json.dumps(payload), proxies=proxy, headers={'Content-Type': 'application/json'})
            print('sent webhook to {}'.format(footer))
            
        for data in datas:
            self.webhook= data['webhook']
            self.footer= data['footer']
            self.logo=data['logo']
            self.color=data['color']
            now = str(datetime.datetime.now(tz))
            t = threading.Thread(target=send,args=(self.webhook,self.footer,self.logo,self.color,))
            t.start()