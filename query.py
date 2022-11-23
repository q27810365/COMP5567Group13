import json

from mongoDB import MongoDB




def findaddr(i):
    cursor = MongoDB().get('transactions', {'owner': i})
    tx = []
    for x in cursor:
        tx.append(x)

    MongoDB().close_connect()
    return tx



if __name__ == '__main__':
    i = input('Please input the transactions you want to query: ')
    res = findaddr(i)
    print(res)