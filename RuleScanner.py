import sys,re,hashlib
import urllib.request
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QFileDialog, QLineEdit
)

Regex = {
    "Eval": r"\beval\s*\(",
    "Exec": r"\bexec\s*\(",
    "OS Exec": r"\bos\.(system|popen|exec|spawn)\s*\(",
    "Base64": r"base64\.b(64)?decode",
    "Import subprc": r"\bimport\s+subprocess",
    "Hex": r"\\x[0-9a-fA-F]{2,}",
    "Fetch": r"\b(urllib\.request\.urlopen|requests\.get|httpx\.get)\s*\(",
    "File": r"\b(open|os\.remove|shutil\.(rmtree|copy|move))\s*\(",
    "Injection": r"(input\s*\(|pickle\.loads|marshal\.loads|json\.loads\s*\()",
    "Threading": r"\b(threading|multiprocessing)\.Process\s*\(",
    "Cryptograph": r"\b(hashlib\.md5|hashlib\.sha256|random\.randint)\s*\(",
    "Keylog": r"\b(pynput|keyboard|mouse)\b",
    "Self-Modifying": r"\bopen\s*\(\s*['\"]__file__['\"]\s*,",
    "XOR": r"\^0x[0-9a-fA-F]+",
    "ROT13": r"rot13",
    "PrivUpgrade": r"os\.set(e)?uid\(0\)",
    "HiddenImport": r"__import__\(|importlib\.import_module\(",
    "Sleep": r"time\.sleep\s*\(\d{4,}\)",
}


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Delta")
        self.setGeometry(100,100,600,400)
        Layout = QVBoxLayout()

        self.Select = QPushButton("Select File")
        self.Select.clicked.connect(self.Open)

        self.Input = QLineEdit()
        self.Input.setPlaceholderText("Select Url")

        self.ScanUrl = QPushButton("Scan Url")
        self.ScanUrl.clicked.connect(self.Scan2)

        self.Results = QTextEdit()
        self.Results.setReadOnly(True)

        Layout.addWidget(self.Select)
        Layout.addWidget(self.Input)
        Layout.addWidget(self.ScanUrl)
        Layout.addWidget(self.Results)

        self.setLayout(Layout)

    def Open(self):
        File, _ = QFileDialog.getOpenFileName(self, "Select a file")
        if File:
            self.Scan(File)

    def Scan(self, Path):
        try:
            Hash = self.Compute(Path)
            with open(Path,"r",encoding="utf-8",errors="ignore") as File:
                Content = File.read()

            Results = self.Detect(Content)
            self.Results.setText(f"HASH:{Hash}\n\n" + (Results if Results else "No code detected."))

        except Exception as Exceptor:
            self.Results.setText(f"Exception while reading {Path}: {str(Exceptor)}")

    def Compute(self, Path):
        Hash = hashlib.sha256()
        try:
            with open(Path,"rb") as File:
                while Chunk := File.read(8192):
                    Hash.update(Chunk)
            return Hash.hexdigest()
        except Exception as Exceptor:
            return f"null:{str(Exceptor)}"

    def Detect(self, Content):
        Results = []
        Lines = Content.splitlines()
        for i,v in Regex.items():
            for k in re.finditer(v, Content):
                Pos = k.start()
                Line = Content[:Pos].count("\n") + 1
                Col = Pos - Content.rfind("\n",0,Pos)
                Results.append(f"{i} detected on {Line}:{Col}.")
            if re.search(v, Content):
                Results.append(f"{i} detected on line {Content.find(v)+1}")
        return "\n".join(Results) if Results else "No code detected."

    def Scan2(self):
        Url = self.Input.text().strip()
        if not Url: self.Results.setText("No Url found."); return
        try:
            with urllib.request.urlopen(Url) as Response:
                Cb = Response.read()
                Ct = Cb.decode("utf-8",errors="ignore")
                Hash = hashlib.sha256(Cb).hexdigest()
                Results = self.Detect(Ct)
                self.Results.setText(f"HASH:{Hash}\n\n" + (Results if Results else "No code detected."))
        except Exception as Exceptor:
            self.Results.setText(f"Failed to fetch, got {str(Exceptor)}")

if __name__ == "__main__":
    Exec = QApplication(sys.argv)
    Window = App()
    Window.show()
    sys.exit(Exec.exec())