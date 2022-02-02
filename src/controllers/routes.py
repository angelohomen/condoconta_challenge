from flask import Flask, request
from flask_restplus import Resource
from src.server.instance import server
from src.database.tables import account_table_update, transfer_table_update
import csv

app = server.app
api = server.api

@api.route('/accounts', methods = ['GET', 'POST'])
class Accounts(Resource):
    def get(self, ):
        if len(account_table_update()['id']) < 1:
            return {'message': f'No registered account'}, 404
        else:
            return account_table_update(), 200

    def post(self, ):
        self._response = api.payload

        if not self._response:
            return {'message': 'error'}, 500

        bigger_id = 0

        for i in account_table_update()['id']:
            i = int(i)
            if i > bigger_id:
                bigger_id = i
            else:
                bigger_id = bigger_id

        self._id = bigger_id + 1
        self._name = str(self._response['name'])
        self._initial_deposit = float(self._response['initial_deposit'])
        self._balance = float(self._initial_deposit)

        if self._initial_deposit <= 0 or type(self._initial_deposit) != float:
            return {'message': '\'initial_deposit\' has to be a float bigger than zero'}, 500
        if self._name == "string" or self._name == '' or type(self._name) != str:
            return {'message': 'insert a valid name'}, 500

        self._fieldnames = ['id', 'name', 'initial_deposit', 'balance']

        with open('src/database/ACCOUNTS_DATABASE.csv', 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self._fieldnames)
            writer.writerow({'id': self._id, 'name': self._name, 'initial_deposit': self._initial_deposit, 'balance': self._balance})

        return {'id': self._id}, 200

@api.route('/accounts/<int:id>', methods = ['GET'])
class AccountsByID(Resource):
    def get(self, id):
        self._id = id
        return account_table_update()['id'][self._id], 200

@api.route('/accounts/<string:name>', methods = ['GET'])
class AccountsByName(Resource):
    def get(self, name):
        self._name = name

        for i in account_table_update()['id']:
            if account_table_update()['id'][i]['name'] == self._name:
                return account_table_update()['id'][i], 200
        
        return {'message': f'name {self._name} has not been found'}, 404

@api.route('/transfers', methods = ['GET', 'POST'])
class Transfer(Resource):
    def get(self, ):
        if len(transfer_table_update()['transfer_id']) < 1:
            return {'message': f'No registered transfer'}, 404
        else:
            return transfer_table_update(), 200

    def post(self, ):
        self._response = api.payload
        self._bigger_id = 0

        if not self._response:
            return {'message': 'error'}, 500

        for i in transfer_table_update()['transfer_id']:
            i = int(i)
            if i > self._bigger_id:
                self._bigger_id = i
            else:
                self._bigger_id = self._bigger_id

        self._transfer_id = int(self._bigger_id) + 1
        self._from_id = int(self._response['from_id'])
        self._to_id = int(self._response['to_id'])
        self._transfer_value = float(self._response['transfer_value'])

        if self._from_id == self._to_id:
            return {'message': '\'from_id\' and \'to_id\' have same values'}, 500
        if self._from_id <= 0 or type(self._from_id) != int:
            return {'message': '\'from_id\' has to be an integer bigger than zero'}, 500
        if self._to_id <= 0 or type(self._from_id) != int:
            return {'message': '\'to_id\' has to be an integer bigger than zero'}, 500
        if self._transfer_value <= 0 or type(self._transfer_value) != float:
            return {'message': '\'transfer_value\' has to be a float bigger than zero'}, 500

        self._fieldnames = ['transfer_id', 'from_id', 'to_id', 'transfer_value']

        if self._from_id not in account_table_update()['id']:
            return {'message': f'ID {self._from_id} does not exist'}, 404
        elif self._to_id not in account_table_update()['id']:
            return {'message': f'ID {self._to_id} does not exist'}, 404
        else:
            with open('src/database/TRANSFERS_DATABASE.csv', 'a', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=self._fieldnames)
                writer.writerow({'transfer_id': self._transfer_id, 'from_id': self._from_id, 'to_id': self._to_id, 'transfer_value': self._transfer_value})

            self._fieldnames = ['id', 'name', 'initial_deposit', 'balance']
            self._from_name = ''
            self._from_initial_deposit = 0.0
            self._from_balance = 0.0
            self._to_name = ''
            self._to_initial_deposit = 0.0
            self._to_balance = 0.0
            self._new_list = []

            with open('src/database/ACCOUNTS_DATABASE.csv') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                csv_list = list(csv_reader)
                for rows in csv_list:
                    for keys in rows:
                        if keys == 'id':
                            if rows[keys] == str(self._from_id):
                                self._from_id = int(rows['id'])
                                self._from_name = str(rows['name'])
                                self._from_initial_deposit = float(rows['initial_deposit'])
                                self._from_balance = float(rows['balance']) - self._transfer_value
                                self._new_list.append({'id': self._from_id, 'name': self._from_name, 'initial_deposit': self._from_initial_deposit, 'balance': self._from_balance})
                                continue
                            elif rows[keys] == str(self._to_id):
                                self._to_id = int(rows['id'])
                                self._to_id = int(rows['id'])
                                self._to_name = str(rows['name'])
                                self._to_initial_deposit = float(rows['initial_deposit'])
                                self._to_balance = float(rows['balance']) + self._transfer_value
                                self._new_list.append({'id': self._to_id, 'name': self._to_name, 'initial_deposit': self._to_initial_deposit, 'balance': self._to_balance})
                                continue
                            else:
                                self._new_list.append({'id': int(rows['id']), 'name': str(rows['name']), 'initial_deposit': float(rows['initial_deposit']), 'balance': float(rows['balance'])})
                with open('src/database/ACCOUNTS_DATABASE.csv', 'w', newline='') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=self._fieldnames)
                    writer.writeheader()
                    for i in self._new_list:
                        writer.writerow(i)

                return {'transfer_id': self._transfer_id, 'from_id_new_balance': self._from_balance, 'to_id_new_balance': self._to_balance}, 200

@api.route('/transfers/<int:id>', methods = ['GET'])
class TransferHistoryByID(Resource):
    def get(self, id):
        self._id = id
        transfer_dict = {}
        index = 1

        for i in transfer_table_update()['transfer_id']:
            if transfer_table_update()['transfer_id'][i]['from_id'] == self._id:
                transfer_dict[index] = transfer_table_update()['transfer_id'][i]
                index += 1

        if len(transfer_dict) < 1:
            return {'message': f'ID {self._id} has no transfer history'}, 404
        else:
            return {'transfer_history': transfer_dict}, 200

@api.route('/transfers/<string:name>', methods = ['GET'])
class TransferHistoryByName(Resource):
    def get(self, name):
        self._name = name
        self._dict = {}
        self._id = 0

        for i in transfer_table_update()['transfer_id']:
            for j in account_table_update()['id']:
                if transfer_table_update()['transfer_id'][i]['from_id'] == j and account_table_update()['id'][j]['name'] == self._name:
                    self._dict[i] = transfer_table_update()['transfer_id'][i]

        if len(self._dict) < 1:
            return {'message': f'{self._name} does not have registered transfers'}, 404
        elif len(self._dict) > 1:
            return {'transfer_id': self._dict}, 200
        else:
            return {'transfer_id': self._dict}, 200

@api.route('/balance', methods = ['GET'])
class Balance(Resource):
    def get(self, ):
        self._account_balances = {}

        for i in account_table_update()['id']:
            self._account_balances[i] = account_table_update()['id'][i]['balance']

        if len(self._account_balances) < 1:
            return {'message': f'No registered account'}, 404
        else:
            return {'id': self._account_balances}, 200

@api.route('/balance/<int:id>', methods = ['GET'])
class BalanceByID(Resource):
    def get(self, id):
        self._id = id
        return {'balance': account_table_update()['id'][self._id]['balance']}, 200

@api.route('/balance/<string:name>', methods = ['GET'])
class BalanceByName(Resource):
    def get(self, name):
        self._name = name
        self._dict = {}
        self._id = 0

        for i in account_table_update()['id']:
            if account_table_update()['id'][i]['name'] == self._name:
                self._id = int(i)
                _balance = account_table_update()['id'][i]['balance']
                self._dict[self._id] = _balance

        if len(self._dict) < 1:
            return {'message': f'Name {self._name} does not exist'}, 404
        elif len(self._dict) > 1:
            return {'balance': {'id': self._dict}}, 200
        else:
            return {'balance': self._dict[self._id]}, 200