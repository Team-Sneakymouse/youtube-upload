#!/usr/local/bin/python
from pprint import pprint
import sys
import json
import googleapiclient.discovery
def _check(instream):
  payload = json.load(instream)
  source = payload['source']
  # source = {
  #   "channel-id": "UCxmdUYEumgACzijeT8LCIuQ",
  #   "api-key": "<api-key>","  
  #   "client-secrets": '{"installed":{"client_id":"<client_id>","client_secret":"<client_secret>","redirect_uris":["<redirect_uri>"],...}}',
  #   "credentials": '{"access_token":"<access_token>","refresh_token":"<refresh_token>","token_uri":"<token_uri>",...}',
  # }
  
  youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=source['api-key'])
  request = youtube.search().list(
    part="id",
    channelId=source['channel-id'],
    type="video",
    order="date",
  )
  response = request.execute()
  urls = list(map(lambda item: {"url": "https://youtu.be/"+item['id']['videoId']}, response['items']))
  return urls

if __name__ == "__main__":
  print(json.dumps(_check(sys.stdin)))