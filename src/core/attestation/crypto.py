import json
from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder

class AttestationSigner:
    def __init__(self, k): self._sk=SigningKey(k, encoder=HexEncoder)
    def sign(self,p): d=json.dumps(p,sort_keys=True).encode(); s=self._sk.sign(d).signature; return {'payload':p,'signature':s.hex(),'public_key':self._sk.verify_key.encode(encoder=HexEncoder).decode()}
