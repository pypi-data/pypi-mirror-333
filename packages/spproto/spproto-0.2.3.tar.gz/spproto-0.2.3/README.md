# Secure Peer Protocol (SPP)

## Description

Chat with friends in a truly cryptographically secure way.

Intended to work as 5th OSI layer usually on top of TCP/IP.

[Rust version](https://github.com/lifr0m/spproto-rs)

### Mechanism

1. shared key is obtained using ECDHE. Transferred DH public keys are
signed and verified with pre-obtained Ed25519 public keys.
2. auth key is derived from shared key using ConcatKDF.
3. Message using ChaCha20-Poly1305 with auth key.

## Preparation before using

1. Generate private key, give your public key to friend.
2. Get friend's public key through reliable channel.

```python
from pathlib import Path
from spproto.key import generate_private_key, get_public_key

def main() -> None:
    privkey_path = Path('~/Desktop/privkey').expanduser()
    pubkey_path = Path('~/Desktop/pubkey').expanduser()
    
    privkey = generate_private_key()
    pubkey = get_public_key(privkey)
    
    privkey_path.write_bytes(privkey)
    pubkey_path.write_bytes(pubkey)

main()
```

## How to use

### Client

Connect to your friend

```python
import asyncio
from pathlib import Path
from spproto.client import connect

async def main() -> None:
    privkey = Path('~/Desktop/privkey').expanduser().read_bytes()
    peer_pubkey = Path('~/Desktop/friend_pubkey').expanduser().read_bytes()

    host = '1.2.3.4'
    port = 4321
    async with connect(host, port, privkey, peer_pubkey) as conn:
        await conn.send(b'Hello, server!')
        print(await conn.receive())

asyncio.run(main())
```

### Server

Make your friend available to connect to you.

```python
import asyncio
from pathlib import Path
from spproto.connection import Connection
from spproto.server import serve

async def callback(
    conn: Connection
) -> None:
    print(await conn.receive())
    await conn.send(b'Hello, client')

async def main() -> None:
    privkey = Path('~/Desktop/privkey').expanduser().read_bytes()
    peer_pubkey = Path('~/Desktop/friend_pubkey').expanduser().read_bytes()

    host = '1.2.3.4'
    port = 4321
    await serve(host, port, privkey, peer_pubkey, callback)

asyncio.run(main())
```
