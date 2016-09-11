from flask import Flask, request, redirect
import twilio.twiml
import twilio.rest

app = Flask(__name__)

accountSid = "AC2e34224eaf5338f905e20b3971137eed"
authToken = "23dc8d06c0366efedd2e91e41c7bb06c"
client = twilio.rest.TwilioRestClient(accountSid, authToken)

# Host number
hostNumber = "+14154293758"

# Customer service number
customerServiceNumber = "+17345481758"

# Robot number
robotNumber = "+18582107986"

# Host URL (the URL hosting THIS service)
hostUrl = "https://2c610ae9.ngrok.io"

# sid for each session (keyed by user's number)
customerServiceSid = {}
robotServiceSid = {}

@app.route("/", methods=['GET', 'POST'])
def entrance():
  userNumber = request.values.get('From', None)
  #userNumber = userNumber.replace( '+', '' )
  # make the call to customer service
  call = client.calls.create(to=customerServiceNumber, from_=hostNumber,
                             url=hostUrl + "/%s/customer_service" % userNumber)

  # make the call to the robot
  call = client.calls.create(to=robotNumber, from_=hostNumber,
                             url=hostUrl + "/%s/robot" % userNumber)

  confName = "conf-%s" % userNumber
  print "send user to conference %s" % confName

  resp = twilio.twiml.Response()
  resp.say("Welcome")
  with resp.dial(method="POST") as d:
    d.conference(name=confName, muted=False)

  return str(resp)

@app.route("/<userNumber>/customer_service", methods=['GET', 'POST'])
def customer_service(userNumber):
  confName = "conf-%s" % userNumber
  print "send customer service to conference %s" % confName

  resp = twilio.twiml.Response()
  resp.say("Welcome Customer Representative")
  with resp.dial(method="POST") as d:
    d.conference(name=confName, muted=False, endConferenceOnExit=True)

  return str(resp)

@app.route("/<userNumber>/robot", methods=['GET', 'POST'])
def robot(userNumber):
  confName = "conf-%s" % userNumber
  print "send robot to conference %s" % confName

  resp = twilio.twiml.Response()
  resp.say("Welcome Robot")
  with resp.dial(method="POST") as d:
    d.conference(name=confName, muted=False)

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
        resp = twilio.twiml.Response()
        resp.say("Record your monkey howl after the tone.")
        resp.record(maxLength="30", action="/handle-recording")
        return str(resp)

    # If the caller pressed anything but 1, redirect them to the homepage.
    else:
        return redirect("/")

@app.route("/handle-recording", methods=['GET', 'POST'])
def handle_recording():
    """Play back the caller's recording."""

    recording_url = request.values.get("RecordingUrl", None)

    resp = twilio.twiml.Response()
    resp.say("Thanks for howling... take a listen to what you howled.")
    resp.play(recording_url)
    resp.say("Goodbye.")
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
