
import re
Obfs = "\xd08\x8c\x10J"
Obfs = re.sub(r'[^0-9a-fA-F]', '', Obfs)
if Obfs.startswith("0x"):
    Obfs = Obfs[2:]
if len(Obfs) % 2 != 0:
    Obfs = "0" + Obfs

try:
    result = bytes.fromhex(Obfs)
    print("Converted bytes:", result)
except ValueError as e:
    print("Error during conversion:", e)