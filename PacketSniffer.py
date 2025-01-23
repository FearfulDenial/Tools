
import sys
from threading import Thread
from PySide6.QtWidgets import QApplication,QMainWindow,QVBoxLayout,QTextEdit,QWidget,QFileDialog,QPushButton
from PySide6.QtGui import QFont, QTextCursor, QColor
from scapy.all import sniff, conf, IP, TCP

class Application(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sniffer")
        self.setGeometry(100,100,800,600)
        self.TextEdit = QTextEdit(self)
        self.TextEdit.setReadOnly(True)
        self.Save = QPushButton("Save")
        self.Save.clicked.connect(self.SaveLog)

        Font = QFont("Monospace")
        Font.setStyleHint(QFont.TypeWriter)
        self.TextEdit.setFont(Font)

        Layout = QVBoxLayout()
        Layout.addWidget(self.TextEdit)
        Layout.addWidget(self.Save)
        Container = QWidget()
        Container.setLayout(Layout)
        self.setCentralWidget(Container)

        self.MaxLogs = 500

    def Log(self,Info,Color="White"):
        TInfo = Info if len(Info) <= 500 else (Info[:497] + "...")
        Html = f'<span style="color:{Color};">{TInfo}</span>'
        self.TextEdit.append(Html)
        self.Truncate()
    def Truncate(self):
        Cursor = self.TextEdit.textCursor()
        Cursor.movePosition(QTextCursor.Start)
        if self.TextEdit.document().lineCount() > self.MaxLogs:
            Cursor.select(QTextCursor.BlockUnderCursor)
            Cursor.removeSelectedText()
            Cursor.deleteChar()
    def SaveLog(self):
        File,_ = QFileDialog.getSaveFileName(self,"Save Log","","Log Files (*.log);;All Files (*)")
        if File:
            with open(File,"w") as AFile:
                AFile.write(self.TextEdit.toPlainText())
            self.Log(f"Saved logs to {File}")

def Handle(Packet,Callback):
    if Packet.haslayer(IP) and Packet.haslayer(TCP):
        Headers = (f"{Packet[IP].src} - {Packet[IP].dst}\n{Packet[TCP].sport} - {Packet[TCP].dport}")
        RawPayload = bytes(Packet[TCP].payload)
        Payload = RawPayload.decode(errors="replace")
        HexPayload = RawPayload.hex()
        Info = (f"{Headers}\n> (Text) [ {Payload} ]\n (Hex) [ {HexPayload} ]")
        Callback(Info)

def Main(Callback):
    try:
        def pcb(packet):
            Handle(packet,Callback)

        sniff(filter="tcp", prn=pcb, store=0)
    except Exception as Exceptor:
        Callback(f"Exceptor - {str(Exceptor)}")

if __name__ == "__main__":
    App = QApplication(sys.argv)
    Window = Application()

    def Start():
        Main(Window.Log)
    
    SniffThread = Thread(target=Start,daemon=True)
    SniffThread.start()

    Window.show()
    sys.exit(App.exec())