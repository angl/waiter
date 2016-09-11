import urllib2
import base64
import subprocess
import requests
import json

GOOGLE_AUTH_TOKEN = None

def get_google_auth_token():
  global GOOGLE_AUTH_TOKEN
  if GOOGLE_AUTH_TOKEN is None:
    GOOGLE_AUTH_TOKEN = subprocess.Popen(["gcloud", "auth", "print-access-token"],
                                         stdout=subprocess.PIPE).communicate()[0]
    GOOGLE_AUTH_TOKEN = GOOGLE_AUTH_TOKEN.strip("\n")
  return GOOGLE_AUTH_TOKEN

def recognize_speech(url):
  retry = True
  while retry:
    try:
      data = urllib2.urlopen(url).read()
      retry = False
    except:
      pass

  encodedData = base64.b64encode(data)
  body = {
      "config": {
        "encoding":"LINEAR16",
        "sample_rate":8000,
        "speech_context": {
          "phrases": [
            "yes",
            "hello",
            "hi",
            "here",
            "thank"
            ]
          }
        },
      "audio": {
        "content":encodedData
        }
      }

  headers = {
      "Content-Type":"application/json",
      "Authorization":"Bearer %s" % get_google_auth_token()
      }

  url = "https://speech.googleapis.com/v1beta1/speech:syncrecognize"

  r = requests.post(url, data=json.dumps(body), headers=headers)

  transcript = None
  if r.status_code == 200:
    j = r.json()
    if "results" in j:
      if len( j["results"] ) > 0:
        result = j["results"][0]
        if "alternatives" in result:
          if len( result["alternatives"] ) > 0:
            alternative = result["alternatives"][0]
            if "transcript" in alternative:
              transcript = alternative["transcript"]

  return transcript
