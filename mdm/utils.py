import M2Crypto
import os

def generate_certificate_signing_request(pkey=None, passphrase=None, common_name='localhost', country='US'):
    def callback(*args):
        pass

    if pkey is None:
        pkey = M2Crypto.EVP.PKey()
    elif isinstance(pkey, str):
        if os.path.isfile(pkey):
            pkey = M2Crypto.EVP.load_key(pkey, callback=lambda x: passphrase)
        else:
            pkey = M2Crypto.EVP.load_key_string(pkey, callback=lambda x: passphrase)
    else:
        raise Exception('Unknown pkey format. Should be a string or filepath.')

    req = M2Crypto.X509.Request()
    rsa = M2Crypto.RSA.gen_key(2048, 65537, callback)
    pkey.assign_rsa(rsa)
    rsa = None
    req.set_pubkey(pkey)
    name = req.get_subject()
    name.C = country
    name.CN = common_name

    req.sign(pkey, 'sha1')
    assert req.verify(pkey)

    pkey2 = req.get_pubkey()
    assert req.verify(pkey2)

    return req.as_der(), pkey.as_pem(callback=lambda x: passphrase)
