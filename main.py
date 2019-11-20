from flask import Flask, request
import logging
from httplib2 import Http
from json import dumps
import json
import os

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return ""

@app.route("/alerts", methods=["POST"])
def alerts():
    data = json.loads(request.get_data())
    logging.debug("Got data: %s", data)
    instance = data['alerts'][0]['labels']['instance']
    status = data['alerts'][0]['status']
    if status == "firing":
        img = "https://png.pngtree.com/svg/20161208/status_warning_336325.png"
    elif status == "resolved":
        img = "https://image.flaticon.com/icons/png/128/291/291201.png"
    else:
        img = "https://raw.githubusercontent.com/stefanprodan/openfaas-promq/master/logo.png"
    alertname = data['alerts'][0]['labels']['alertname']
    description = data['alerts'][0]['annotations']['description']
    job = data['alerts'][0]['labels']['job']
    sendMessage(instance, status, img, alertname, description, job)
    return "OK", 200

def sendMessage(instance, status, img, alertname, description, job):
    url = os.environ.get('TOKEN_URL').replace("\\", "")
    bot_message = {
            "cards": [
              { "header":
                { "title": "Prometheus:",
                  "subtitle": status,
                  "imageUrl": img,
                  "imageStyle": "IMAGE"
                },
                "sections": [
                  { "widgets": [
                    { "keyValue": {
                        "topLabel": "AlertName",
                        "content": alertname,
                        "contentMultiline": "true"
                      }
                    },
                    { "keyValue": {
                        "topLabel": "Instance",
                        "content": instance,
                        "contentMultiline": "true"
                      }
                    },
                    { "keyValue": {
                        "topLabel": "Description",
                        "content": description,
                        "contentMultiline": "true"
                      }
                    },
                    { "keyValue": {
                        "topLabel": "Job",
                        "content": job,
                        "contentMultiline": "true"
                      }
                    }
                  ]}
              ]}
            ]}
    message_headers = { 'Content-Type': 'application/json; charset=UTF-8'}
    http_obj = Http()

    response = http_obj.request(
        uri=url,
        method='POST',
        headers=message_headers,
        body=dumps(bot_message),
    )
    logging.debug(response)
if __name__ == "__main__":
    logging.basicConfig(level = logging.DEBUG)
    app.run(host='0.0.0.0', port=3000)
