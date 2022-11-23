import time

from queue import Empty

from mongoDB import MongoDB
from random import choice


def choose_winner(announcements, My_Lock, temp_blocks, validators, block_chain):
    time.sleep(2)
    while True:
        with My_Lock:
            temp = temp_blocks
        lottery_pool = []
        if temp:
            for block in temp:
                if block["Validator"] not in lottery_pool:
                    set_validators = validators
                    k = set_validators.get(block["Validator"])
                    if k:
                        for i in range(k):
                            lottery_pool.append(block["Validator"])
            lottery_winner = choice(lottery_pool)
            print(lottery_winner)
            # add block of winner to blockchain and let all the other nodes known
            for block in temp:
                if block["Validator"] == lottery_winner:
                    with My_Lock:
                        MongoDB().insertOne('blockchain', block)
                        MongoDB().close_connect()
                        block_chain.append(block)
                    # write message in queue.
                    msg = "\n{0} Earns the right to generate a block\n".format(lottery_winner)
                    announcements.put(msg)
                    break
            # add one more record in lottery_pool(credit score + 1)
            validators[lottery_winner] += 1
            print(validators)
        with My_Lock:
            temp_blocks.clear()


def candidate(candidate_blocks, temp_blocks):
    """
    :param candidate_blocks:
    :return:
    """
    while True:
        try:
            candi = candidate_blocks.get(block=False)
        except Empty:
            time.sleep(5)
            continue
        temp_blocks.append(candi)
