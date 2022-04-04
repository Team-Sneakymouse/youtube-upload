#!/usr/local/bin/python
import sys
import json
import subprocess
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
  if not "file" in params:
    raise Exception("Missing 'file' in params")
  if not "client-secrets" in params:
    params["client-secrets"] = "client_secrets.json"
  if not "credentials-file" in params:
    params["credentials-file"] = "credentials.json"
  
  command = "youtube-upload"
  for param in params.items():
    if param[0] == "file":
      continue
    command += " --" + param[0] + " \"" + param[1] + "\""
  
  command += " " + params["file"]

  url = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
  return [{"url": url}]

if __name__ == "__main__":
  print(json.dumps(download(sys.stdin)))