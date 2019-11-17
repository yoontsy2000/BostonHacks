from flask import Flask, request, redirect, jsonify
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)



@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    resp = MessagingResponse()
    resp.message("Oui oui, Jean-Pierre received your message.")
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)