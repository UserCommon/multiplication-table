import sys
import json

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QDoubleValidator, QValidator
from random import randint, choice

from stats import Stats


class ProblemCreator:
    def __init__(self):
        self.wins: int = 0
        self.looses: int = 0

        self.a: int = 0
        self.b: int = 0
        self.answer = self.a * self.b

    def update_poblem(self):
        self.a = randint(1, 10)
        self.b = randint(1, 10)
        self.answer = self.a * self.b


class ClassicMode(QtWidgets.QMainWindow, ProblemCreator):
    def __init__(self):
        super(ClassicMode, self).__init__()
        uic.loadUi("resources/ui/main.ui", self)
        self.updating()
        self.label_update()
        self.button_collection = [
            self.pushButton,
            self.pushButton_2,
            self.pushButton_3,
            self.pushButton_4
        ]

        self.pushButton_5.hide()
        self.label_2.hide()

        self.pushButton_5.clicked.connect(self.ready_click)
        for button in self.button_collection:
            button.clicked.connect(self.on_click)

        self.show()

    def updating(self):
        self.update_poblem()
        self.button_text_update()
        self.label_update()

    def label_update(self):
        self.label.setText(f"{self.a}*{self.b}=?")

    def button_text_update(self):
        to_choose = [self.pushButton, self.pushButton_2, self.pushButton_3, self.pushButton_4]
        choosen = choice(to_choose)
        choosen.setText(f"{self.answer}")
        to_choose.remove(choosen)

        for button in to_choose:
            button.setText(f"{randint(1, 10) * randint(1, 10)}")

    def on_click(self):
        if int(self.sender().text()) == self.answer:
            self.label.setText("Молодец!")
            self.wins += 1
            stats.add_to_stats("wins", f"{self.a}", f"{self.a}x{self.b}")
        else:
            self.looses += 1
            stats.add_to_stats("loses", f"{self.a}", f"{self.a}x{self.b}")
            self.label.setText(f"Нет! Правильный ответ: {self.answer}")

        for button in self.button_collection:
            button.hide()

        self.pushButton_5.show()
        self.label_2.setText(f"Правильно: {self.wins} Неправильно: {self.looses} Всего: {(self.looses + self.wins)}")
        self.label_2.show()

    def ready_click(self):
        self.sender().hide()
        for button in self.button_collection:
            button.show()
        self.updating()


class ProMode(QtWidgets.QMainWindow, ProblemCreator):
    def __init__(self):
        self.active = True
        super(ProMode, self).__init__()
        uic.loadUi("resources/ui/pro.ui", self)
        self.updating()
        self.lineEdit.editingFinished.connect(self.answer_ready)
        self.pushButton_5.clicked.connect(self.ready_click)

        self.show()
        self.pushButton_5.hide()

    def validate(self) -> str:
        validation_rule = QDoubleValidator(-100, 100, 0)
        return validation_rule.validate(self.lineEdit.text(), 14)[1]

    def updating(self):
        self.update_poblem()
        self.label_update()

    def label_update(self):
        self.label.setText(f"{self.a}*{self.b} = ?")

    def answer_ready(self):
        try:
            if self.active:
                if int(self.validate()) == self.answer:
                    self.label.setText("Молодец!")
                    self.wins += 1
                    stats.add_to_stats("wins", f"{self.a}", f"{self.a}x{self.b}")
                else:
                    self.looses += 1
                    stats.add_to_stats("loses", f"{self.a}", f"{self.a}x{self.b}")
                    self.label.setText(f"Нет! Правильный ответ: {self.answer}")

                self.pushButton_5.show()
                self.label_2.setText(f"Правильно: {self.wins} Неправильно: {self.looses} Всего: {(self.looses + self.wins)}")
                self.label_2.show()

                self.lineEdit.setReadOnly(1)
                self.active = False
        except ValueError:
            print("Invalid input!")

    def ready_click(self):
        self.sender().hide()
        self.updating()
        self.lineEdit.setText("")
        self.active = True
        self.lineEdit.setReadOnly(0)


class Statistics(QtWidgets.QMainWindow):
    def __init__(self):
        super(Statistics, self).__init__()
        uic.loadUi("resources/ui/stats.ui", self)
        self.show()
        self.pushButton_2.clicked.connect(self.goto_menu)
        self.pushButton.clicked.connect(self.reset_statistics)
        self.draw_statistics()
        self.setFixedSize(800, 600)

    def draw_statistics(self):
        for wins_or_loses in stats.data.keys():
            for values in stats.data[wins_or_loses].items():
                for values_of_values in values:
                    data = []
                    if type(values_of_values) == dict:
                        data.append(values_of_values)

                    for element in data:
                        for (key, value) in zip(element.keys(), element.values()):
                            if wins_or_loses == "wins":
                                self.label_4.setText(self.label_4.text() + f"{key} {value} \n")
                            if wins_or_loses == "loses":
                                self.label_2.setText(self.label_2.text() + f"{key} {value} \n")
                            print(key, value)

        self.label_5.setText(self.label_5.text() + f" {stats.wins_stats['total']}")
        self.label_6.setText(self.label_6.text() + f" {stats.wins_stats['wins']}")
        self.label_7.setText(self.label_7.text() + f" {stats.wins_stats['loses']}")

        self.label_8.setText(self.label_8.text() + f" {stats.wins_stats['wins']/stats.wins_stats['total']}" \
                                    if stats.wins_stats['total'] != 0\
                                    else self.label_8.text() + " 0")

    @staticmethod
    def goto_menu():
        widgets.setCurrentIndex(0)

    def clear_statistics(self):
        self.label_2.setText("")
        self.label_4.setText("")

    def reset_statistics(self):
        stats.reset_stats()
        self.clear_statistics()
        self.draw_statistics()


class Menu(QtWidgets.QMainWindow):

    def __init__(self):
        super(Menu, self).__init__()
        uic.loadUi("resources/ui/menu.ui", self)
        self.pushButton.clicked.connect(self.goto_classic_mode)
        self.pushButton_2.clicked.connect(self.goto_pro_mode)
        self.pushButton_3.clicked.connect(self.goto_stats_mode)
        self.show()

    @staticmethod
    def goto_classic_mode():
        widgets.setCurrentIndex(1)

    @staticmethod
    def goto_pro_mode():
        widgets.setCurrentIndex(2)

    @staticmethod
    def goto_stats_mode():
        widgets.setCurrentIndex(3)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # Stats
    stats = Stats()

    #   All windows
    menu                = Menu()
    classic_mode_window = ClassicMode()
    pro_mode_window     = ProMode()
    stats_window        = Statistics()

    #   Stack Windows above
    widgets = QtWidgets.QStackedWidget()
    widgets.addWidget(menu)
    widgets.addWidget(classic_mode_window)
    widgets.addWidget(pro_mode_window)
    widgets.addWidget(stats_window)

    widgets.show()
    widgets.setFixedSize(660, 550)

    app.exec_()
    stats.__del__()
