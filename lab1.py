import sys
import re
from collections import Counter
import pymorphy2
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QWidget, QLabel


class TextAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Скриптовые языки. Задание 1. Куликов Д.Е.")
        self.setGeometry(100, 100, 800, 600)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Заголовки
        input_label = QLabel("Введите текст для анализа:")
        output_label = QLabel("Результат анализа (слово - количество):")

        # Текстовые поля
        self.input_text_edit = QTextEdit()
        self.output_text_edit = QTextEdit()
        self.output_text_edit.setReadOnly(True)  # Только читать

        # Кнопка
        self.analyze_button = QPushButton("Анализировать")
        self.analyze_button.clicked.connect(self.analyze_text)

        # Компоновка
        main_layout.addWidget(input_label)
        main_layout.addWidget(self.input_text_edit)
        main_layout.addWidget(output_label)
        main_layout.addWidget(self.output_text_edit)
        main_layout.addWidget(self.analyze_button)

        # Запуск морф анализатора
        self.morph = pymorphy2.MorphAnalyzer()

    def get_normal_form(self, word):
        # Возврат нормальной формы слова
        parsed = self.morph.parse(word)[0]
        return parsed.normal_form

    def analyze_text(self):
        # Анализ текста и вывод результата
        input_text = self.input_text_edit.toPlainText()
        if not input_text.strip():
            self.output_text_edit.setPlainText("Текст пустой.")
            return

        # Извлечение слов
        words = re.findall(r'[а-яёa-z]+', input_text.lower()) # Находит последовательности кирилицы и латиницы

        if not words:
            self.output_text_edit.setPlainText("Слова в тексте не найдены.")
            return

        # Нормализация всех слов
        normalized_words = [self.get_normal_form(word) for word in words]

        # Подсчёт слов
        word_counts = Counter(normalized_words)

        # Сортировка частовстречающихся слов
        sorted_by_frequency = word_counts.most_common() # most_common() возвращает слово - количество

        # Формирование результата
        result_lines = []
        for word, count in sorted_by_frequency:
            result_lines.append(f"{word} - {count}")

        # Вывод результата в поле вывода
        self.output_text_edit.setPlainText("\n".join(result_lines))


def main():
    app = QApplication(sys.argv)
    window = TextAnalyzerApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()