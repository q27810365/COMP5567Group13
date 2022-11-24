import json

from mongoDB import MongoDB


def findaddr(i):
    cursor = MongoDB().get('transactions', {'from': i})
    tx = []
    count = 100
    for x in cursor:
        tx.append(x)
        count += 1

    MongoDB().close_connect()
    return tx, count



if __name__ == '__main__':
    i = input('Please input the transactions you want to query: ')
    res = findaddr(i)

    print(res[0])
    print('Your credit point is ' + str(res[1]))