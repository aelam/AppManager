import base64
import plistlib
import hashlib

import M2Crypto


def gen_plist(csr, chain, signature):
    plist_dict = {
        'PushCertRequestCSR': csr,
        'PushCertCertificateChain': chain,
        'PushCertSignature': signature
    }

    plist = plistlib.writePlistToString(plist_dict)
    encoded_plist = base64.encodestring(plist)

    return plist, encoded_plist


def sign_csr(csr, key_path, passphrase, mdm_cert, intermediate_cert, root_cert):
    for key, value in locals().iteritems():
        if value is None:
            raise Exception('%s cannot be None' % key)

    digest = hashlib.sha1(csr).digest()
    private_key = M2Crypto.RSA.load_key(key_path, callback=lambda x: passphrase)
    s = private_key.sign(digest, 'sha1')
    signature = base64.encodestring(s)
    chain = '%s%s%s' % (mdm_cert, intermediate_cert, root_cert)

    return gen_plist(base64.encodestring(csr), chain, signature)
