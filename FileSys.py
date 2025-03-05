import sys, os, shutil
from PySide6.QtWidgets import (QApplication, QMainWindow, QFileSystemModel, QTreeView, QListView, QVBoxLayout,
                               QPushButton, QHBoxLayout, QWidget, QMessageBox, QInputDialog, QMenu)
from PySide6.QtCore import Qt, QPoint, QModelIndex

class Manager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Management System")
        self.resize(800,600)
        Central = QWidget()
        self.setCentralWidget(Central)
        self.Layout = QVBoxLayout()
        Central.setLayout(self.Layout)

        self.Model = QFileSystemModel()
        self.Model.setRootPath("")

        self.Tree = QTreeView()
        self.Tree.setModel(self.Model)
        self.Tree.setRootIndex(self.Model.index(""))
        self.Tree.setColumnWidth(0,250)
        self.Tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.Tree.customContextMenuRequested.connect(self.ShowMenuTree)
        self.Layout.addWidget(self.Tree)

        self.List = QListView()
        self.List.setModel(self.Model)
        self.List.setContextMenuPolicy(Qt.CustomContextMenu)
        self.List.customContextMenuRequested.connect(self.ShowMenuList)
        self.Layout.addWidget(self.List)

        self.Tree.selectionModel().selectionChanged.connect(self.UpdateList)

        self.StatusBar = self.statusBar()
        self.StatusBar.setContentsMargins(0,5,0,5)

    def ShowMenuTree(self,Position:QPoint):
        Index = self.Tree.indexAt(Position)
        if not Index.isValid(): return
        Path = self.Model.filePath(Index)
        Menu = QMenu(self)
        Create = Menu.addAction("Create")
        Delete = Menu.addAction("Delete")
        Rename = Menu.addAction("Rename")
        Action = Menu.exec(self.Tree.viewport().mapToGlobal(Position))
        if Action == Create: self.CreateFile(Path)
        elif Action == Delete: self.DeleteFile(Path)
        elif Action == Rename: self.RenameFile(Path)
    def ShowMenuList(self,Position:QPoint):
        Index = self.Tree.indexAt(Position)
        if not Index.isValid(): return
        Path = self.Model.filePath(Index)
        Menu = QMenu(self)
        Create = Menu.addAction("Create")
        Delete = Menu.addAction("Delete")
        Rename = Menu.addAction("Rename")
        Action = Menu.exec(self.Tree.viewport().mapToGlobal(Position))
        if Action == Create: self.CreateFile(os.path.dirname(Path))
        elif Action == Delete: self.DeleteFile(Path)
        elif Action == Rename: self.RenameFile(Path)
    def UpdateList(self,Selected,Deselected):
        Index = self.Tree.selectionModel().currentIndex()
        Path = self.Model.filePath(Index)
        self.List.setRootIndex(self.Model.index(Path))

    def CreateFile(self,Directory):
        if os.path.isdir(Directory):
            Name,Ok = QInputDialog.getText(self,"Create File","Enter File Name")
            if Ok and Name:
                Path = os.path.join(Directory,Name)
                try:
                    with open(Path,'w') as File:
                        File.write("")
                    self.StatusBar.showMessage(f"File '{Name}' created successfully.", 3000)
                except Exception as Exceptor:
                    QMessageBox.critical(self,"Exception",f"An Exception occured. Exceptor: {str(Exceptor)}")       
        else:
            QMessageBox.warning(self,"Warning","Select a valid directory to create a file.")
       
    def DeleteFile(self,Path):
        if os.path.exists(Path):
            Confirm = QMessageBox.question(self,"Confirm",f"Are you sure you want to delete {Path}?",QMessageBox.Yes | QMessageBox.No)
            if Confirm == QMessageBox.Yes:
                try:
                    if os.path.isfile(Path):
                        os.remove(Path)
                    else:
                        shutil.rmtree(Path)
                    self.StatusBar.showMessage(f"File '{Path}' deleted successfully.", 3000)
                except Exception as Exceptor:
                    QMessageBox.critical(self,"Exception",f"An Exception occured. Exceptor: {str(Exceptor)}")
        else:
            QMessageBox.warning(self,"Warning","Select a valid File to delete.")

    def RenameFile(self,Path):
        if os.path.exists(Path):
            Name,Ok = QInputDialog.getText(self,"Rename","Enter New File name:")
            if Ok and Name:
                NewPath = os.path.join(os.path.dirname(Path),Name)
                try:
                    os.rename(Path,NewPath)
                    self.StatusBar.showMessage(f"File renamed to '{Path}'.", 3000)
                except Exception as Exceptor:
                    QMessageBox.critical(self,"Exception",f"An Exception occured. Exceptor: {str(Exceptor)}")
        else:
            QMessageBox.warning(self,"Warning","Select a valid File to rename.")

if __name__ == "__main__":
    Application = QApplication(sys.argv)
    Window = Manager()
    Window.show()
    sys.exit(Application.exec())
