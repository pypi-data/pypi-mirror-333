import hashlib
import hmac

class signature:
    @staticmethod
    async def signature_valider_async(salt, id, signature):
        content = {
            "id": id,
            "signature": signature
        }

        id_value=content["id"]
        signature=content["signature"]

        salt = salt

        # Генерация хеша
        hash_string=f"{id_value}:{salt}"
        computed_hash=hashlib.sha1(hash_string.encode()).hexdigest()

        # Безопасное сравнение подписи
        if not hmac.compare_digest(computed_hash, signature):
            return False
        else:
            return True

    @staticmethod
    def signature_valider_sync(salt, id, signature):
        content = {
            "id": id,
            "signature": signature
        }

        id_value=content["id"]
        signature=content["signature"]

        salt = salt

        # Генерация хеша
        hash_string=f"{id_value}:{salt}"
        computed_hash=hashlib.sha1(hash_string.encode()).hexdigest()

        # Безопасное сравнение подписи
        if not hmac.compare_digest(computed_hash, signature):
            return False
        else:
            return True
        
    @staticmethod
    async def generete_signature_valider_async(salt, **kwargs):
        hash_string=str()
        for i in kwargs.keys():
            hash_string[i]+':'
        hash_string+=salt

        signature = hashlib.sha1(hash_string.encode()).hexdigest()


    @staticmethod
    def generete_signature_valider_sync(salt, **kwargs):
        hash_string=str()
        for i in kwargs.keys():
            hash_string+=f'{kwargs[i]}:'
        hash_string+=salt
        return hashlib.sha1(hash_string.encode()).hexdigest()

