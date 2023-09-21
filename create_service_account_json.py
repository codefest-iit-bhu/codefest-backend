import os

import pyAesCrypt
from dotenv import load_dotenv

load_dotenv()

encFileSize = os.stat("service_account.json.aes").st_size
with open("service_account.json.aes", "rb") as encrypted_file:
    with open("service_account.json", "wb") as decrypted_file:
        # decrypt file stream
        pyAesCrypt.decryptStream(
            encrypted_file,
            decrypted_file,
            os.getenv("SERVICE_ACCOUNT_DECRYPT_KEY", ""),
            64 * 1024,
            encFileSize,
        )
