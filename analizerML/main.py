import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.Qt import *
from PyQt5.QtCore import QObject, pyqtSignal
import gui
import re

# анализ правильности конструкции выражения
def analizeExpressionConstruction():
    pass

# анализ возвращаемых выражением данных
def analizeExpressionTypeData():
    pass

# класс условного цикла: while (выражение) do оператор
class Lexem:
    def __init__(self, name, position, table, tableIndex):
        self.name = name
        self.position = position
        if table == 1:
            self.table = "Ключевое слово"
        elif table == 2:
            self.table = "Разделитель"
        if table == 3:
            self.table = "Число"
        if table == 4:
            self.table = "Идентификатор"
        self.tableIndex = tableIndex+1

    def analizeConstruction(self):
        pass

# класс условного цикла: while (выражение) do оператор
class WhileLoop:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def analizeConstruction(self):
        pass

# класс фиксированного цикла: for присваивание to выражение step выражение оператор next
class ForLoop:
    def __init__(self, assignment, toBody, stepBody, body):
        self.assignment = assignment
        self.toBody = toBody
        self.stepBody = stepBody
        self.body = body

    def analizeConstruction(self):
        pass

# класс описания: тип идентификатор, идентификатор, ...
class DescriptionStatement:
    def __init__(self, typeData, body):
        self.typeData = typeData
        self.body = body

    def analizeConstruction(self):
        pass

# класс присваивания: идентификатор := выражение
class AssignmentStatement:
    def __init__(self, identificator, body):
        self.identificator = identificator
        self.body = body

    def analizeConstruction(self):
        pass

# класс условного оператора: if (выражение) оператор else оператор
class IfStatement:
    def __init__(self, condition, thenBody, elseBody):
        self.condition = condition
        self.thenBody = thenBody
        self.elseBody = elseBody

    def analizeConstruction(self):
        pass

# класс оператора чтения данных: readln идентификатор, идентификатор, ...
class ReadStatement:
    def __init__(self, body):
        self.body = body

    def analizeConstruction(self):
        pass

# класс оператора чтения данных: readln идентификатор, идентификатор, ...
class BefinEndOperator:
    def __init__(self, body):
        self.body = body

    def analizeConstruction(self):
        pass

# класс оператора вывода данных: writeln выражение, выражение, ...
class WriteStatement:
    def __init__(self, body):
        self.body = body

    def analizeConstruction(self):
        pass

# ГЛАВНЫЙ КЛАСС - ГЛАВНОЕ ОКНО ПРИЛОЖЕНИЯ
class Window(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.onLoad)
        self.keywords = ["program","var","true", "false", "begin", "end", "%", "!", "$", "if", "else", "for", "to", "step", "next", "while", "readln", "writeln"]
        self.delimiters = ["!=", "==", "<", "<=", ">", ">=", "+", "-", "||", "*", "/", "&&", "!", ":", ",", ";", ":=", "(", ")", "." ,"{", "}"]
        self.keywords.sort()
        self.delimiters.sort()
        self.descriptionIdentificators = {}
        self.initialazedIndificators = []
        self.identificators = []
        self.numbers = []
        self.numbersTypeData = []

        self.descsIdentificators = []
        self.initialsIdentificators = []

        self.onLoad()

        self.pushButton.clicked.connect(self.lexicalAnalizer)
        self.pushButton_2.clicked.connect(self.clearAll)

    def clearAll(self):
        self.tableWidget_3.clear()
        self.tableWidget_4.clear()
        self.tableWidget_5.clear()
        self.listWidget.clear()
        self.listWidget_2.clear()
        self.listWidget_3.clear()
        self.identificators = []
        self.numbers = []
        self.label_2.setStyleSheet("color: black;")
        self.label_3.setStyleSheet("color: black;")
        self.label_4.setStyleSheet("color: black;")

    def getError(self, messege, type):
        if type == 1:
            # self.listWidget_2.clear()
            self.label_3.setStyleSheet("color: red;")
            item = QListWidgetItem(messege)
            item.setForeground(QColor("red"))
        elif type == 2:
            item = QListWidgetItem(messege)
            item.setForeground(QColor("green"))
        elif type == 3:
            item = QListWidgetItem(messege)
            item.setForeground(QColor("black"))
        elif type == 4:
            item = QListWidgetItem(messege)
            item.setForeground(QColor("blue"))
        self.listWidget_2.addItem(item)

    def getErrorLex(self, messege, type):
        if type == 1:
            # self.listWidget.clear()
            self.label_2.setStyleSheet("color: red;")
            item = QListWidgetItem(messege)
            item.setForeground(QColor("red"))
        elif type == 2:
            item = QListWidgetItem(messege)
            item.setForeground(QColor("green"))
        elif type == 3:
            item = QListWidgetItem(messege)
            item.setForeground(QColor("black"))
        elif type == 4:
            item = QListWidgetItem(messege)
            item.setForeground(QColor("blue"))
        self.listWidget.addItem(item)

    def getErrorSem(self, messege, type):
        if type == 1:
            # self.listWidget_3.clear()
            self.label_4.setStyleSheet("color: red;")
            item = QListWidgetItem(messege)
            item.setForeground(QColor("red"))
        elif type == 2:
            item = QListWidgetItem(messege)
            item.setForeground(QColor("green"))
        elif type == 3:
            item = QListWidgetItem(messege)
            item.setForeground(QColor("black"))
        elif type == 4:
            item = QListWidgetItem(messege)
            item.setForeground(QColor("blue"))
        self.listWidget_3.addItem(item)

    def onDoneLexer(self, lexemes):
        self.getErrorLex("Лексический анализ успешно завершен", 2)
        self.tableWidget_3.setColumnCount(2)
        self.tableWidget_4.setColumnCount(2)
        self.tableWidget_5.setColumnCount(3)
        self.identificators.sort()
        self.tableWidget_3.setRowCount(len(self.numbers))
        self.tableWidget_4.setRowCount(len(self.identificators))
        self.tableWidget_5.setRowCount(len(lexemes))

        self.tableWidget_3.setHorizontalHeaderLabels(['Число', 'Тип'])
        self.tableWidget_4.setHorizontalHeaderLabels(['Идентификатор', 'Тип данных'])
        self.tableWidget_5.setHorizontalHeaderLabels(['Лексема', 'Таблица', 'Позиция'])

        for row in range(len(self.numbers)):
            value_item = QTableWidgetItem(self.numbers[row])
            self.tableWidget_3.setItem(row, 0, value_item)
            value_item = QTableWidgetItem(str(self.numbersTypeData[row]))
            self.tableWidget_3.setItem(row, 1, value_item)

        row = 0
        for lexem in lexemes:
            value_item = QTableWidgetItem(lexem.name)
            self.tableWidget_5.setItem(row, 0, value_item)
            value_item = QTableWidgetItem(str(lexem.table))
            self.tableWidget_5.setItem(row, 1, value_item)
            value_item = QTableWidgetItem(str(lexem.tableIndex))
            self.tableWidget_5.setItem(row, 2, value_item)
            row += 1
            # print(row, lexem.name, lexem.table, lexem.tableIndex)

    def onLoad(self):
        self.tableWidget.setColumnCount(1)
        self.tableWidget_2.setColumnCount(1)
        self.listWidget_3.setWordWrap(True)
        self.listWidget_2.setWordWrap(True)
        self.listWidget.setWordWrap(True)

        self.tableWidget.setRowCount(len(self.keywords))
        self.tableWidget_2.setRowCount(len(self.delimiters))

        for row, value in enumerate(self.keywords):
            value_item = QTableWidgetItem(value)  # Создаем ячейку для значения
            self.tableWidget.setItem(row, 0, value_item)  # Устанавливаем ячейку во второй столбец

        for row, value in enumerate(self.delimiters):
            value_item = QTableWidgetItem(value)  # Создаем ячейку для значения
            self.tableWidget_2.setItem(row, 0, value_item)  # Устанавливаем ячейку во второй столбец

        """self.textEdit.setText("int num1, num2\n"
                              "float numF:num2:=3d+5-110B\n"
                              "numF:=5.4\n"
                              "num2:=2\n"
                              "numF:=3E+3+10D\n"
                              "begin if (num1<=num2) num1 := num2; if (num2>10) num2:=num2+10-2*153 else begin num2:=num2-10;readln num1 end end\n"
                              "for num1:=2+5 to 10 step 2 writeln num1, num1*10 next\n"
                              "while (num1>5) num1:=num1-1*5:writeln num1\n"
                              "(*комментарий*) readln numF, num1, num2\n"
                              "bool i : i:=true : writeln i\n.")
        """
        self.textEdit.setText("program var a, b, c, x1, x2, discriminant, discriminantQuadratum, temp1, temp2, temp3, temp4, const: !;\n"
                              "begin\n"
                              "a:=4;\n"
                              "b:=4 + 1;\n"
                              "c:=6;\n"
                              "const:=4;\n"
                              "temp1 := b * b;\n"
                              "temp2 := const * a * c;\n"
                              "discriminant := temp1 - temp2;\n"
                              "if (discriminant < 0)\n"
                              "{Квадратное уравнение не имеет корней}\n"
                              "else\n"
                              "begin\n"
                              "if (discriminant == 0)\n"
                              "begin\n"
                              "temp1 := 0 - b;\n"
                              "temp2 := 2 * a;\n"
                              "x1 := temp1 / temp2;\n"
                              "x2 := x1;\n"
                              "end\n"
                              "else\n"
                              "begin\n"
                              "discriminantQuadratum := discriminant * discriminant;\n"
                              "temp3 := temp1 + discriminantQuadratum;\n"
                              "temp4 := temp1 - discriminantQuadratum;\n"
                              "x1 := temp3 / temp2;\n"
                              "x2 := temp4 / temp2;\n"
                              "end;\n"
                              "end;\n"
                              "writeln x1;\n"
                              "writeln x2;\n"
                              "end .")
        """self.textEdit.setText("prog dim num1, num2 #;\n"
                              "dim numF @ ;\n"
                              "num2:=3d plus 5 min 110B ;\n"
                              "numF:=5.4 ;\n"
                              "num2:=2 ;\n"
                              "numF:=3E+3 plus 10D ;\n"
                              "begin if (num1 LE num2) num1 := num2; if (num2 GT 10) num2:=num2 plus 10 min 2 mult 153 else begin num2:=num2 min 10;readln num1 end end ;\n"
                              "for num1:=2 plus 5 to 10 step 2 writeln num1, num1 mult 10 next ;\n"
                              "while (num1 GT 5) num1:=num1 min 1 mult 5 ;"
                              "writeln num1 ;\n"
                              "/*комментарий*/ readln numF, num1, num2 ;\n"
                              "dim i &; i:=true ; writeln i ; }")
        """
    def getNumberSystem(self, s):
        if all(char.isdigit() and int(char) <= 7 for char in s[:-1]) and (s[-1] == 'O' or s[-1] == 'o'):
            return "Целое 8-ричное"
        elif all(char.isdigit() and int(char) <= 1 for char in s[:-1]) and (s[-1] == 'B' or s[-1] == 'b'):
            return "Целое 2-ичное"
        elif all(char.isdigit() for char in s[:-1]) and (s[-1] == 'D' or s[-1] == 'd'):
            return "Целое 10-тичное"
        elif all(char.isdigit() or char in "ABCDEFabcdef" for char in s[:-1]) and (s[-1] == 'H' or s[-1] == 'h'):
            return "Целое 16-ричное"
        elif all(char.isdigit() for char in s):
            return "Целое 10-тичное"
        elif ("E" in s or "e" in s) and "." not in s:
            if "E" in s:
                s = s.split("E")
            else:
                s = s.split("e")
            if all(char.isdigit() for char in s[0]):
                if all(char.isdigit() for char in s[1][1:]):
                    if s[1][0] == "+" or s[1][0] == "-":
                        if len(s[1]) == 1:
                            return 1
                        else:
                            return "ДЭФЗ"
                    elif all(char.isdigit() for char in s[1][0]):
                        return "ДЭФ"
                    else:
                        return 1
                else:
                    return 1

            else:
                return 1
            return "ДЭФ"
        elif "." in s:
            s = s.split(".")
            if all(char.isdigit() for char in s[0]):
                if ("E" in str(s[1]) or "e" in str(s[1])):
                    si = []
                    if "E" in s[1]:
                        si = str(s[1]).split("E")
                    elif "e" in s[1]:
                        si = str(s[1]).split("e")
                    if len(si[0]) > 0 and all(char.isdigit() for char in si[0]):
                        moreThan = 0
                        if "+" in si[1] or "-" in si[1]:
                            moreThan = 1
                        if len(si[1])>moreThan:
                            if all(char.isdigit() for char in si[1][1:]):
                                if "+" == si[1][0] or "-" == si[1][0]:
                                    return "ДЭФЗ"
                                elif all(char.isdigit() for char in si[1]):
                                    return "ДЭФ"
                                else:
                                    return 1
                            else:
                                return 1
                        else:
                            return 1
                    else:
                        return 1
                elif all(char.isdigit() for char in s[0]) and all(char.isdigit() for char in s[1]) and len(s[1])>0:
                    return "Д"
                else:
                    return 1
            else:
                return 1
        else:
            return 1

    # функция лексического анализа: разбитие кода на лексемы
    def lexicalAnalizer(self):
        if len(self.textEdit.toPlainText()) < 2:
            self.getErrorLex("Пустая строка", 1)
        else:
            lexemes = []
            self.numbersTypeData = []
            countLexem = 0
            stack = ""
            isNumber = False
            isWord = False
            index = 0
            isComment = False

            self.label_2.setStyleSheet("color: black;")
            self.label_3.setStyleSheet("color: black;")
            self.label_4.setStyleSheet("color: black;")
            self.tableWidget_3.clear()
            self.tableWidget_4.clear()
            self.tableWidget_5.clear()
            self.listWidget.clear()
            self.listWidget_2.clear()
            self.listWidget_3.clear()
            self.identificators = []
            self.numbers = []
            isExpNumber = False
            self.getErrorLex("Лексический анализ...", 3)
            error = 0



            # получение кода из формы
            code = self.textEdit.toPlainText().replace("\n", "")
            # проход по символам строки кода
            while index < len(code):
                self.getErrorLex("Считывание символа", 4)
                char = code[index]
                if isComment:
                    if char == ".":
                        self.getErrorLex("В составе комментария встречен символ завершения программы", 1)
                        error = 1
                        break

                if not isComment:
                    if index == (len(code)-1):
                        #stack += char
                        if char == ".": # end
                            lexemes.append(Lexem(char, countLexem, 2, self.delimiters.index(char)))
                    # обработка буквы
                    elif char.isalpha() and bool(re.match(r'[a-zA-Z]', char)):
                        if stack == "":
                            isWord = True
                            stack += char
                            self.getErrorLex("Сбор в буфер Слова, установка статуса Слово: " + stack, 3)
                        elif isNumber:
                            if isExpNumber:
                                stack += char
                                isExpNumber = False
                            elif char == "E" or char == "e":
                                isExpNumber = True
                                stack += char
                                self.getErrorLex("Сбор в буфер буквы E в статусе Число, установка статуса Экспонента: " + stack, 3)
                            else:
                                stack += char
                                self.getErrorLex("Сбор в буфер буквы в статусе Число: " + stack, 3)
                        elif isWord:
                            stack += char
                            self.getErrorLex("Сбор в буфер буквы в статусе Слово: " + stack, 3)
                        else:
                            self.getErrorLex("Ошибка формирования лексемы", 1)
                            error = 1
                            break

                    # обработка числа
                    elif char.isdigit():
                        if stack == "":
                            isNumber = True
                            stack += char
                            self.getErrorLex("Сбор в буфер числа, установка статуса Число: " + stack, 3)
                        elif isExpNumber:
                            stack += char
                            isExpNumber = False
                            self.getErrorLex("Сбор в буфер цифры в статусе Число и Экспонента: " + stack, 3)
                        elif isNumber:
                            stack += char
                            self.getErrorLex("Сбор в буфер цифры в статусе Число: " + stack, 3)
                        elif isWord:
                            stack += char
                            self.getErrorLex("Сбор в буфер цифры в статусе Слово: " + stack, 3)

                    elif char == ".":
                        if isNumber:
                            stack += char
                            self.getErrorLex("-- Обработка: сбор в буфер . при статусе Число " + stack, 3)
                        elif not isWord:
                            stack += char
                            isNumber = True
                        else:
                            self.getErrorLex("Ошибка формирования лексемы", 1)
                            error = 1
                            break

                    elif char == "-" and isNumber and isExpNumber:
                        self.getErrorLex("-- Обработка: - при статусе Экспонента " + stack, 3)
                        stack += char
                        isExpNumber = False

                    elif char == "+" and isNumber and isExpNumber:
                        self.getErrorLex("-- Обработка: + при статусе Экспонента " + stack, 3)
                        stack += char
                        isExpNumber = False

                    elif char == "{":

                            isComment = True
                            index += 1
                            self.getErrorLex("Комментарий", 3)

                    # встречен пробел или разделитель
                    elif char.isspace() or char in self.delimiters or index == (len(code)-1) or char == ";" or char == "|" or char == "="  or char == "&":
                        self.getErrorLex("Обнаружен разделитель: " + char + " при статусе: Число (" + str(isNumber) + "), Слово (" + str(isWord) + ")", 3)
                        if index == (len(code)-1):
                            if char == ".":
                                self.getErrorLex("Обнаружено завершение программы", 3)
                        elif stack != "":
                            if isNumber == True:
                                self.numbers.append(stack)
                                lexemes.append(Lexem(stack, countLexem, 3, len(self.numbers)-1))
                                self.getErrorLex("Собрано: число " + stack, 3)
                                if self.getNumberSystem(stack) == 1:
                                    self.getErrorLex("Неверное представление числа " + stack, 1)
                                    return 1
                                    break
                                else:
                                    self.numbersTypeData.append(self.getNumberSystem(stack))
                                if isNumber:
                                    self.getErrorLex("Отключение статуса Число", 3)
                                if isExpNumber:
                                    self.getErrorLex("Отключение статуса Экспонента", 3)
                                isNumber = False
                                isExpNumber = False


                                stack = ""
                                self.getErrorLex("Опустошение буфера", 4)
                            elif stack in self.keywords:
                                lexemes.append(Lexem(stack, countLexem, 1, self.keywords.index(stack)))
                                self.getErrorLex("Собрано: ключевое слово " + stack, 2)
                                stack = ""
                                self.getErrorLex("Опустошение буфера", 4)
                                countLexem += 1
                                isWord = False
                                self.getErrorLex("Отключение статуса Слово.", 3)
                            elif stack in self.delimiters:
                                lexemes.append(Lexem(stack, countLexem, 2, self.delimiters.index(stack)))
                                self.getErrorLex("Собрано: разделитель " + stack, 2)
                                stack = ""
                                self.getErrorLex("Опустошение буфера", 4)
                                countLexem += 1
                            elif stack in self.identificators:
                                lexemes.append(Lexem(stack, countLexem, 4, self.identificators.index(stack)))
                                self.getErrorLex("Собрано: идентификатор " + stack, 2)
                                stack = ""
                                self.getErrorLex("Опустошение буфера", 4)
                                countLexem += 1
                                isWord = False
                                self.getErrorLex("Отключение статуса Слово.", 3)
                            else:
                                if isWord == True:
                                    self.identificators.append(stack)
                                    lexemes.append(Lexem(stack, countLexem, 4, self.identificators.index(stack)))
                                    self.getErrorLex("Собрано: новый идентификатор " + stack, 2)
                                    isWord = False
                                    self.getErrorLex("Отключение статуса Слово.", 3)
                                    stack = ""
                                else:
                                    self.getErrorLex("Ошибка лексического анализа", 1)
                                    error = 1
                                    break
                                stack = ""
                                self.getErrorLex("Опустошение буфера", 4)
                                countLexem += 1

                        if char == ":":
                            self.getErrorLex("-- Обработка: возможен составной разделитель, сбор в буфер " + char, 4)
                            if code[index+1] == "=":
                                lexemes.append(Lexem(char + code[index+1], countLexem, 2, self.delimiters.index(":=")))
                                self.getErrorLex("Собрано: составной разделитель " + char + code[index+1], 2)
                                index += 1
                                self.getErrorLex("Опустошение буфера", 4)
                            else:
                                lexemes.append(Lexem(char, countLexem, 2, self.delimiters.index(":")))
                        elif char == "|":
                            self.getErrorLex("-- Обработка: возможен составной разделитель, сбор в буфер " + char, 4)
                            if code[index+1] == "|":
                                lexemes.append(Lexem(char + code[index+1], countLexem, 2, self.delimiters.index("||")))
                                self.getErrorLex("Собрано: составной разделитель " + char + code[index+1], 2)
                                index += 1
                                self.getErrorLex("Опустошение буфера", 4)
                            else:
                                self.getErrorLex("Ошибка записи двойного разделителя ||", 1)
                                error = 1
                                break
                        elif char == "&":
                            self.getErrorLex("-- Обработка: возможен составной разделитель, сбор в буфер " + char, 4)
                            if code[index+1] == "&":
                                lexemes.append(Lexem(char + code[index+1], countLexem, 2, self.delimiters.index("&&")))
                                self.getErrorLex("Собрано: составной разделитель " + char + code[index+1], 2)
                                index += 1
                                self.getErrorLex("Опустошение буфера", 4)
                            else:
                                self.getErrorLex("Ошибка записи двойного разделителя &&", 1)

                                error = 1
                                break
                        elif char == "!" and code[index + 1] == ";":
                            lexemes.append(Lexem(char, countLexem, 1, self.keywords.index(char)))
                            self.getErrorLex("Собрано: ключевое слово " + char, 2)
                            countLexem += 1
                        elif char == "!":
                            self.getErrorLex("-- Обработка: возможен составной разделитель, сбор в буфер " + char, 4)
                            if code[index+1] == "=":
                                lexemes.append(Lexem(char + code[index+1], countLexem, 2, self.delimiters.index("!=")))
                                self.getErrorLex("Собрано: составной разделитель " + char + code[index+1], 2)
                                index += 1
                                self.getErrorLex("Опустошение буфера", 4)
                            else:
                                lexemes.append(Lexem(char, countLexem, 2, self.delimiters.index("!")))
                        elif char == "<":
                            self.getErrorLex("-- Обработка: возможен составной разделитель, сбор в буфер " + char, 4)
                            if code[index+1] == "=":
                                lexemes.append(Lexem(char + code[index+1], countLexem, 2, self.delimiters.index("<=")))
                                self.getErrorLex("Собрано: составной разделитель " + char + code[index+1], 2)
                                index += 1
                                self.getErrorLex("Опустошение буфера", 4)
                            else:
                                lexemes.append(Lexem(char, countLexem, 2, self.delimiters.index("<")))
                        elif char == ">":
                            self.getErrorLex("-- Обработка: возможен составной разделитель, сбор в буфер " + char, 4)
                            if code[index+1] == "=":
                                lexemes.append(Lexem(char + code[index+1], countLexem, 2, self.delimiters.index(">=")))
                                self.getErrorLex("Собрано: составной разделитель " + char + code[index+1], 2)
                                index += 1
                                self.getErrorLex("Опустошение буфера", 4)
                            else:
                                lexemes.append(Lexem(char, countLexem, 2, self.delimiters.index(">")))
                        elif char == "=":
                            self.getErrorLex("-- Обработка: возможен составной разделитель, сбор в буфер " + char, 4)
                            if code[index+1] == "=":
                                lexemes.append(Lexem(char + code[index+1], countLexem, 2, self.delimiters.index("==")))
                                self.getErrorLex("Собрано: составной разделитель " + char + code[index+1], 2)
                                index += 1
                                self.getErrorLex("Опустошение буфера", 4)
                            else:
                                self.getErrorLex("Ошибка записи двойного разделителя ==", 1)
                                error = 1
                                break
                        elif char in self.delimiters:
                            lexemes.append(Lexem(char, countLexem, 2, self.delimiters.index(char)))
                            self.getErrorLex("Собрано: разделитель " + char, 3)
                        elif char == ";":
                            lexemes.append(Lexem("Перенос строки", countLexem, 2, 18))

                    elif char == "%":
                        lexemes.append(Lexem(char, countLexem, 1, self.keywords.index(char)))
                        self.getErrorLex("Собрано: ключевое слово " + char, 2)
                        countLexem += 1
                    elif char == "$":
                        lexemes.append(Lexem(char, countLexem, 1, self.keywords.index(char)))
                        self.getErrorLex("Собрано: ключевое слово " + char, 2)
                        countLexem += 1
                    else:
                        self.getErrorLex("Ошибка: Неизвестный символ " + char, 1)
                        error = 1
                        break


                elif char == "}":
                        index += 1
                        isComment = False
                        self.getErrorLex("Завершение комментария", 3)


                index += 1

            if error == 0:
                self.onDoneLexer(lexemes)
                ret = self.sintacticAnalizer(lexemes)
                if ret == 1:
                    return 1

    # функция синтаксического анализа: разбитие лексем на конструкции,
    # анализ строения конструкций,
    # просмотр правильности расстановки знаков
    def sintacticAnalizer(self, lexemes):
        error = 0
        self.sintacticLexemes = []

        self.getError("Синтаксический анализ...", 3)

        if lexemes[len(lexemes)-3].name in [";"] and lexemes[len(lexemes)-1].name == ".":
            begins = 1
            for k in lexemes:
                if k.name == "begin":
                    begins += 1
                elif k.name == "end":
                    begins -= 1
            if begins != 0:
                self.getError("Ошибка формирования составного оператора begin end", 1)
            index = 0
            sintacticLexemes = []
            stackLexemes = []
            flag = 0
            while index < len(lexemes):

                stackLexemes = []
                sintacticLexemes = []

                if lexemes[index].name == "begin":
                    while lexemes[index].name != "end":
                        stackLexemes.append(lexemes[index])
                        index += 1
                if index == (len(lexemes)-1):
                    stackLexemes.append(lexemes[index])
                    if lexemes[index].name == "begin":
                        flag = 1
                else:
                    while lexemes[index].name not in [";", "Перенос строки"] and index < len(lexemes):

                        stackLexemes.append(lexemes[index])
                        index += 1

                if flag != 1:
                    index += 2
                else:
                    index += 1

                if len(stackLexemes) > 0:

                    if self.sintacticInnerOperator(stackLexemes) == 1:
                        error = 1
                        break

                else:
                    self.getError("Обнаружен пустой оператор или описание", 1)
                    error = 1
                    break
        else:
            self.getError("Ошибка считывания программы: Неверно представлено завершение конструкции", 1)




    def sintacticInnerOperator(self, stackLexemes):
        error = 0



        # ДОРАБОТАТЬ СТРУКТУРЫ ДАБЫ БЫЛО ПРАВИЛЬНО ЕСЛИ ДВЕ СТРОКИ ТИПА ДАННЫХ
        # ЕЩЕ ЧТОБЫ ОПИСАНИЯ ВООБЩЕ МОГЛО НЕ БЫТЬ
        # обработка описания
        if stackLexemes[0].name == "program" and stackLexemes[1].name == "var" and stackLexemes[2].name != "begin":
            self.getError(">> Описание", 3)
            innerIndex = 2
            error = 0
            body = []
            waitIdent = True
            while innerIndex < len(stackLexemes):
                if waitIdent:
                    if stackLexemes[innerIndex].table == "Идентификатор":
                        body.append(stackLexemes[innerIndex])
                        waitIdent = False
                    elif stackLexemes[innerIndex].name == ",":
                        self.getError("Ошибка записи описания: ожидался идентификатор, а не символ разделения", 1)
                        error = 1
                        break
                    else:
                        self.getError("Ошибка записи описания: недопустимая лексема", 1)
                        error = 1
                        break
                elif not waitIdent:
                    if stackLexemes[innerIndex].name == ",":
                        waitIdent = True
                    elif stackLexemes[innerIndex].table == "Идентификатор":
                        self.getError("Ошибка записи описания: Ожидался символ разделения, а не идентификатор", 1)
                        error = 1
                        break
                    elif stackLexemes[innerIndex].name == ":" or stackLexemes[innerIndex].name in ["!", "%", "$"]:
                        break
                    else:
                        self.getError("Ошибка записи описания: Недопустимая лексема", 1)
                        error = 1
                        break
                innerIndex += 1

            if error == 0:
                bodyString = ""
                for s in body:
                    bodyString += s.name + " "
                self.getError("Собрано: Тело описания:", 2)
                self.getError(bodyString, 4)
            else:
                return 1
            if len(body) > 0:
                if waitIdent:
                    self.getError("Ошибка записи описания: ожидался идентификатор, а не символ разделения", 1)
                    error = 1
                    return 1
                self.sintacticLexemes.append(DescriptionStatement(stackLexemes[0], body))
            else:
                self.getError("Отсутствует тело описания", 1)
                error = 1

                return 1

            idents = ""
            for lex in body:
                idents += lex.name + " "
            n = len(stackLexemes)-1
            t = ""
            if stackLexemes[n].name == "%":
                t = "целый"
            elif stackLexemes[n].name == "!":
                t = "действительный"
            elif stackLexemes[n].name == "$":
                t = "логический"
            self.getError("Собрано: Описание, тип данных: " + t + " для " + idents, 2)


        # обработка присваивания
        elif stackLexemes[0].table == "Идентификатор":
            if len(stackLexemes) > 1:
                if stackLexemes[1].name == ":=":
                    if len(stackLexemes) > 2:
                        self.getError(">> Присваивание", 3)
                        bodyString = ""
                        for s in stackLexemes[2:]:
                            bodyString += s.name + " "
                            if s.table != "Ключевое слово" or s.name in ["true", "false"]:
                                pass
                            else:

                                self.getError("Ошибка формирования выражения: Ключевое слово " + s.name + " оператора в составе выражения", 1)
                                error = 1
                                return 1
                        self.getError("Собрано: оператор Присваивание для идентификатора " + stackLexemes[0].name + ", присвоено выражение: ", 2)
                        self.getError(bodyString, 4)
                        self.sintacticLexemes.append(AssignmentStatement(stackLexemes[0], stackLexemes[2:]))
                    else:
                        self.getError("Ошибка записи оператора Присваивания: Пустое тело", 1)
                        error = 1
                        return 1
                else:
                    self.getError("Неверная конструкция оператора присваивания", 1)
                    error = 1
                    return 1
            else:
                self.getError("Неверное расположение выражения", 1)
                error = 1
                return 1

        # обработка условного оператора
        elif stackLexemes[0].name == "if":
            self.getError(">> Условный оператор if", 3)
            if len(stackLexemes) == 1:
                self.getError("Ошибка записи выражения в условном операторе if: отсутствует условие и тело", 1)
                error = 1
                return 1
            condition = []
            thenBody = []
            elseBody = []
            innerIndex = 1
            exit = 0
            brackets = 1
            if stackLexemes[1].name != "(":
                self.getError("Ошибка записи выражения в условном операторе if: Условие начинается с (", 1)
                error = 1
                return 1
            innerIndex += 1
            while innerIndex < len(stackLexemes):
                if stackLexemes[innerIndex].name == "(":
                    brackets += 1
                elif stackLexemes[innerIndex].name == ")":
                    brackets -= 1
                if stackLexemes[innerIndex].name == ")" and brackets == 0:
                    break
                elif stackLexemes[innerIndex].name == ")" and brackets < 0:
                    self.getError("Ошибка записи выражения в условном операторе if: Нет открывающей скобки", 1)
                else:
                    condition.append(stackLexemes[innerIndex])
                innerIndex += 1
            if len(condition) == 2:
                self.getError("Отсутствует условие оператора if", 1)
                error = 1
                return 1
            if brackets == 0:
                bodyString = ""
                for s in condition:
                    bodyString += s.name + " "
                self.getError("Собрано: Условие if: ", 2)
                self.getError(bodyString, 4)

            else:
                self.getError("Ошибка записи выражения в условном операторе if: Непарные скобки", 1)
                error = 1
                return 1
            innerIndex += 1
            beginStatus = False
            elseStatus = False
            while innerIndex < len(stackLexemes):
                if stackLexemes[innerIndex].name == "begin":
                    beginStatus = True
                if stackLexemes[innerIndex].name == "(":
                    brackets += 1
                elif stackLexemes[innerIndex].name == ")":
                    brackets -= 1
                if stackLexemes[innerIndex].name == "else" and brackets == 0 and beginStatus == False:
                    elseStatus = True
                    break
                elif stackLexemes[innerIndex].name == ")" and brackets < 0:
                    self.getError("Ошибка записи выражения в условном операторе if: Нет открывающей скобки", 1)
                    error = 1
                    break
                else:
                    thenBody.append(stackLexemes[innerIndex])
                innerIndex += 1

            if len(thenBody) == 0:
                self.getError("Отсутствует тело оператора if (Истина)", 1)
                error = 1
                return 1
            else:
                bodyInnerBegin = []
                if thenBody[0].name == "begin":
                    self.getError("--- Анализ вложенности --- ", 3)
                    for lex in thenBody[1:len(thenBody)-1]:
                        if lex.name != ";":
                            bodyInnerBegin.append(lex)
                        else:
                            if self.sintacticInnerOperator(bodyInnerBegin) == 1:
                                error = 1
                                break
                            bodyInnerBegin = []

                    if len(bodyInnerBegin) > 0:
                        if self.sintacticInnerOperator(bodyInnerBegin) == 1:
                            return 1
                        bodyInnerBegin = []
                    self.getError("--- Завершение вложенности --- ", 3)
                else:
                    self.getError("--- Анализ вложенности --- ", 3)
                    if self.sintacticInnerOperator(thenBody) == 1:
                        error = 1
                        return 1
                    self.getError("--- Завершение вложенности --- ", 3)


            if brackets == 0:
                bodyString = ""
                for s in thenBody:
                    bodyString += s.name + " "
                self.getError("Собрано: Условие тело оператора if (Истина): " + bodyString, 2)
                self.getError(bodyString, 4)
            else:
                self.getError("Ошибка записи выражения в условном операторе if: Непарные скобки", 1)
                error = 1
                return 1
            innerIndex += 1
            beginStatus = False
            if elseStatus:
                while innerIndex < len(stackLexemes):
                    if stackLexemes[innerIndex].name == "(":
                        brackets += 1
                    elif stackLexemes[innerIndex].name == ")":
                        brackets -= 1
                    elif stackLexemes[innerIndex].name == ")" and brackets < 0:
                        self.getError("Ошибка записи выражения в условном операторе if: Нет открывающей скобки", 1)
                    else:
                        elseBody.append(stackLexemes[innerIndex])
                    innerIndex += 1
                if len(elseBody) == 0:
                    self.getError("Отсутствует тело оператора if (Ложь)", 1)
                    error = 1
                    return 1
                else:
                    bodyInnerBegin = []
                    if elseBody[0].name == "begin":
                        elseBody = elseBody[:-1]
                        self.getError("--- Анализ вложенности --- ", 3)
                        for lex in elseBody[1:len(elseBody)]:
                            if lex.name != ";":
                                bodyInnerBegin.append(lex)
                            else:
                                if self.sintacticInnerOperator(bodyInnerBegin) == 1:
                                    error = 1
                                    return 1
                                bodyInnerBegin = []

                        if len(bodyInnerBegin) > 0:
                            if self.sintacticInnerOperator(bodyInnerBegin) == 1:
                                return 1
                            bodyInnerBegin = []
                        self.getError("--- Завершение вложенности --- ", 3)
                    else:
                        self.getError("--- Анализ вложенности --- ", 3)
                        if self.sintacticInnerOperator(elseBody) == 1:
                            error = 1
                            return 1
                        self.getError("--- Завершение вложенности --- ", 3)

                if brackets == 0:
                    for s in elseBody:
                        bodyString += s.name + " "
                    self.getError("Собрано: тело оператора if (Ложь): ", 2)
                    self.getError(bodyString, 4)
                else:
                    self.getError("Ошибка записи выражения в условном операторе if: Непарные скобки", 1)
                    error = 1
                    return 1
                innerIndex += 1
            self.sintacticLexemes.append(IfStatement(condition, thenBody, elseBody))

        # обработка фиксированного цикла
        elif stackLexemes[0].name == "for":
            self.getError(">> Фиксированный цикл for", 3)
            if len(stackLexemes) == 1:
                self.getError("Ошибка записи выражения в условном операторе for: Отсутствует условие и тело", 1)
                error = 1
                return 1
            condition = []
            toBody = []
            stepBody = []
            body = []
            innerIndex = 1
            exit = 0
            brackets = 0
            if stackLexemes[1].table != "Идентификатор" or stackLexemes[2].name != ":=":
                self.getError("Ошибка записи выражения в операторе фиксированного цикла for: Неверная конструкция присваивания",1)
                error = 1
                return 1

            toStatus = False
            while innerIndex < len(stackLexemes):
                if stackLexemes[innerIndex].name != "to":
                    condition.append(stackLexemes[innerIndex])
                else:
                    toStatus = True
                    break
                innerIndex += 1
            if len(condition) == 0:
                self.getError("Ошибка в операторе фиксированного цикла for: Пустое присваивание", 1)
                error = 1
                return 1
            elif toStatus == False:
                self.getError("Ошибка в операторе фиксированного цикла for: Не обнаружена конструкция to", 1)
                error = 1
                return 1
            elif toStatus == True:
                toBodyStatus = True
                stepBodyStatus = False
                bodyStatus = False
                nextStatus = False
                innerIndex += 1
                while innerIndex < len(stackLexemes):
                    if toBodyStatus == True:
                        if stackLexemes[innerIndex].name != "step" and stackLexemes[innerIndex].name != "next":
                            if (stackLexemes[innerIndex].name in self.keywords and stackLexemes[innerIndex].name not in ["true", "false"]) or (stackLexemes[innerIndex].table == "Идентификатор" and stackLexemes[
                                innerIndex+1].name == ":="):
                                toBodyStatus = False
                                bodyStatus = True
                                innerIndex -= 1
                                if len(toBody) > 0:
                                    bodyString = ""
                                    for s in toBody:
                                        bodyString += s.name + " "
                                    self.getError("Собрано: Тело to оператора фиксированного цикла: ", 2)
                                    self.getError(bodyString, 4)
                                    self.getError("Переход к сбору тела...", 2)
                                else:
                                    self.getError(
                                        "Ошибка в операторе фиксированного цикла for: Отсутствует тело to цикла", 1)
                                    error = 1
                                    break
                            else:
                                toBody.append(stackLexemes[innerIndex])

                        elif stackLexemes[innerIndex].name == "step":
                            toBodyStatus = False
                            stepBodyStatus = True
                            if len(toBody) > 0:
                                bodyString = ""
                                for s in toBody:
                                    bodyString += s.name + " "
                                self.getError("Собрано: Тело to оператора фиксированного цикла: ", 2)
                                self.getError(bodyString, 4)
                                self.getError("Переход к сбору step...", 2)
                            else:
                                self.getError("Ошибка в операторе фиксированного цикла for: Отсутствует тело to цикла",
                                              1)
                                error = 1
                                break
                        elif stackLexemes[innerIndex].name == "next":
                            self.getError("Ошибка в операторе фиксированного цикла for: Отсутствует тело цикла", 1)
                            error = 1
                            break

                    elif stepBodyStatus == True:
                        if stackLexemes[innerIndex].name != "next":
                            if (stackLexemes[innerIndex].name in self.keywords and stackLexemes[
                                innerIndex].name not in ["true", "false"]) or (
                                    stackLexemes[innerIndex].table == "Идентификатор" and stackLexemes[
                                innerIndex + 1].name == ":="):
                                stepBodyStatus = False
                                bodyStatus = True
                                innerIndex -= 1
                                if len(stepBody) > 0:

                                    bodyString = ""
                                    for s in stepBody:
                                        bodyString += s.name + " "
                                    self.getError("Собрано: Тело step оператора фиксированного цикла:", 2)
                                    self.getError(bodyString, 4)
                                    self.getError("Переход к сбору тела...", 2)
                                else:
                                    self.getError("Ошибка в операторе фиксированного цикла for: Отсутствует тело step",
                                                  1)
                                    error = 1
                                    break
                            else:
                                stepBody.append(stackLexemes[innerIndex])

                        elif stackLexemes[innerIndex].name == "next":
                            self.getError("Ошибка в операторе фиксированного цикла for: Отсутствует тело цикла", 1)
                            error = 1
                            break

                    elif bodyStatus == True:
                        if stackLexemes[innerIndex].name != "next":
                            body.append(stackLexemes[innerIndex])

                        elif stackLexemes[innerIndex].name == "next":
                            if innerIndex == len(stackLexemes)-1:
                                nextStatus = True
                                bodyStatus = False
                                break
                            else:
                                self.getError("Ошибка в операторе фиксированного цикла for: После завершения конструкции обнаружена конструкция", 1)
                                break
                    innerIndex += 1

                if nextStatus == True and error == 0:
                    bodyString = ""
                    for s in body:
                        bodyString += s.name + " "
                    self.getError("Собрано: Тело оператора фиксированного цикла for:", 2)
                    self.getError(bodyString, 4)
                    self.sintacticLexemes.append(ForLoop(condition, toBody, stepBody, body))
                    bodyInnerBegin = []
                    if body[0].name == "begin":
                        self.getError("--- Анализ вложенности --- ", 3)
                        for lex in body[1:len(body) - 1]:
                            if lex.name != ";":
                                bodyInnerBegin.append(lex)
                            else:
                                if self.sintacticInnerOperator(bodyInnerBegin) == 1:
                                    error = 1
                                    break
                                bodyInnerBegin = []
                        if len(bodyInnerBegin) > 0:
                            self.sintacticInnerOperator(bodyInnerBegin)
                            bodyInnerBegin = []
                        self.getError("--- Завершение вложенности --- ", 3)
                    else:
                        self.getError("--- Анализ вложенности --- ", 3)
                        if self.sintacticInnerOperator(body) == 1:
                            return 1
                        self.getError("--- Завершение вложенности --- ", 3)

                elif error == 0:
                    self.getError("Ошибка в операторе фиксированного цикла for: Не обнаружено корректное завершение next", 1)
                    error = 1
                    return 1
                else:
                    return 1

        # обработка условного цикла
        elif stackLexemes[0].name == "while":
            self.getError(">> Условный цикл while", 3)
            if len(stackLexemes) == 1:
                self.getError("Ошибка записи выражения в условном операторе while: Отсутствует условие и тело", 1)
                error = 1
                return 1

            condition = []
            body = []
            innerIndex = 1
            exit = 0
            brackets = 1
            if stackLexemes[1].name != "(":
                self.getError("Ошибка записи выражения в условном операторе while: Условие начинается с (", 1)
                error = 1
                return 1
            innerIndex += 1
            while innerIndex < len(stackLexemes):
                if stackLexemes[innerIndex].name == "(":
                    brackets += 1
                elif stackLexemes[innerIndex].name == ")":
                    brackets -= 1
                if stackLexemes[innerIndex].name == ")" and brackets == 0:
                    break
                elif stackLexemes[innerIndex].name == ")" and brackets < 0:
                    self.getError("Ошибка записи выражения в условном операторе while: Нет открывающей скобки", 1)
                else:
                    condition.append(stackLexemes[innerIndex])
                # condition.append(stackLexemes[innerIndex])
                innerIndex += 1
            if len(condition) == 2:
                self.getError("Отсутствует условие оператора while", 1)
                error = 1
                return 1
            if brackets == 0 and len(condition) > 0:
                bodyString = ""
                for s in condition:
                    bodyString += s.name + " "
                self.getError("Собрано: Условие while", 2)
                self.getError(bodyString, 4)
            elif len(condition) == 0:
                self.getError("Ошибка записи выражения в условном операторе while: Отсутствие условия", 1)
                error = 1
                return 1
            else:
                self.getError("Ошибка записи выражения в условном операторе while: Непарные скобки", 1)
                error = 1
                return 1
            innerIndex += 1

            while innerIndex < len(stackLexemes):
                body.append(stackLexemes[innerIndex])
                innerIndex += 1

            if len(body) == 0:
                self.getError("Ошибка в операторе фиксированного цикла while: Отсутствие тела", 1)
                error = 1
                return 1
            else:
                bodyString = ""
                for s in body:
                    bodyString += s.name + " "
                self.getError("Собрано: Тело while:", 2)
                self.getError(bodyString, 4)

                self.sintacticLexemes.append(WhileLoop(condition, body))
                bodyInnerBegin = []
                if body[0].name == "begin":
                    self.getError("--- Анализ вложенности --- ", 3)
                    for lex in body[1:len(body) - 1]:
                        if lex.name != ";":
                            bodyInnerBegin.append(lex)
                        else:
                            if self.sintacticInnerOperator(bodyInnerBegin) == 1:
                                error = 1
                                break
                            bodyInnerBegin = []
                    if len(bodyInnerBegin) > 0:
                        if self.sintacticInnerOperator(bodyInnerBegin) == 1:
                            return 1
                        bodyInnerBegin = []
                    self.getError("--- Завершение вложенности --- ", 3)
                else:
                    self.getError("--- Анализ вложенности --- ", 3)
                    if self.sintacticInnerOperator(body) == 1:
                        return 1
                    self.getError("--- Завершение вложенности --- ", 3)

        # обработка оператора ввода
        elif stackLexemes[0].name == "readln":
            self.getError(">> Оператор чтения данных readln", 3)
            if len(stackLexemes) == 1:
                self.getError("Ошибка записи оператора readln: Отсутствует тело", 1)
                error = 1
                return 1
            body = []
            innerIndex = 1
            bodyInner = []
            waitIdent = True
            while innerIndex < len(stackLexemes):
                if waitIdent:
                    if stackLexemes[innerIndex].table == "Идентификатор":
                        body.append(stackLexemes[innerIndex])
                        waitIdent = False
                    elif stackLexemes[innerIndex].name == ",":
                        self.getError("Ошибка записи оператора readln: Ожидался идентификатор, а не символ разделения",
                                      1)
                        error = 1
                        break
                    else:
                        self.getError("Ошибка записи оператора readln: Недопустимая лексема " + stackLexemes[innerIndex].name, 1)
                        error = 1
                        break
                elif not waitIdent:
                    if stackLexemes[innerIndex].name == ",":
                        body.append(stackLexemes[innerIndex])
                        waitIdent = True
                    elif stackLexemes[innerIndex].table == "Идентификатор":
                        self.getError("Ошибка записи оператора readln: Ожидался символ разделения, а не идентификатор",
                                      1)
                        error = 1
                        break
                    else:
                        self.getError("Ошибка записи оператора readln: Недопустимая лексема " + stackLexemes[innerIndex].name, 1)
                        error = 1
                        break
                innerIndex += 1

            if error == 1:
                return 1

            if waitIdent or len(body) == 0:
                self.getError("Ошибка записи оператора readln: Ожидался идентификатор", 1)
                error = 1
                return 1
            bodyString = ""
            for s in body:
                bodyString += s.name + " "
            self.getError("Собрано: Тело readln:", 2)
            self.getError(bodyString, 4)
            self.sintacticLexemes.append(ReadStatement(body))

        # обработка оператора вывода
        elif stackLexemes[0].name == "writeln":
            self.getError(">> Оператор чтения данных writeln", 3)
            if len(stackLexemes) == 1:
                self.getError("Ошибка записи оператора writeln: Отсутствует тело", 1)
                error = 1
                return 1
            body = []
            innerIndex = 1
            bodyInner = []

            waitIdent = True
            delimStatus = False
            while innerIndex < len(stackLexemes):
                if stackLexemes[innerIndex].name == ",":
                    delimStatus = True
                    if len(bodyInner) > 0:
                        for k in bodyInner:
                            print(k.table, k.name)
                            if k.table == "Ключевое слово":
                                self.getError("Ошибка записи оператора writeln: Недопустимое выражение", 1)
                                error = 1
                                break
                        body.append(bodyInner)
                    else:
                        self.getError("Ошибка записи оператора writeln: Отсутствует выражение", 1)
                        error = 1
                        break
                    bodyInner = []
                else:
                    bodyInner.append(stackLexemes[innerIndex])
                    delimStatus = False
                innerIndex += 1

            if error == 1:
                return 1

            if len(bodyInner) > 0:
                body.append(bodyInner)
                bodyInner = []

            else:
                self.getError("Ошибка записи оператора writeln: Ожидалось выражение", 1)
                error = 1
                return 1

            if len(body) > 0:
                bodyString = ""
                for s in body:
                    for k in s:
                        if k.table == "Ключевое слово":
                            self.getError("Ошибка записи оператора writeln: Недопустимое выражение", 1)
                            error = 1
                            break
                        bodyString += k.name + " "
                self.getError("Собрано: Тело writeln:", 2)
                self.getError(bodyString, 4)
                self.sintacticLexemes.append(WriteStatement(body))

            else:
                self.getError("Ошибка записи оператора writeln: Отсутствует тело", 1)
                error = 1
                return 1

        # обработка составного оператора
        elif stackLexemes[0].name == "begin":

            self.getError(">> Составной оператор begin end", 3)
            body = []
            bodyInner = []
            innerIndex = 1
            begs = 1
            while innerIndex < len(stackLexemes):
                if stackLexemes[innerIndex].name == "begin":
                    begs += 1
                elif stackLexemes[innerIndex].name == "end":
                    begs -= 1
                elif stackLexemes[innerIndex].name == ";" and begs == 1:
                    if len(bodyInner) > 0:
                        body.append(bodyInner)
                        bodyString = ""
                        for s in bodyInner:
                            bodyString += s.name + " "
                        self.getError("Собрано: Вложенный оператор:", 2)
                        self.getError(bodyString, 4)
                        bodyInnerBegin = []
                        if bodyInner[0].name == "begin":
                            self.getError("--- Анализ вложенности --- ", 3)
                            for lex in bodyInner[1:len(bodyInner)-1]:
                                if lex.name != ";":
                                    bodyInnerBegin.append(lex)
                                else:
                                    if self.sintacticInnerOperator(bodyInnerBegin) == 1:
                                        error = 1
                                        break
                                    bodyInnerBegin = []
                            if len(bodyInnerBegin) > 0:
                                if self.sintacticInnerOperator(bodyInnerBegin) == 1:
                                    return 1
                                bodyInnerBegin = []
                            self.getError("--- Завершение вложенности --- ", 3)
                        else:
                            self.getError("--- Анализ вложенности --- ", 3)
                            if self.sintacticInnerOperator(bodyInner) == 1:
                                return 1
                            self.getError("--- Завершение вложенности --- ", 3)
                        bodyInner = []

                        innerIndex += 1
                    else:
                        self.getError("Отсутствует оператор в теле составного оператора", 1)
                        error = 1
                        break
                bodyInner.append(stackLexemes[innerIndex])
                innerIndex += 1

            if len(bodyInner[:-1]) > 0:
                bodyInner = bodyInner[:-1]
                body.append(bodyInner)
                bodyString = ""
                for s in bodyInner:
                    bodyString += s.name + " "
                self.getError("Собрано: Вложенный оператор:", 2)
                self.getError(bodyString, 4)
                bodyInnerBegin = []
                if bodyInner[0].name == "begin":
                    self.getError("--- Анализ вложенности --- ", 3)
                    for lex in body[1:len(bodyInner)]:
                        if lex.name != ";":
                            bodyInnerBegin.append(lex)
                        else:
                            if self.sintacticInnerOperator(bodyInnerBegin) == 1:
                                error = 1
                                break
                            bodyInnerBegin = []
                    if len(bodyInnerBegin) > 0:
                        if self.sintacticInnerOperator(bodyInnerBegin) == 1:
                            return 1
                        bodyInnerBegin = []
                    self.getError("--- Завершение вложенности --- ", 3)
                else:
                    self.getError("--- Анализ вложенности --- ", 3)
                    if self.sintacticInnerOperator(bodyInner) == 1:
                        return 1
                    self.getError("--- Завершение вложенности --- ", 3)
                innerIndex += 1
            else:
                self.getError("Отсутствует оператор в теле составного оператора", 1)
                error = 1
                return 1
            bodyInner = []
            self.sintacticLexemes.append(BefinEndOperator(body))
            bodyInnerBegin = []

        elif stackLexemes[1].name == "." and len(stackLexemes) == 2:
            if error == 0:
                self.getError(">> Завершение программы", 3)
                self.semanticAnalizer()
            else:
                error = 1
                return 1
        else:
            self.getError("Неверное представление конструкции: лексема " + stackLexemes[0].name + " обнаружена в неположеном месте.", 1)
            error = 1
            return 1

        if error == 1:
            return 1

    def analizeExpression(self, expression):
        innerIndex = 0
        lexemesInner = []
        lexemes = []
        isLogical = False
        znaks = ["+", "-", "*", "/", "!", "||", "&&", "<", "<=", ">", ">=", "!=", "=="]

        if len(expression) > 1:
            for lex in range(len(expression)):
                if expression[lex].table != "Ключевое слово" or expression[lex].name in ["true", "false"]:

                    print("да", expression[lex].table, expression[lex].name)
                    if expression[lex].name == "(":
                        if lex == 0:
                            if expression[lex+1].name in ["(", "true", "false"] or expression[lex+1].table in ["Идентификатор", "Число"]:
                                pass
                            else:
                                self.getError("Ошибка формирования выражения", 1)
                        elif lex == (len(expression)-1):
                            self.getError("Ошибка формирования выражения", 1)
                        else:
                            if (expression[lex + 1].name in ["(", "true", "false"] or expression[lex + 1].table in ["Идентификатор", "Число"]) and (expression[lex - 1].name == "(" or expression[lex - 1].name in znaks):
                                pass
                            else:
                                self.getError("Ошибка формирования выражения", 1)
                    elif expression[lex].name == ")":
                        if lex == 0:
                            self.getError("Ошибка формирования выражения", 1)
                        elif lex == (len(expression)-1):
                            if expression[lex - 1].name in [")", "true", "false"]:
                                pass
                            else:
                                self.getError("Ошибка формирования выражения", 1)
                        else:
                            if (expression[lex - 1].name in [")", "true", "false"] or expression[lex - 1].table in ["Идентификатор", "Число"]) and (expression[lex + 1].name in znaks):
                                pass
                            else:
                                self.getError("Ошибка формирования выражения", 1)
                    elif expression[lex].table == "Число":
                        if lex == 0:
                            if expression[lex + 1].name in znaks:
                                pass
                            else:
                                self.getError("Ошибка формирования выражения", 1)
                        elif lex == (len(expression)-1):
                            if expression[lex - 1].name in znaks:
                                pass
                            else:
                                self.getError("Ошибка формирования выражения", 1)
                        else:
                            if (expression[lex - 1].name in ["("] or expression[lex - 1].name in znaks) and (expression[lex + 1].name in [")"] or expression[lex + 1].name in znaks):
                                pass
                            else:
                                self.getError("Ошибка формирования выражения", 1)
                    elif expression[lex].table == "Идентификатор":
                        if lex == 0:
                            if expression[lex + 1].name in znaks:
                                pass
                            else:
                                self.getError("Ошибка формирования выражения", 1)
                        elif lex == (len(expression) - 1):
                            if expression[lex - 1].name in znaks:
                                pass
                            else:
                                self.getError("Ошибка формирования выражения", 1)
                        else:
                            if (expression[lex - 1].name in ["("] or expression[lex - 1].name in znaks) and (
                                    expression[lex + 1].name in [")"] or expression[lex + 1].name in znaks):
                                pass
                            else:
                                self.getError("Ошибка формирования выражения", 1)
                    elif expression[lex].name in znaks and expression[lex].name != "!":
                        if lex == 0:
                                self.getError("Ошибка формирования выражения", 1)
                        elif lex == (len(expression) - 1):
                                self.getError("Ошибка формирования выражения", 1)
                        else:
                            if (expression[lex - 1].table in ["Идентификатор", "Число"] or expression[lex - 1].name == ")") and (expression[lex + 1].table in ["Идентификатор", "Число"] or expression[lex - 1].name == "("):
                                pass
                            else:
                                self.getError("Ошибка формирования выражения", 1)
                    elif expression[lex].name == "!":
                        if lex == 0:
                            if expression[lex + 1].table == "Идентификатор" or expression[lex + 1].name in ["(", "true", "false"]:
                                pass
                            else:
                                self.getError("Ошибка формирования выражения", 1)
                        elif lex == (len(expression)-1):
                            self.getError("Ошибка формирования выражения", 1)
                        else:
                            if (expression[lex + 1].table == "Идентификатор" or expression[lex + 1].name in ["(", "true", "false"]) and (expression[lex - 1].name in znaks):
                                pass
                            else:
                                self.getError("Ошибка формирования выражения", 1)
                else:
                    print("нет", expression[lex].table, expression[lex].name)
                    self.getError("Ошибка формирования выражения: Ключевое слово "+expression[lex].name+" оператора в составе выражения", 1)
            for lex in expression:
                if lex.name != "&&" and lex.name != "||":
                    lexemesInner.append(lex)
                else:
                    isLogical = True
                    lexemes.append(lexemesInner)
                    lexemesInner = []

            if len(lexemesInner) > 0:
                lexemes.append(lexemesInner)
                lexemesInner = []

        isFloat = False
        for lex in expression:
            if lex.name in ["true", "false", ">", "<", "==", "<=", ">=", "!="]:
                isLogical = True
            elif lex.table == "Идентификатор":
                if self.descriptionIdentificators[lex.name].name == "bool":
                    isLogical = True
                elif self.descriptionIdentificators[lex.name].name == "float":
                    isFloat = True
            elif lex.table == "Число":
                if self.numbersTypeData[self.numbers.index(lex.name)][0] == "Д":
                    isFloat = True
            elif lex.name == "/":
                isFloat = True

        if isLogical == True:
            # в выражении есть конъюнкция или дизъюнкция,
            # которая может быть только между логическими типами данных
            # for innerExp in lexemes:
            return "bool"
        elif isFloat == True:
            return "float"
        else:
            return "int"

    def analizeExpressionReturnedType(self, expression, typeExpression):
        pass

    def convert_to_binary(self, number_str, base):
        if all(char.isdigit() for char in number_str):
            number = int(number_str)
        elif 'B' in number_str.upper():
            number = int(number_str[:-1], 2)
        elif 'O' in number_str.upper():
            number = int(number_str[:-1], 8)
        elif 'D' in number_str.upper():
            number = int(number_str[:-1])
        elif 'H' in number_str.upper():
            number = int(number_str[:-2], 16)
        else:  # Предположим, что число вещественное или в научной форме
            number = float(number_str)

        if base == 2:
            return bin(int(number))
        elif base == 8:
            return oct(int(number))
        elif base == 10:
            return bin(int(number))[2:]
        elif base == 16:
            return hex(int(number))
        else:
            return "Invalid base"

    # семантический анализ: логическая проверка - совместимы ли типы данных
    def semanticAnalizer(self):
        self.getError("Синтаксический анализ успешно завершен", 2)
        self.getErrorSem("Семантический анализ...", 3)
        self.descriptionIdentificators = {}
        self.initialazedIndificators = []
        error = 0
        for lexemCostruction in self.sintacticLexemes:
            if isinstance(lexemCostruction, DescriptionStatement):
                for i in lexemCostruction.body:
                    if i.name not in self.descriptionIdentificators:
                        self.descriptionIdentificators[i.name] = lexemCostruction.typeData
                        self.getErrorSem("Идентификатор " + i.name + " описан, тип данных " + lexemCostruction.typeData.name , 2)
                    else:
                        self.getErrorSem("Идентификатор " + i.name + " уже был описан", 1)
                        error = 1
                        break
            elif isinstance(lexemCostruction, AssignmentStatement):
                if lexemCostruction.identificator.name in self.descriptionIdentificators:
                    if lexemCostruction.identificator.name not in self.initialazedIndificators:
                        self.initialazedIndificators.append(lexemCostruction.identificator.name)
                        self.getErrorSem("Идентификатор " + lexemCostruction.identificator.name + " инициализирован", 2)
                    else:
                        self.getErrorSem("Идентификатор " + lexemCostruction.identificator.name + " переопределен", 2)
                else:
                    self.getErrorSem("Идентификатор " + lexemCostruction.identificator.name + " не описан", 1)
                    error = 1
                    break

                if self.analizeExpression(lexemCostruction.body) == self.descriptionIdentificators[lexemCostruction.identificator.name].name:
                    self.getErrorSem("Проверка оператора присваивания: Тип данных совпадает", 2)
                else:
                    tr = self.analizeExpression(lexemCostruction.body)
                    t = ""
                    if tr == "int":
                        t = "целый"
                    elif tr == "float":
                        t = "действительный"
                    elif tr == "bool":
                        t = "логический"
                    self.getErrorSem("Проверка оператора присваивания: \nНесовпадение типов данных " + lexemCostruction.identificator.name + " и выражения с возвратом тип данных: " + t, 1)
                    error = 1
                    break
            elif isinstance(lexemCostruction, ReadStatement):
                for i in lexemCostruction.body:
                    if i.name == ",":
                        pass
                    else:
                        if i.name in self.descriptionIdentificators:
                            if i.name not in self.initialazedIndificators:
                                self.initialazedIndificators.append(i.name)
                                self.getErrorSem("Идентификатор " + i.name + " инициализирован", 2)
                            else:
                                self.getErrorSem("Идентификатор " + i.name + " переопределен", 2)
                        else:
                            self.getErrorSem("Идентификатор " + i.name + " не описан", 1)
                            error = 1
                            break
            elif isinstance(lexemCostruction, ForLoop):
                if self.analizeExpression(lexemCostruction.assignment[2:]) == "int" and self.analizeExpression(lexemCostruction.assignment[2:]) == self.descriptionIdentificators[lexemCostruction.assignment[0].name].name:
                    self.getErrorSem("Проверка цикла for: В операторе присваивания целый тип данных", 2)
                else:
                    self.getErrorSem("Ошибка цикла for: В операторе присваивания ожидался целый тип данных", 1)
                    error = 1
                    break

                if self.analizeExpression(lexemCostruction.toBody) == "int":
                    self.getErrorSem("Проверка цикла for: В теле to целый тип данных", 2)
                else:
                    self.getErrorSem("Ошибка цикла for: В теле to ожидался целый тип данных", 1)
                    error = 1
                    break

                if len(lexemCostruction.stepBody) > 0:
                    if self.analizeExpression(lexemCostruction.stepBody) == "int":
                        self.getErrorSem("Проверка цикла for: В теле step целый тип данных", 2)
                    else:
                        self.getErrorSem("Ошибка цикла for: В теле step ожидался целый тип данных", 1)
                        error = 1
                        break
            elif isinstance(lexemCostruction, WhileLoop):
                if self.analizeExpression(lexemCostruction.condition) == "bool":
                    self.getErrorSem("Проверка цикла while: В условии логический тип данных", 2)
                else:
                    self.getErrorSem("Ошибка цикла while: В условии ожидался логический тип данных", 1)
                    error = 1
                    break
            elif isinstance(lexemCostruction, IfStatement):
                if self.analizeExpression(lexemCostruction.condition) == "bool":
                    self.getErrorSem("Проверка цикла if: В условии логический тип данных", 2)
                else:
                    self.getErrorSem("Ошибка цикла if: В условии ожидался логический тип данных ", 1)
                    error = 1
                    break
            elif isinstance(lexemCostruction, WriteStatement):
                for lexemBody in lexemCostruction.body:
                    self.analizeExpression(lexemBody)

        row = 0
        t = ""
        if error == 0:
            for number in self.numbers:
                type = self.numbersTypeData[self.numbers.index(number)]
                if type == "Ц10CC":
                    self.getErrorSem("Перевод в бинарное представление: " + str(number) + " => " + str(self.convert_to_binary(number, 10)), 3)
                elif type == "Ц2CC":
                    self.getErrorSem("Перевод в бинарное представление: " + str(number) + " => " + str(self.convert_to_binary(number, 2)), 3)
                elif type == "Ц8CC":
                    self.getErrorSem("Перевод в бинарное представление: " + str(number) + " => " + str(self.convert_to_binary(number, 8)), 3)
                elif type == "Ц16CC":
                    self.getErrorSem("Перевод в бинарное представление: " + str(number) + " => " + str(self.convert_to_binary(number, 16)), 3)
                else:
                    self.getErrorSem("Перевод в бинарное представление: " + str(number) + " => " + str(self.convert_to_binary(number, 10)), 3)

            for value in self.identificators:
                value_item = QTableWidgetItem(value)
                self.tableWidget_4.setItem(row, 0, value_item)
                if value in self.descriptionIdentificators:
                    if self.descriptionIdentificators[value].name == "%":
                        t = "целый"
                    elif self.descriptionIdentificators[value].name == "!":
                        t = "действительный"
                    elif self.descriptionIdentificators[value].name == "$":
                        t = "логический"
                value_item = QTableWidgetItem(t)
                self.tableWidget_4.setItem(row, 1, value_item)
                row += 1
            self.getErrorSem("Семантический анализ успешно завершен", 2)


app = QtWidgets.QApplication(sys.argv)
window = Window()
window.show()
app.exec_()