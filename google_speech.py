import urllib2
import base64
import subprocess
import requests
import json

GOOGLE_AUTH_TOKEN = None
SPEECH_API = "https://speech.googleapis.com/v1beta1/speech:syncrecognize"

def get_google_auth_token():
  global GOOGLE_AUTH_TOKEN
  if GOOGLE_AUTH_TOKEN is None:
    GOOGLE_AUTH_TOKEN = subprocess.Popen(["gcloud", "auth", "print-access-token"],
                                         stdout=subprocess.PIPE).communicate()[0]
    GOOGLE_AUTH_TOKEN = GOOGLE_AUTH_TOKEN.strip("\n")
  return GOOGLE_AUTH_TOKEN

# Returns recognized transcript as a string. Returns false if that failed.
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

  r = requests.post(SPEECH_API, data=json.dumps(body), headers=headers)

  transcripts = []
  if r.status_code == 200:
    j = r.json()
    if "results" in j:
      for result in j["results"]:
        if "alternatives" in result:
          for alternative in result["alternatives"]:
            if "transcript" in alternative:
              transcripts.append(alternative["transcript"])

  return " ".join(transcripts)
