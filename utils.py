import hashlib
import Cryptodome.Random.random
from base58 import b58decode, b58encode
from fastecdsa import keys, curve, ecdsa
from fastecdsa.encoding.pem import PEMEncoder
from fastecdsa.encoding.der import DEREncoder


def sha256(pattern) -> str:
    if not isinstance(pattern, (bytes, bytearray, str)):
        raise TypeError("pattern should be bytes, bytearray or string")
    if isinstance(pattern, str):
        pattern = pattern.encode("utf-8")
    return hashlib.sha256(pattern).hexdigest()


def ripemd160(pattern) -> str:
    if not isinstance(pattern, (bytes, bytearray, str)):
        raise TypeError("pattern should be bytes, bytearray or string")
    if isinstance(pattern, str):
        pattern = pattern.encode("utf-8")
    return hashlib.new("ripemd160", pattern).hexdigest()


def sign(input, prkey) -> dict:
    r, s = ecdsa.sign(input.encode('utf-8'), prkey, curve.P256)
    signaturepoint = DEREncoder.encode_signature(r, s)
    pukey = keys.get_public_key(prkey, curve.P256)
    pukey = PEMEncoder.encode_public_key(pukey)
    pack = {
        'signature': b58encode(signaturepoint).decode('utf-8'),
        'publickey': pukey,
    }
    return pack

def verify(input, pack, address) -> bool:
    signature = b58decode(pack['signature'])
    publickey = pack['publickey']
    publickey = ripemd160(sha256(publickey))
    try:
        pubkey = b58decode(address).decode('utf-8')
    except ValueError as e:
        print('Wrong Address')
        return False
    if pubkey != publickey:
        print('Hash wrong')
        return False
    orignalSignature = DEREncoder.decode_signature(signature)
    orignalPublicKey = PEMEncoder.decode_public_key(pack['publickey'], curve.P256)
    return ecdsa.verify(orignalSignature, input.encode('utf-8'), orignalPublicKey, curve.P256)


def randomSort(stakeholders: list):
    return Cryptodome.Random.random.shuffle(stakeholders)