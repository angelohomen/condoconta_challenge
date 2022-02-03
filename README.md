API documentation: https://bank-api-doc-pg6lpv4v5-angelohomen.vercel.app/

Bank API is a system developed to simulate a bank system. It is composed by list of accounts and transfers history. You can POST new accounts giving as parameters the customers name and its initial deposit. You also can POST a transfer based on customers ID's. You'll just send the ID from who's transfering, ID of the one who's receiving the money and how much money will be transfered. This event will automatically append to transfer history database, update accounts balances and generate a transfer ID, which is very important to maintain control and data to facilitate searching. Talking about searching, it is possible to search some informations like:

- Account initial deposit and balance by ID;
- Account initial deposit and balance by owner's name;
- Accounts history transfers by ID;
- Accounts history transfers by name;
- Account balance by ID;
- Account balance by name;
- All of this can be returned by adding '/{information}' to the base link.

Here is an example: If you want to know how much money is in account with ID 4, you just want to apply GET at: http://127.0.0.1:5000/balance/4

And that's it! It will return the account balance.

More detailed information is given by each method description.

Enjoy it!