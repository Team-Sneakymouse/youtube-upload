#!/usr/local/bin/python
import sys
import json
import subprocess
from datetime import datetime, timedelta
def download(instream):
  payload = json.load(instream)
  source = payload['source']
  # source = {
  #   "client-secrets": '{"installed":{"client_id":"<client_id>","client_secret":"<client_secret>","redirect_uris":["<redirect_uri>"],...}}',
  #   "credentials": '{"access_token":"<access_token>","refresh_token":"<refresh_token>","token_uri":"<token_uri>",...}',
  # }
  if 'client-secrets' in source:
    client_secrets = source['client-secrets']
    with open('client_secrets.json', 'w') as f:
      f.write(client_secrets)
  if 'credentials' in source:
    credentials = source['credentials']
    with open('credentials.json', 'w') as f:
      f.write(credentials)

  params = payload["params"]
  # params = {
  #   "file": "video.mp4",
  #   "youtube-dl.info.json": "video.info.json",
  #   "client-secrets": "client_secrets.json",
  #   "credentials-file": "credentials.json",
  #   "title": "Video Title",
  #   "description": "Video Description",
  #   "tags": "youtube,tags",
  #   "recording-date": "1970-01-01",
  #   "default-language": "en",
  #   "default-audio-language": "en",
  #   "publish-at": "1970-01-01T00:00:00Z",
  #   "playlist": "playlist",
  # }
  if not "client-secrets" in params:
    params["client-secrets"] = "client_secrets.json"
  if not "credentials-file" in params:
    params["credentials-file"] = "credentials.json"
  if "youtube-dl.info.json" in params:
    file = open(params["youtube-dl.info.json"], "r")
    info = json.load(file)

    params["title"] = info["title"]
    timestamp = datetime.utcfromtimestamp(info["timestamp"])
    params["description"] = f"Streamed on {timestamp.strftime('%Y-%m-%d')}\n{info['id'].replace('v', '')}"
    timestamp = timestamp + timedelta(hours=24)
    params["publish-at"] = timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')

    file.close()
  
  command = "youtube-upload"
  for param in params.items():
    if param[0] == "file":
      continue
    command += " --" + param[0] + " \"" + param[1] + "\""
  
  command += " " + params["file"]

  videoId = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
  return [{"url": "https://youtu.be/" + videoId.strip()}]

if __name__ == "__main__":
  print(json.dumps(download(sys.stdin)))