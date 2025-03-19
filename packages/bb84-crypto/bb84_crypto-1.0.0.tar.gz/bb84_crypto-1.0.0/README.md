# bb84_crypto
I developed this package for crypto messagaing

it's easy to use. You would just need to install the package between your partner and go on :)

```
pip install bb84_crypto
```

```
from bb84_crypto import bb84_protocol, encrypt_message, decrypt_message
```

Here, generate a secret key using BB84 and share it with your partner<br>

```
key = bb84_protocol(n=128)
```

Then, write your message and encrypt it, then also can be decrypted
```
message = "Hi Bob! Wassuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuup ?"
encrypted = encrypt_message(message, key)
decrypted = decrypt_message(encrypted, key)
```

Of course you would need to print the magic

```
print(f"Decrypted: {decrypted}")
Hi Bob! Wassuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuup ?
```
