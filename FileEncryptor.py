from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os,sys

# Fetch the key and encrypt with Password
def DeriveKey(Password: str, Salt: bytes) -> bytes:
    Kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=32,
        salt=Salt,
        iterations=100000,
        backend=default_backend()
    )
    return Kdf.derive(Password.encode())

# Encrypt provided Input to Output using Password to encrypt
def Encrypt(Input: str, Output: str, Password: str) -> None:
    try:
        Salt = os.urandom(16)
        Iv = os.urandom(16)
        Key = DeriveKey(Password, Salt)
        Ciph = Cipher(algorithms.AES(Key), modes.CBC(Iv), backend=default_backend())
        Encryptor = Ciph.encryptor()
        Padder = padding.PKCS7(algorithms.AES.block_size).padder()

        with open(Input,"rb") as File:
            Data = File.read()

        PaddedData = Padder.update(Data) + Padder.finalize()
        CiphText = Encryptor.update(PaddedData) + Encryptor.finalize()

        with open(Output,"wb") as File:
            File.write(Salt + Iv + CiphText)
    except FileNotFoundError:
        print(f"{Input} not found.")
        sys.exit(1)
    except Exception as Exceptor:
        print(f"Exceptor received, {Exceptor}")
        sys.exit(1)

# Decrypt Input to Output using Password to unlock
def Decrypt(Input: str, Output: str, Password: str) -> None:
    try:
        with open(Input,"rb") as File:
            Data = File.read()

        Salt = Data[:16]
        Iv = Data[16:32]
        CiphText = Data[32:]
        Key = DeriveKey(Password, Salt)

        Ciph = Cipher(algorithms.AES(Key), modes.CBC(Iv), backend=default_backend())
        Decryptor = Ciph.decryptor()
        Padder = padding.PKCS7(algorithms.AES.block_size).unpadder()

        PaddedData = Decryptor.update(CiphText) + Decryptor.finalize()
        Data = Padder.update(PaddedData) + Padder.finalize()

        with open(Output,"wb") as File:
            File.write(Data)
    except ValueError:
        print("Incorrect password or corrupted file(s)")
        sys.exit(1)
    except FileNotFoundError:
        print(f"{Input} not found.")
        sys.exit(1)
    except Exception as Exceptor:
        print(f"Exceptor received, {Exceptor}")
        sys.exit(1)
    
if __name__ == "__main__":
    Task = input("Task (enc/dec)\n$ ").lower()
    if Task not in ["enc", "dec"]: print("Invalid task. Please choose 'enc' for encryption or 'dec' for decryption.") ; sys.exit(1)
    File = input("File\n$ ")
    if not os.path.isfile(File): print(f"{File} doesn't exist.") ; sys.exit(1)
    if Task == "enc":
        Password = input("Password\n$ ")
        Output = File + ".enc"
        Encrypt(File, Output, Password)
    elif Task == "dec":
        if not File.endswith(".enc"):
            print("File must end with .enc to decode.")
            sys.exit(1)
        Password = input("Password\n$ ")
        Output = File[:-4]
        Decrypt(File, Output, Password)