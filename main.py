import time
import requests
from pytz import timezone
import datetime
import random
from webhook import Webhook
import json

tz = timezone('EST')
interval = 35
tracking_details = []
trackings = [
['','UPS'],
['','UPS']
]

def main(tracking_number, site, is_first_time):
    print('\n*********************')
    now = str(datetime.datetime.now(tz))
    print('')
    print(now)
    print(tracking_number)
    proxy = None
    if 'UPS' in site:
      url = "https://www.ups.com/track/api/Track/GetStatus?loc=en_US"
      payload = {"Locale":"en_US","TrackingNumber":[tracking_number],"Requester":"wt"}
      headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'Sec-Fetch-Dest': 'empty',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0. 2272.118 Safari/537.36.',
        'Content-Type': 'application/json',
        'Origin': 'https://www.ups.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Referer': 'https://www.ups.com/track?loc=en_US&tracknum='+tracking_number+'&requester=WT/trackdetails',
        'Accept-Language': 'en-US,en;q=0.9'
      }
      try:
        response = requests.request("POST", url, headers=headers, proxies=proxy, json=payload)
      except requests.RequestException:
          print("request error")
          return False
      if 'Successful' in response.text:
        print('Query good')
        pass
      else:
        print('not successful')
        return False
      try:
        data = response.json()
      except:
        print('data err')
        return False
      for each_status in data['trackDetails'][0]['shipmentProgressActivities']:
        if each_status not in tracking_details:
          webhook_status = str(each_status['activityScan'])+' in '+str(each_status['location'])+' ('+str(each_status['time']).replace('A.M.','AM').replace('P.M.','PM')+')'
          print(webhook_status)
          path = 'track.json'
          send = Webhook()
          quick = ''
          image = 'https://awards.brandingforum.org/wp-content/uploads/2016/05/UPS-Logo.jpg'
          if not is_first_time:
            send.embed('https://www.ups.com/track?tracknum='+tracking_number,'UPS Tracker Update - '+tracking_number,webhook_status,image,quick,path)
          tracking_details.append(each_status)



x = 0
while (True):
    if x == 0:
      is_first_time = True
    else:
      is_first_time = False
    for track in trackings:
        main(track[0],track[1],is_first_time)
    time.sleep(interval)
    x += 1











