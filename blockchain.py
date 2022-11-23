import json
import threading
from datetime import datetime
import time
from hashlib import sha256
from queue import Queue, Empty
from socketserver import ThreadingTCPServer, BaseRequestHandler
from mongoDB import MongoDB
from block import calculate_hash, check_valid, create_block
from pos import candidate, choose_winner

# need two queue
# 定义变量
block_chain = []
temp_blocks = []
candidate_blocks = Queue()  # 创建队列，用于线程间通信
announcements = Queue()
validators = {}
My_Lock = threading.Lock()


class HandleConn(BaseRequestHandler):
    def handle(self):
        print("Got connection from", self.client_address)
        # initial credit score = 10
        balance = 10
        t = str(datetime.now())
        address = sha256(t.encode()).hexdigest()
        validators[address] = balance
        print(validators)
        while True:
            announce_winner_t = threading.Thread(target=broadcast_winner, args=(announcements, self.request,),
                                                 daemon=True)
            announce_winner_t.start()
            self.request.send(b"\nEnter a new Transaction:")
            tx = self.request.recv(8192)
            try:
                tx = int(tx)
            except Exception as e:
                print(e)
                address = validators[address]
                del validators[address]
                break
            data = {
                "amount": tx,
                "owner": address
                    }
            MongoDB().insertOne('transactions', data)
            MongoDB().close_connect()
            for x in MongoDB().getlast('blockchain'):
                last_block = x
            MongoDB().close_connect()
            for x in MongoDB().getAll('transactions'):
                tx = x["tx"]
            MongoDB().close_connect()
            new_block = create_block(last_block, tx, address)
            if check_valid(new_block, last_block):
                print("new block is valid!")
                candidate_blocks.put(new_block)
            broadcast_blockchain_t = threading.Thread(target=broadcast_blockchain,
                                                      args=(self.request,), daemon=True)
            broadcast_blockchain_t.start()


def broadcast_winner(announcements, request):
    """
    :param announcements:
    :param request:
    :return:
    """
    while True:
        try:
            msg = announcements.get(block=False)
            request.send(msg.encode())
            request.send(b'\n')
        except Empty:
            time.sleep(3)
            continue


def broadcast_blockchain(request):
    """
    :param request:
    :return:
    """
    while True:
        time.sleep(15)
        with My_Lock:
            blockchain = []
            for x in MongoDB().getAll('blockchain'):
                blockchain.append(x)

            output = json.dumps(blockchain)
        try:
            request.send(output.encode())
            request.send(b'\n')
        except OSError:
            pass

def run():
    check = None
    for x in MongoDB().getAll('blockchain'):
        check = x
    MongoDB().close_connect()
    if check is None:
        t = str(datetime.now())
        genesis_block = {
            "Index": 0,
            "Timestamp": t,
            "TX": 0,
            "PrevHash": "",
            "Validator": ""
        }
        genesis_block["Hash"] = calculate_hash(genesis_block)
        print(genesis_block)
        block_chain.append(genesis_block)
        # TODO: done
        # put block_chain into MongoDB.
        MongoDB().insertOne('blockchain', genesis_block)
        MongoDB().close_connect()
    thread_canditate = threading.Thread(target=candidate, args=(candidate_blocks, temp_blocks), daemon=True)
    thread_pick = threading.Thread(target=choose_winner, args=(announcements, My_Lock, temp_blocks, validators,
                                                               block_chain), daemon=True)
    thread_canditate.start()
    thread_pick.start()
    # start a tcp server
    serv = ThreadingTCPServer(('', 9090), HandleConn)
    serv.serve_forever()


if __name__ == '__main__':
    run()