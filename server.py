from flask import Flask, request, redirect
import twilio.twiml
import twilio.rest
from google_speech import recognize_speech

app = Flask(__name__)

accountSid = "AC2e34224eaf5338f905e20b3971137eed"
authToken = "23dc8d06c0366efedd2e91e41c7bb06c"
client = twilio.rest.TwilioRestClient(accountSid, authToken)

# Customer number
customerNumber = "+19494392369"

# Host number
hostNumber = "+14154293758"

# Customer service number
#customerServiceNumber = "+17345481758"

# Robot number
robotNumber = "+18582107986"

# Debugger number
debuggerNumber = "+17345481758"

# Host URL (the URL hosting THIS service)
hostUrl = "https://2c610ae9.ngrok.io"

# mapping from robot SID to user number
robotSidToUserNumber = {}

# robot call SID (in conference)
robotCallSid = None

# customer service call SID (in conference)
customerServiceCallSid = None

# customer call SID (in conference)
customerCallSid = None

triggerWords = [
    "hello",
    "how are you",
    "hear you"
    ]

@app.route("/host", methods=['GET', 'POST'])
def handle_host_entrance():
  global robotSidToUserNumber
  global customerCallSid
  customerCallSid = request.values.get('CallSid')
  userNumber = request.values.get('From', None)

  # Connect debugger
  client.calls.create(to=debuggerNumber, from_=hostNumber,
                      url=hostUrl + "/host/%s/debugger" % customerNumber)

  # Get the customer service phone number.
  resp = twilio.twiml.Response()
  with resp.gather(numDigits=10, action="/handle-customer-service-number",
                   method="POST") as g:
    g.say("""Please dail the number for customer service and we will 
               connect you with them.""")

  return str(resp)

@app.route("/handle-customer-service-number", methods=['GET', 'POST'])
def handle_customer_service_number():
  """Handle customer service number typed by a user."""

  global customerServiceNumber
  customerServiceNumber = request.values.get('Digits', None)
  resp = twilio.twiml.Response()
  resp.say("You just typed: " + customerServiceNumber)
  # make the call to customer service
  call = client.calls.create(to=customerServiceNumber, from_=hostNumber,
                             url=hostUrl + "/host/%s/customer_service" % customerNumber)

  confName = "conf-%s" % customerNumber
  print "send user to conference %s" % confName

  resp = twilio.twiml.Response()
  with resp.dial(method="POST") as d:
    d.conference(name=confName, muted=False, beep=False,
                 statusCallbackEvent="join leave", statusCallback="/host/conference",
                 statusCallbackMethod="POST")

  return str(resp)

@app.route("/host/<userNumber>/customer_service", methods=['GET', 'POST'])
def handle_host_call_customer_service(userNumber):
  global customerServiceCallSid
  customerServiceCallSid = request.values.get('CallSid')
  confName = "conf-%s" % userNumber
  print "send customer service to conference %s" % confName

  resp = twilio.twiml.Response()
  resp.say("Welcome Customer Representative")
  with resp.dial(method="POST") as d:
    d.conference(name=confName, muted=False, endConferenceOnExit=True, beep=False,
                 statusCallbackEvent="join leave", statusCallback="/host/conference",
                 statusCallbackMethod="POST")

  return str(resp)

@app.route("/host/<userNumber>/robot", methods=['GET', 'POST'])
def handle_host_call_robot(userNumber):
  global robotCallSid
  robotCallSid = request.values.get('CallSid')
  confName = "conf-%s" % userNumber
  print "send robot to conference %s" % confName

  resp = twilio.twiml.Response()
  resp.say("Welcome Robot")
  with resp.dial(method="POST") as d:
    d.conference(name=confName, muted=False, beep=False,
                 statusCallbackEvent="join leave", statusCallback="/host/conference",
                 statusCallbackMethod="POST")

  return str(resp)

@app.route("/host/<userNumber>/customer", methods=['GET', 'POST'])
def handle_host_call_customer(userNumber):
  global customerCallSid
  customerCallSid = None
  confName = "conf-%s" % userNumber
  print "send customer to conference %s" % confName

  resp = twilio.twiml.Response()
  resp.say("Your call has been answered. Transferring.")
  with resp.dial(method="POST") as d:
    d.conference(name=confName, muted=False, beep=False,
                 statusCallbackEvent="join leave", statusCallback="/host/conference",
                 statusCallbackMethod="POST")

  return str(resp)

@app.route("/host/<userNumber>/debugger", methods=['GET', 'POST'])
def handle_host_call_debugger(userNumber):
  confName = "conf-%s" % userNumber
  print "send debugger to conference %s" % confName

  resp = twilio.twiml.Response()
  with resp.dial(method="POST") as d:
    d.conference(name=confName, muted=True, beep=False,
                 statusCallbackEvent="join leave", statusCallback="/host/conference",
                 statusCallbackMethod="POST")

  return str(resp)

@app.route("/host/conference", methods=['GET', 'POST'])
def handle_conference():
  global robotCallSid
  global customerServiceCallSid
  global customerCallSid
  callSid = request.values.get("CallSid")
  event = request.values.get("StatusCallbackEvent")
  userNumber = customerNumber
  if callSid == customerCallSid:
    if event == "participant-leave":
      # bring the robot online
      print "bring robot online"
      client.calls.create(to=robotNumber, from_=hostNumber,
                          url=hostUrl + "/host/%s/robot" % userNumber)

      # send a message to customer
      client.messages.create(to=userNumber, from_=hostNumber,
                             body="Waiter is still waiting on the call. Reply anything to make it stop.")

  return ""

#@app.route("/robot", methods=['GET', 'POST'])
#def handle_robot_entrance():
#    resp = twilio.twiml.Response()
#    resp.gather(numDigits=11, action="/robot/record", timeout=10, method="POST")
#    resp.say("Must input the customer's phone number first")
#    return str(resp)

@app.route("/robot", methods=['GET', 'POST'])
def handle_robot_record():
    global robotSidToUserNumber
    resp = twilio.twiml.Response()
    recording_url = request.values.get("RecordingUrl", None)
    user_number = customerNumber
    #user_number = request.values.get("Digits", None)
    #sid = request.values.get("CallSid")
    #if user_number:
    #  robotSidToUserNumber[ sid ] = "+%s" % user_number
    #else:
    #  user_number = robotSidToUserNumber[ sid ]
    #print user_number

    if recording_url:
        print recording_url
        transcript = recognize_speech(recording_url)
        print transcript
        if transcript:
            triggered = False
            for word in triggerWords:
                if word in transcript.lower():
                    triggered = True
                    break
            if triggered:
                resp.say("I'm a voice assistant robot. Please hold on for a few seconds while I wake up my master.")
                client.calls.create(to=user_number, from_=hostNumber,
                                    url=hostUrl + "/host/%s/customer" % user_number)
                return str(resp)

    resp.say("Hello? Can you hear me?")
    resp.record(maxLength="2", action="/robot", playBeep=False)
    return str(resp)

@app.route("/message", methods=['GET', 'POST'])
def handle_message():
    global customerServiceCallSid
    if customerServiceCallSid != None:
      try:
        client.calls.update(customerServiceCallSid, status="completed")
      except:
        pass

    return ""

if __name__ == "__main__":
    app.run(debug=True)
