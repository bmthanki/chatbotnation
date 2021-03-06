import json
import os
import logging
from flask import Flask
from flask import make_response
from flask import request
from db.mysql import *
from service.service import verify_nick_name
from service.service import verify_email_id
from service.service import get_schedule_details
from service.service import save_friend
from service.service import insert_event
from service.service import insert_into_schtable
from service.service import user_greetings
from service.service import insert_into_schtable
from service.service import insert_into_teammap
from service.service import insert_into_team

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
dbconnect()



@app.route('/', methods=['POST'])
def chatbot_facade():
    req = request.get_json(silent=True, force=True)

    logger.info("Entry:Chatbot Facade")
    print("Input Json:")
    print(json.dumps(req, indent=4, sort_keys=True))

    if req.get("result").get("action") == "check_nick_name":
        parameters= req.get("result").get("parameters")
        facebook_id=req.get("originalRequest").get("data").get("sender").get("id")
        name=parameters.get("given-name")
        res=verify_nick_name(name,facebook_id)
    elif req.get("result").get("action") == "check_email":
        parameters = req.get("result").get("parameters")
        email = parameters.get("email")
        print(email)
        res = verify_email_id(email)
    elif req.get("result").get("action") == "save_email":
        parameters =  req.get("result").get("parameters")
        facebook_id = req.get("originalRequest").get("data").get("sender").get("id")
        email = parameters.get("email")
        name = parameters.get("given-name2")
        res = save_friend(facebook_id, email, name)
    elif req.get("result").get("action") == "check_schedule":
        parameters = req.get("result").get("parameters")
        email= parameters.get("email")
        print(email)
        name= parameters.get("given-name")
        date= parameters.get("date")
        period = parameters.get("Period")
        duration= parameters.get("duration").get("amount")
        res= get_schedule_details(email,name,date,period,duration)
    elif req.get("result").get("action") == "final_step":
        facebook_id = req.get("originalRequest").get("data").get("sender").get("id")
        print(facebook_id)
        parameters = req.get("result").get("parameters")
        name = parameters.get("given-name")
        email = parameters.get("email")
        date = parameters.get("date")
        duration = parameters.get("duration")
        duration_amount = duration.get("amount")
        application = parameters.get("application")
        start_time = parameters.get("time1")
        print(start_time)
        speech = insert_into_schtable(date,facebook_id,duration_amount,application,start_time,email,name)
        res = {
            "speech": speech,
            "displayText": speech,
            "data": {"facebook": {
                "text": speech
            }},
            # "contextOut": [],
            "source": "Test"
        }
    elif req.get("result").get("action") == "user_greet":
        new_facebook_id = req.get("originalRequest").get("data").get("sender").get("id")
        print(new_facebook_id)
        speech = user_greetings(new_facebook_id)
        res = {
            "speech": speech,
            "displayText": speech,
            "data": {"facebook": {
                "text": speech
            }},
            # "contextOut": [],
            "source": "Test"
        }
    elif req.get("result").get("action") == "get_all_params":
        facebook_id = req.get("originalRequest").get("data").get("sender").get("id")
        parameters = req.get("result").get("parameters")
        name = parameters.get("given-name")
        email = parameters.get("email")
        date = parameters.get("date")
        duration = parameters.get("duration")
        duration_amount = duration.get("amount")
        application = parameters.get("application")
        start_time = parameters.get("time1")
        print(start_time)
        res = insert_into_schtable(date, facebook_id, duration_amount, application, start_time, email, name)
    elif req.get("result").get("action") == "team_details":


    #        print(email)
        facebook_id = req.get("originalRequest").get("data").get("sender").get("id")
        parameters = req.get("result").get("parameters")
        team_name = parameters.get("team-name")
        email = parameters.get("email2")
        length = len(email)
        if team_name != ' ':
            email1 = ""
            for i in range(0, length):
                email1 = email[i]
                speech = insert_into_teammap(facebook_id, email1)
                i += i
                print(email1)
            speech = insert_into_team(facebook_id, team_name)
            res = {
                "speech": speech,
                "displayText": speech,
                "data": {"facebook": {
                    "text": speech
                }},
                # "contextOut": [],
                "source": "Test"
            }

    else:
        res = {}

    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    #print(r)
    logger.info("Exit:Chatbot Facade")
    return r



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ['PORT']))
    #app.run()
