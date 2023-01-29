from app import app
from flask import jsonify, make_response,request
import json
from app.models.models import Subscription
from app.models.models import db
from datetime import datetime, timedelta
import requests


@app.route('/api/v1/subscriptions/create/', methods=['POST'])
def create_subscription():
    data = request.json
    if not data:
        return make_response(jsonify({'message': 'No data provided'}), 400)
    if not data["discord"]:
        return make_response(jsonify({'message': 'No username provided'}), 400)
    if not data["days"]:
        return make_response(jsonify({'message': 'No expiration date provided'}), 400)
    if data["days"]<=0:
        return make_response(jsonify({'message': 'Expiration date cannot be less than 1'}), 400)
    if data["days"] != 30:
        return make_response(jsonify({'message': 'Expiration date must be 30 days, 90 days, or 120 days'}), 400)
    if not data["payment_id"]:
        return make_response(jsonify({'message': 'No payment id provided'}), 400)   


    pid=data["payment_id"]
    resp=requests.get(f"https://api.nowpayments.io/v1/payment/{pid}", headers={"x-api-key": "1A23V53-YYE4CR3-HVPF3V1-P842NZH"}).json()

    #check if payment is completed

    if resp["payment_status"]!="confirmed ":
        return make_response(jsonify({'message': 'Payment is not confirmed'}), 400)



    sub=Subscription.query.filter_by(username=data["discord"])
    if sub:
        if sub.expiration_date<datetime.now():
            db.session.delete(sub) 
            db.session.commit()




    subscription=Subscription(username=data["discord"], expiration_date=datetime.now()+timedelta(days=data["days"]), payment_id=pid)
    db.session.add(subscription)
    db.session.commit()
    return make_response(jsonify({'message': 'Subscription created'}), 200)





@app.route('/api/v1/subscriptions/', methods=['GET'])
def get_subscriptions():
    data=request.json

    if data["username"]=="all":
        subs=[]
        for sub in Subscription.query.all():
            subs.append(
            {
                "id":sub.id,
                "username":sub.username,
                "expiration_date":str(sub.expiration_date.strftime("%Y-%m-%d %H:%M:%S")),
                "payment_id":sub.payment_id
            }



            )
        return make_response(jsonify({"subs":subs}),200)
    else:
        sub=Subscription.query.filter_by(username=data["username"]).first()
        if sub:
            return make_response(jsonify({
                "id":sub.id,
                "username":sub.username,
                "expiration_date":str(sub.expiration_date.strftime("%Y-%m-%d %H:%M:%S")),
                "payment_id":sub.payment_id
            
            }),200)
        else:
            return make_response(jsonify({"message":"Subscription not found"}),404)




