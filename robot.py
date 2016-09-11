from flask import Flask, request, redirect, url_for

import twilio.twiml
from google_speech import recognize_speech

@app.route("/robot", methods=['GET', 'POST'])
def handle_robot():
    global robotSidToUserNumber
    resp = twilio.twiml.Response()
    recording_url = request.values.get("RecordingUrl", None)
    sid = request.values.get("CallSid")
    user_number = sidToUserNumber[ sid ]
    if recording_url:
        print recording_url
        transcript = recognize_speech(recording_url)
        print transcript
        if transcript and ('yes' in transcript.lower()):
            user_number = robotSidToUserNumber[ sid ]
            resp.say("I'm the voice assistant robot for Ang Li. Please hold on for a few seconds while I wake up my master.")
            resp.dial(user_number)
            resp.say("Sorry, Ang Li is not available. Thank you and have a nice day.")
            return str(resp)

    resp.record(maxLength="2", action="/robot")
    return str(resp)
