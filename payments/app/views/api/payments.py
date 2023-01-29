from app import app
from flask import jsonify, make_response,request
import requests
import json


@app.route('/api/v1/payments/', methods=['POST'])
def create_payment():
        json_data=request.json
        price=json_data["price"]
        if not price:
            return make_response(jsonify({"error":"Price is required"}), 400)

        payment_create={
        "price_amount": price,
        "price_currency": "eur",
        "pay_currency": "ada"
        }

        payment_json=requests.post(f"https://api.nowpayments.io/v1/payment/", headers={"x-api-key": "1A23V53-YYE4CR3-HVPF3V1-P842NZH", "Content-Type":"application/json"}, data=json.dumps(payment_create))
        return make_response(jsonify(payment_json.text), 200)


@app.route("/api/v1/payments/<int:id>",methods=["GET"])
def get_payment(id):
    payment_json=requests.get(f"https://api.nowpayments.io/v1/payment/{id}", headers={"x-api-key": "1A23V53-YYE4CR3-HVPF3V1-P842NZH"})
    return make_response(jsonify(payment_json.text), 200)
