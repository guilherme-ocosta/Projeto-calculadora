from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QGridLayout, QMessageBox
from PySide6.QtCore import Slot
from PySide6.QtGui import QKeyEvent, Qt
from components import Button, Display, Info
from variables import isNumOrDot, isEmpty, isValidNumber, isValidOperator, convertToNumber
import math


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)    
        ...

        self.setWindowTitle('Calculadora')

        self.vLayout = QVBoxLayout()
        self.setStyleSheet('font-size: 40px')

        self.cw = QWidget()
        self.cw.setLayout(self.vLayout)

        self.setCentralWidget(self.cw)

    def addWidgetToVLayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)

    def addGridToVLayout(self, grid):
        self.vLayout.addLayout(grid)


    def adjustFixedSize(self):
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def makeMsgBox(self):
        return QMessageBox(self)


class ButtonsGrid(QGridLayout):
    def __init__(self, display: Display, info: Info, window: QMessageBox, *args, **kwargs):
        super().__init__(*args, **kwargs)

    
        self._gridMask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['N',  '0', '.', '='],
        ]


        self.display = display
        self.window = window
        self.info = info
        self._left = None
        self._right = None
        self._op = None
        self._equation = ''
        self._initialEquation = 'Sua conta'
        self.equation = self._initialEquation

        self._makeGrid()

    @property
    def equation(self):
        return self._equation
    
    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self._backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._configLeftOp)

        for i, row in enumerate(self._gridMask):
            for j, val in enumerate(row):
                button = Button(val)

                if not isNumOrDot(val) and not isEmpty(val):
                    button.setProperty('cssClass', 'specialButton')
                    self._configsSpecialButton(button)

                self.addWidget(button, i, j)
                slot = self._makeSlot(self._insertToDisplay, val)
                self._connectButtonClicked(button, slot)

    def _connectButtonClicked(self, button, func):
        button.clicked.connect(func)

    def _configsSpecialButton(self, button: Button):
        buttonText = button.text()

        if buttonText == 'C':
            self._connectButtonClicked(button, self._clear)

        if buttonText == '◀':
            self._connectButtonClicked(button, self._backspace)

        if buttonText in '+-/*^':
            self._connectButtonClicked(button, self._makeSlot(self._configLeftOp, buttonText))

        if buttonText.upper() == 'N':
            self._connectButtonClicked(button, self._turnNegative)

        if buttonText == '=':
            self._connectButtonClicked(button, self._eq)


    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot():
            func(*args, **kwargs)
        return realSlot
    
    @Slot()
    def _insertToDisplay(self, text):
        newDisplayValue = self.display.text() + text

        if isValidNumber(newDisplayValue):
            self.display.insert(text)
            self.display.setFocus()
            return
    
    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()

    @Slot()
    def _clear(self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = self._initialEquation
        self.display.clear()
        self.display.setFocus()
        return

    @Slot()
    def _configLeftOp(self, text):
        displayText = self.display.text()
        self.display.clear()

        if not isValidNumber(displayText) and self._left is None:
            self._showError('Operação inválida. Digite primeiro o número.')
            return
        
        if self._left is None:
            self._left = convertToNumber(displayText)

        self._op = text
        self.equation = f'{self._left} {self._op} ??'

        self.display.setFocus()

    @Slot()
    def _turnNegative(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            return
        
        number = convertToNumber(displayText) * -1

        self.display.setText(str(number))
        self.display.setFocus()

    @Slot()
    def _eq(self):
        displayText = self.display.text()
        
        if not isValidNumber(displayText) or self._left is None:
            self._showError('Operação inválida. Sem números para a conta.')
            return
        
        self._right = convertToNumber(displayText)

        self.equation = f'{self._left} {self._op} {self._right}'
        
        result = 'error'

        try:
            if '^' in self.equation and isinstance(self._left, (float, int)):
                result = math.pow(self._left, self._right)
                result = convertToNumber(str(result))
            else:
                result = eval(self.equation)
                result = convertToNumber(str(result))
        except ZeroDivisionError:
            self._showError('Erro de divisão.')
        except OverflowError:
            self._showError('Operação com overflow.')
            
        self.display.clear()
        self.info.setText(f'{self.equation} = {result}')
        self._left = result
        self._right = None

        self.display.setFocus()

        if result == 'error':
            self._left = None

    def _showError(self, text):
        msgBox = self.window.makeMsgBox()
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.setStandardButtons(msgBox.StandardButton.Ok)
        msgBox.setText(text)
        msgBox.exec()
        self.display.setFocus()

        





        



    




