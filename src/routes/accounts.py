from flask import Flask
from flask_restplus import Resource
from src.server.instance import server
from src.database.tables import account_table_update
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
        self._name = self._response['name']
        self._initial_deposit = float(self._response['initial_deposit']) if type(self._response['initial_deposit']) == int else self._response['initial_deposit']
        self._balance = float(self._initial_deposit)

        if self._initial_deposit < 0 or type(self._initial_deposit) != float:
            return {'message': '\'initial_deposit\' has to be a float bigger or equals zero'}, 500
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
        if self._id not in account_table_update()['id']:
            return {'message': f'ID {self._id} not found'}, 404
        else:
            return account_table_update()['id'][self._id], 200

@api.route('/accounts/<string:name>', methods = ['GET'])
class AccountsByName(Resource):
    def get(self, name):
        self._name = name

        for i in account_table_update()['id']:
            if account_table_update()['id'][i]['name'] == self._name:
                return account_table_update()['id'][i], 200
        
        return {'message': f'name {self._name} has not been found'}, 404