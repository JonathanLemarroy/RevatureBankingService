import json
import logging
from math import inf

from flask import Flask, request

from services.bankingservice import BankingService

app = Flask(__name__)
app.config["DEBUG"] = True

logging.basicConfig(filename="records.log", level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(message)s')

banking_service = BankingService()


@app.route('/clients', methods=['POST'])
def create_client():
    try:
        json_dict = json.loads(request.data)
        first_name = None
        last_name = None
        for k, v in json_dict.items():
            if k == "firstName":
                first_name = str(v)
            if k == "lastName":
                last_name = str(v)
        return banking_service.create_client(first_name, last_name)
    except Exception as e:
        print(str(e))
        return "Error parsing body of request", 400


@app.route('/clients', methods=['GET'])
def get_all_clients():
    return banking_service.get_all_clients()


@app.route('/clients/<client_id>', methods=['GET'])
def get_client(client_id: str):
    return banking_service.get_client(int(client_id))


@app.route('/clients/<client_id>', methods=['PUT'])
def update_client(client_id: str):
    try:
        json_dict = json.loads(request.data)
        f_name = None
        l_name = None
        for k, v in json_dict.items():
            if k == "firstName":
                f_name = str(v)
            elif k == "lastName":
                l_name = str(v)
        return banking_service.update_client(int(client_id), f_name, l_name)
    except Exception as e:
        print(str(e))
        return "Error parsing body of request", 400


@app.route('/clients/<client_id>', methods=['DELETE'])
def delete_client(client_id: str):
    return banking_service.remove_client(int(client_id))


@app.route('/clients/<client_id>/accounts', methods=['POST'])
def create_account(client_id: str):
    try:
        json_dict = json.loads(request.data)
        account_type = None
        for k, v in json_dict.items():
            if k == "accountType":
                account_type = str(v)
        if account_type is None:
            return f"Missing accountType in body", 400
        return banking_service.create_account(int(client_id), account_type)
    except Exception as e:
        print(str(e))
        return "Error parsing body of request", 400


@app.route('/clients/<client_id>/accounts', methods=['GET'])
def get_accounts(client_id: str):
    try:
        min_bal = 0.0
        max_bal = inf
        for k, v in request.args.items():
            if k == "amountLessThan":
                max_bal = int(v)
            elif k == "amountGreaterThan":
                min_bal = int(v)
        return banking_service.get_accounts(int(client_id), min_bal, max_bal)
    except Exception as e:
        print(str(e))
        return "Error parsing body of request", 400


@app.route('/clients/<client_id>/accounts/<account_id>', methods=['GET'])
def get_account(client_id: str, account_id: str):
    return banking_service.get_account(int(client_id), int(account_id))


@app.route('/clients/<client_id>/accounts/<account_id>', methods=['PUT'])
def update_account(client_id: str, account_id: str):
    try:
        json_dict = json.loads(request.data)
        account_type = None
        balance = None
        for k, v in json_dict.items():
            if k == "accountType":
                account_type = str(v)
            elif k == "balance":
                balance = float(v)
        return banking_service.update_account(int(client_id), int(account_id), account_type, balance)
    except Exception as e:
        print(str(e))
        return "Error parsing body of request", 400


@app.route('/clients/<client_id>/accounts/<account_id>', methods=['DELETE'])
def delete_account(client_id: str, account_id: str):
    return banking_service.remove_account(int(client_id), int(account_id))


@app.route('/clients/<client_id>/accounts/<account_id>', methods=['PATCH'])
def update_balance(client_id: str, account_id: str):
    try:
        json_dict = json.loads(request.data)
        total = 0
        for k, v in json_dict.items():
            if k == "deposit":
                total += int(v)
            elif k == "withdraw":
                total += -1 * int(v)
        return banking_service.update_balance(int(client_id), int(account_id), total)
    except Exception as e:
        print(str(e))
        return "Error parsing body of request", 400


@app.route('/clients/<client_id>/accounts/<account_from_id>/transfer/<account_to_id>', methods=['PATCH'])
def transfer_balance(client_id: str, account_from_id: str, account_to_id: str):
    try:
        json_dict = json.loads(request.data)
        funds = 0
        for k, v in json_dict.items():
            if k == "amount":
                funds += int(v)
        return banking_service.transfer_funds(int(client_id), int(account_from_id), int(account_to_id), funds)
    except Exception as e:
        print(str(e))
        return "Error parsing body of request", 400


if __name__ == "__main__":
    app.run()
