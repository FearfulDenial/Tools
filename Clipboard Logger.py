import pyperclip
import time

# Vars
LogFile = "cliplog.txt"
PrevContent = ""
Debug = False

# Functions
def LogClipboard():
    if Debug:
        print("LogClipboard() called.")
    global PrevContent
    while True:
        CurContent = pyperclip.paste()

        if CurContent != PrevContent:
            with open(LogFile, 'a') as F:
                if Debug:
                    print("Writing Content to LogFile.")
                F.write(f"CLIP-LOG: {CurContent}\n")
            PrevContent = CurContent
        
        time.sleep(1)

# Runtime
if __name__ == "__main__":
    if Debug:
        print("Runtime initialized.")
    LogClipboard()