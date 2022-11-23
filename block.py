from datetime import datetime
from hashlib import sha256



def create_block(prevblock, tx, address):
    """
    :param prevblock:
    :param tx:
    :param address:
    :return:
    """
    newblock = {
        "Index": prevblock["Index"] + 1,
        "TX": tx,
        "Timestamp": str(datetime.now()),
        "PrevHash": prevblock["Hash"],
        "Validator": address
    }

    newblock["Hash"] = calculate_hash(newblock)
    return newblock


def calculate_hash(block):
    record = "".join([
        str(block["Index"]),
        str(block["TX"]),
        block["Timestamp"],
        block["PrevHash"]
    ])

    return sha256(record.encode()).hexdigest()


def check_valid(newblock, prevblock):
    """
    :param newblock:
    :param prevblock:
    :return:
    """

    if prevblock["Index"] + 1 != newblock["Index"]:
        return False

    if prevblock["Hash"] != newblock["PrevHash"]:
        return False

    if calculate_hash(newblock) != newblock["Hash"]:
        return False

    return True