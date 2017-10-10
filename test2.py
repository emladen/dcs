import pprp
import base64

KEY_SIZE = 16
BLOCK_SIZE = 32


def encrypt(key, plaintext):
    key = key.encode('ascii')
    plaintext = plaintext.encode('utf-8')
    padded_key = key.ljust(KEY_SIZE, b'\0')

    sg = pprp.data_source_gen(plaintext, block_size=BLOCK_SIZE)
    eg = pprp.rjindael_encrypt_gen(padded_key, sg, block_size=BLOCK_SIZE)

    ciphertext = pprp.encrypt_sink(eg)

    encoded = base64.b64encode(ciphertext)

    return encoded.decode('ascii')


def decrypt(key, encoded):
    key = key.encode('ascii')
    padded_key = key.ljust(KEY_SIZE, b'\0')

    ciphertext = base64.b64decode(encoded.encode('ascii'))

    sg = pprp.data_source_gen(ciphertext, block_size=BLOCK_SIZE)
    dg = pprp.rjindael_decrypt_gen(padded_key, sg, block_size=BLOCK_SIZE)

    return pprp.decrypt_sink(dg).decode('utf-8')


key = 'MyKey'
text = 'test'

encoded = encrypt(key, text)
print(repr(encoded))
# prints 'ju0pt5Y63Vj4qiViL4VL83Wjgirq4QsGDkj+tDcNcrw='

decoded = decrypt(key, encoded)
print(repr(decoded))
# prints 'test'