from flask import Flask
from flask_restplus import Resource
from src.server.instance import server
from src.database.tables import account_table_update
import csv

app = server.app
api = server.api

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
        if self._id not in account_table_update()['id']:
            return {'message': f'ID {self._id} not found'}, 404
        else:
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
            return {'message': f'Name {self._name} not registered'}, 404
        elif len(self._dict) > 1:
            return {'balance': {'id': self._dict}}, 200
        else:
            return {'balance': self._dict[self._id]}, 200