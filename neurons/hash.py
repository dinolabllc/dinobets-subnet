import dinobets.config as config
import hashlib
import hmac

def salt_with_new_seed(serverSeed: str, newSeed: str):        
    hash_value = hmac.new(key=str(newSeed).encode(), msg=str(serverSeed).encode(), digestmod=hashlib.sha512).hexdigest()
    return hash_value

def salt_with_client_seed(serverSeed: str, clientSeed: str):
    hash_value = hmac.new(key=str(serverSeed).encode(), msg=str(clientSeed).encode(), digestmod=hashlib.sha512).hexdigest()
    return hash_value

def salt(serverSeed: str) -> str:
    hash_value = hashlib.sha512(serverSeed.encode()).hexdigest()
    return hash_value

def generate_hash(
    client_seed: str,
    nonce: int,
    round_id: str,
):
    nonce_seed = client_seed + "-" + str(nonce)
    server_seed = salt_with_new_seed(config.SEVER_SEED, round_id)
    hash = salt_with_new_seed(server_seed, nonce_seed) 
    server_hash = salt(server_seed)
    return { "round_id":round_id, "server_hash":server_hash, "server_seed":server_seed, "hash": hash }
