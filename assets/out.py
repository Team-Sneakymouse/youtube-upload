#!/usr/local/bin/python
import sys
import json
import subprocess
def download(instream):
  payload = json.load(instream)
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