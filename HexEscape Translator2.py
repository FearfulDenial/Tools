import string

def CleanKey(Key):
    if isinstance(Key, int):
        return Key % 256
    else:
        print(f"Not a key {Key}")
        return 0
def Clean(Data):
    Cleaned = ''.join(c for c in Data if c in string.printable)
    return Cleaned

def XORDecrypt(Data, Key):
        Key = CleanKey(Key)  # Clean the Key first
        if isinstance(Data, str):
            Data = Data.encode('utf-8')  # Convert string to bytes
        Decrypted = bytes([byte ^ Key for byte in Data])
        return Decrypted
def AttemptXOR(Data):

    if isinstance(Data, str):
        Data = Data.encode('utf-8')

    ByteData = list(Data)

    for Key in range(256):
        Decrypted = XORDecrypt(Data, Key)
        decrypted_str = Decrypted.decode('utf-8', errors='ignore')
        print(f"Attempting XOR with Key {Key}: {decrypted_str[:1000]}...")
        if all(c in string.printable for c in decrypted_str):
            Cleaned = Clean(decrypted_str)
            print(f"Cleaned: {Cleaned}")
            return decrypted_str
    
    return "Failed to decrypt"
def Decrypt(Encoded):
    Dictionary = [chr(i) for i in range(256)]
    Start = 256
    Position = 0
    Decoded = ""

    while Position < len(Encoded):
        try:
            Character = int(Encoded[Position], 36)
            Position += 1

            if Character < len(Dictionary):
                Decoded += Dictionary[Character]
            else:
                print(f"Error: Character {Character} out of bounds (Position: {Position})")
                break

            if Position < len(Encoded):
                NextCharacter = int(Encoded[Position], 36)
                Position += 1

                if Character < len(Dictionary) and NextCharacter < len(Dictionary):
                    NewEntry = Dictionary[Character] + Dictionary[NextCharacter][0]
                    Dictionary.append(NewEntry)
                    Start += 1
                else:
                    print(f"Invalid dictionary reference: {Character}, {NextCharacter}")
                    break
        except Exception as e:
            print(f"Error: {e} at Position {Position}")
            break
        

    print(f"Final Decoded: {repr(Decoded)}")
    return Decoded

def Encryptable(Data):
    Sum = sum(c not in string.printable for c in Data) > len(Data) * 0.3
    return Sum

def Decode(Payload):
    Decrypted = Decrypt(Payload)

    if Encryptable(Decrypted):
        Decrypted = Clean(Decrypted)
        print(f"Cleansed: {Decrypted}")
        return Decrypted
    

Payload = "\x01\x01"
Result = AttemptXOR(Payload)

print(f"Decoded: {Result}")