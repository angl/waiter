from flask import Flask, request, redirect, url_for

import twilio.twiml

app = Flask(__name__)

# Try adding your own number to this list!
callers = {
    "+17345481758": "Jiang Chen",
    "+19494392369": "Ang Li",
    "+14158675311": "Virgil",
}

is_representative_available = False

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    from_number = request.values.get('From', None)
    if from_number in callers:
        caller = callers[from_number]
    else:
        caller = "Monkey"

    resp = twilio.twiml.Response()
    # Greet the caller by name
    resp.say("Hello " + caller)
    # Play an mp3
    # resp.play("http://demo.twilio.com/hellomonkey/monkey.mp3")

    # Gather digits.
    with resp.gather(numDigits=1, action="/handle-key", method="POST") as g:
        g.say("""To speak to a real monkey, press 1. 
                 Press 2 to record your own monkey howl.
                 Press any other key to start over.""")

    return str(resp)

@app.route("/handle-key", methods=['GET', 'POST'])
def handle_key():
    """Handle key press from a user."""

    digit_pressed = request.values.get('Digits', None)
    if digit_pressed == "1":
        resp = twilio.twiml.Response()
        # Dial (310) 555-1212 - connect that number to the incoming caller.
        resp.dial("+19494392369")
        # If the dial fails:
        resp.say("The call failed, or the remote party hung up. Goodbye.")

        return str(resp)

    elif digit_pressed == "2":
       return redirect(url_for('handle_recording'))




    # If the caller pressed anything but 1, redirect them to the homepage.
    else:
        return redirect("/")

@app.route("/handle-recording", methods=['GET', 'POST'])
def handle_recording():
    """Challenge and transcribe the caller's response."""

    resp = twilio.twiml.Response()
    if is_representative_available:
        resp.dial("+19494392369")
    else:
        recording_url = request.values.get("RecordingUrl", None)
        if recording_url:
            resp.say("Thanks for howling... take a listen to what you howled.")
            resp.play(recording_url)
            resp.say("Recording ends.")
        resp.say("Hello? Can you hear me?")
        resp.record(maxLength="3", action="/handle-recording",
                transcribe="true", transcribeCallback="/handle-transcription")
    return str(resp)

@app.route("/handle-transcription", methods=['GET', 'POST'])
def handle_transcription():
    """Handle the transcription and check if the representative is available."""

    transcription = request.values.get("TranscriptionText", None)
    print transcription
    if transcription and ("yes" in transcription.lower()):
        is_representative_available = True
    return ""

if __name__ == "__main__":
    app.run(debug=True)
