# GUI application that compares two texts
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog, QShortcut,
                             QTextEdit, QPushButton, QHBoxLayout, QVBoxLayout, QLabel)
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QKeySequence
from style import *
from os import path


class DialogApp(QWidget):
    def __init__(self):
        super().__init__()

        # load the icons folder for the app
        app_dir = path.dirname(__file__)
        icons_dir = path.join(app_dir, "icons")

        # setting up the buttons and texteditor field
        button1 = QPushButton("Import file")
        button1.clicked.connect(lambda: self.import_data(1))
        button1.setMinimumHeight(30)
        button1.setFont(QtGui.QFont("Sanserif", 11))
        button1.setIcon(QtGui.QIcon(path.join(icons_dir, "open.png")))
        button1.setToolTip("Shortcut: Ctrl+E")
        button1_shortcut = QShortcut(QKeySequence('Ctrl+E'), button1)
        button1_shortcut.activated.connect(lambda: self.import_data(1))

        button2 = QPushButton("Import file to compare to")
        button2.clicked.connect(lambda: self.import_data(2))
        button2.setMinimumHeight(30)
        button2.setFont(QtGui.QFont("Sanserif", 11))
        button2.setIcon(QtGui.QIcon(path.join(icons_dir, "open.png")))
        button2.setToolTip("Shortcut: Ctrl+T")
        button2_shortcut = QShortcut(QKeySequence('Ctrl+T'), button2)
        button2_shortcut.activated.connect(lambda: self.import_data(2))

        quitbutton = QPushButton()
        quitbutton.setIcon(QtGui.QIcon(path.join(icons_dir, "x.png")))
        quitbutton.setIconSize(QtCore.QSize(25, 25))
        quitbutton.clicked.connect(self.close)
        quitbutton.setMaximumWidth(30)
        quitbutton.setMaximumHeight(30)
        quitbutton.move(50, 0)
        quitbutton.setToolTip("Shortcut: Escape")
        quit_shortcut = QShortcut(QKeySequence('Esc'), self)
        quit_shortcut.activated.connect(self.close)

        self.textEditor1 = QTextEdit("Or You Can Copy The Text Into The Box")
        self.textEditor1.setFont(QtGui.QFont("Sanserif", 10))
        self.textEditor1.setStyleSheet("background-color:lightgrey")
        self.textEditor1.textChanged.connect(self.get_text)
        self.textEditor2 = QTextEdit()
        self.textEditor2.setFont(QtGui.QFont("Sanserif", 10))
        self.textEditor2.setStyleSheet("background-color:lightgrey")
        self.textEditor2.textChanged.connect(self.get_text)

        button3 = QPushButton("Compare")
        button3.clicked.connect(self.set_text)
        button3.setIcon(QtGui.QIcon(path.join(icons_dir, "run.png")))
        button3.setIconSize(QtCore.QSize(25, 25))
        button3.setMaximumWidth(150)
        button3.setMinimumHeight(30)
        button3.setFont(QtGui.QFont("Sanserif", 11))
        button3.setToolTip("Shortcut: Ctrl+R")
        button3_shortcut = QShortcut(QKeySequence('Ctrl+R'), button3)
        button3_shortcut.activated.connect(self.set_text)

        icon = QLabel("<html><img src='text.png'>")
        program_label = QLabel("Compare Texts")
        program_label.setFont(QtGui.QFont("Sanserif", 20))

        # organize the buttons with HBox and VBox layouts
        layout0 = QHBoxLayout()
        layout0.addStretch(1)
        layout0.addWidget(icon)
        layout0.addWidget(program_label)
        layout0.addStretch(1)
        layout0.addWidget(quitbutton)

        layout1 = QHBoxLayout()
        layout1.addWidget(button1)
        layout1.addWidget(button3)
        layout1.addWidget(button2)

        layout2 = QHBoxLayout()
        layout2.addWidget(self.textEditor1)
        layout2.addWidget(self.textEditor2)

        layout3 = QHBoxLayout()
        layout3.addStretch(1)
        layout3.addWidget(button3)
        layout3.addStretch(1)

        layout = QVBoxLayout()
        layout.addLayout(layout0)
        layout.addLayout(layout1)
        layout.addLayout(layout2)

        self.setLayout(layout)
        self.showFullScreen()

    def set_text(self):
        """After getting the texts from the get_text fn, iterate over
        every line.

        For every line, check the 4 lines before it and after
        it in the other text.

        If we find the exact match, add a '\n' for formatting and break.

        Else look for such a line in the other text so that more than 50%
        of the words in those lines are the same. Then iterate over every
        word in first line, see if it's in the other line. If not add
        red(blue) background to it.

        If we didn't find anything in the for loop, that means the line
        doesn't exist in the other text, or it has changed drastically.
        So add red(blue) background to the whole line, minus the leading
        or trailing spaces in it.
        """
        text1, text2 = self.get_text()
        cpy = text1[:]
        for ind in range(len(text1)):
            split1 = text1[ind].split()
            if len(split1) > 0:
                changed = False
                low = ind - 4 if ind - 4 > 0 else 0
                high = ind + 5 if ind + 5 < len(text2) else len(text2)
                for ind2 in range(low, high):
                    split2 = text2[ind2].split()
                    if text1[ind] == text2[ind2]:
                        text1[ind] += '\n'
                        break
                    elif sum(1 for word in split1 if word in split2) / len(split1) > 0.5:
                        for word in split1:
                            if word not in split2:
                                changed = True
                                text1[ind] = text1[ind].replace(
                                    word, "<span style='background-color:rgba(255, 0, 0, 0.5)'>" + word + "</span>", 1)
                        text1[ind] += "\n"
                        if changed:
                            break
                else:
                    strip1 = text1[ind].strip()
                    text1[ind] = text1[ind].replace(
                        strip1, "<span style='background-color:rgba(255, 0, 0, 0.5)'>" + strip1 + "</span>")
                    text1[ind] += "\n"
            else:
                text1[ind] += "\n"

        self.textEditor1.setHtml(
            "<p style='white-space:pre-wrap'>" + "".join(text1) + "</p>")

        text1 = cpy
        for ind in range(len(text2)):
            split2 = text2[ind].split()
            if len(split2) > 0:
                changed = False
                low = ind - 4 if ind - 4 > 0 else 0
                high = ind + 5 if ind + 5 < len(text2) else len(text2)
                for ind2 in range(low, high):
                    split1 = text1[ind2].split()
                    if text2[ind] == text1[ind2]:
                        text2[ind] += "\n"
                        break
                    elif sum(1 for word in split2 if word in split1) / len(split2) > 0.5:
                        for word in split2:
                            if word not in split1:
                                changed = True
                                text2[ind] = text2[ind].replace(
                                    word, "<span style='background-color:rgba(0, 0, 255, 0.5)'>" + word + "</span>", 1)
                        text2[ind] += "\n"
                        if changed:
                            break
                else:
                    strip2 = text2[ind].strip()
                    text2[ind] = text2[ind].replace(
                        strip2, "<span style='background-color:rgba(0, 0, 255, 0.5)'>" + strip2 + "</span>")
                    text2[ind] += "\n"
            else:
                text2[ind] += "\n"

        self.textEditor2.setHtml(
            "<p style='white-space:pre-wrap'>" + "".join(text2) + "</p>")

    def get_text(self):
        return (self.textEditor1.toPlainText().split("\n"),
                self.textEditor2.toPlainText().split("\n"))

    def import_data(self, num):
        # import the data, can be any file that has a text representation
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setFilter(QDir.Files)

        if dialog.exec_():
            file_name = dialog.selectedFiles()

            with open(file_name[0], "r") as f:
                data = f.read()
                if num == 1:
                    self.textEditor1.setPlainText(data)
                if num == 2:
                    self.textEditor2.setPlainText(data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    window = DialogApp()
    sys.exit(app.exec_())
