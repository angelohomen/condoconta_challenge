import csv

def account_table_update():

    account_table = {}

    with open('src/database/ACCOUNTS_DATABASE.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for rows in csv_reader:
            index = int(rows['id'])
            corrected = {}
            name = ''
            initial_deposit = 0.0
            balance = 0.0
            for keys in rows:
                if keys == str('name'):
                    name = str(rows[keys])
                    continue
                elif keys == str('initial_deposit'):
                    initial_deposit = float(rows[keys])
                    continue
                elif keys == str('balance'):
                    balance = float(rows[keys])
                    corrected = {'name': name, 'initial_deposit': initial_deposit, 'balance': balance}
                    account_table[int(index)] = corrected

    return {'id': account_table}

def transfer_table_update():

    transfer_table = {}

    with open('src/database/TRANSFERS_DATABASE.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for rows in csv_reader:
            index = int(rows['transfer_id'])
            corrected = {}
            from_id = 0
            to_id = ''
            transfer_value = 0.0
            for keys in rows:
                if keys == str('from_id'):
                    from_id = int(rows[keys])
                    continue
                if keys == str('to_id'):
                    to_id = int(rows[keys])
                    continue
                elif keys == str('transfer_value'):
                    transfer_value = float(rows[keys])
                    corrected = {'from_id': from_id, 'to_id': to_id, 'transfer_value': transfer_value}
                    transfer_table[int(index)] = corrected

    return {'transfer_id': transfer_table}