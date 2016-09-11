from flask import Flask, request, redirect
import twilio.twiml
import twilio.rest

@app.route("/host", methods=['GET', 'POST'])
def handle_host_entrance():
  global robotSidToUserNumber
  userNumber = request.values.get('From', None)
  # make the call to customer service
  call = client.calls.create(to=customerServiceNumber, from_=hostNumber,
                             url=hostUrl + "/host/%s/customer_service" % userNumber)

  # make the call to the robot
  call = client.calls.create(to=robotNumber, from_=hostNumber,
                             url=hostUrl + "/host/%s/robot" % userNumber)

  robotSidToUserNumber[ call.sid ] = userNumber

  confName = "conf-%s" % userNumber
  print "send user to conference %s" % confName

  resp = twilio.twiml.Response()
  resp.say("Welcome")
  with resp.dial(method="POST") as d:
    d.conference(name=confName, muted=False)

  return str(resp)

@app.route("/host/<userNumber>/customer_service", methods=['GET', 'POST'])
def handle_host_call_customer_service(userNumber):
  confName = "conf-%s" % userNumber
  print "send customer service to conference %s" % confName

  resp = twilio.twiml.Response()
  resp.say("Welcome Customer Representative")
  with resp.dial(method="POST") as d:
    d.conference(name=confName, muted=False, endConferenceOnExit=True)

  return str(resp)

@app.route("/host/<userNumber>/robot", methods=['GET', 'POST'])
def handle_host_call_robot(userNumber):
  confName = "conf-%s" % userNumber
  print "send robot to conference %s" % confName

  resp = twilio.twiml.Response()
  resp.say("Welcome Robot")
  with resp.dial(method="POST") as d:
    d.conference(name=confName, muted=False)

  return str(resp)
