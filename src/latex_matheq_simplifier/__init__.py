"""LaTeX Math Equation Simplifier"""

import sys
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLabel, QFileDialog
)


def replace_equations(text: str, placeholder: str = '[EQUATION]') -> str:
    """Replace LaTeX math equations with a placeholder."""
    patterns = [
        r'\$(.+?)\$',
        r'\\begin\{equation\*?\}(.+?)\\end\{equation\*?\}',
        r'\\begin\{align\*?\}(.+?)\\end\{align\*?\}',
    ]
    for pattern in patterns:
        text = re.sub(pattern, placeholder, text, flags=re.DOTALL)
    return text


class LatexSimplifierGUI(QWidget):
    """A simple GUI for replacing LaTeX math equations with a placeholder."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("LaTeX Math Equation Simplifier")
        self.init_ui()

    def init_ui(self):
        """Initialize the UI components."""
        self.setWindowIconText("LaTeX Simplifier")
        self.setMinimumSize(800, 600)

        layout = QVBoxLayout()

        self.open_button = QPushButton("Open LaTeX File")
        self.open_button.clicked.connect(self.open_file)
        layout.addWidget(self.open_button)

        self.input_label = QLabel("Input LaTeX Text:")
        layout.addWidget(self.input_label)

        self.input_text = QTextEdit()
        layout.addWidget(self.input_text)

        # Horizontal layout for replacement text and button
        h_layout = QHBoxLayout()

        self.replacement_label = QLabel("Replacement Text:")
        self.replacement_label.setToolTip(
            "Text to replace the equations. Default is [EQUATION]."
        )
        self.replacement_label.setMaximumWidth(
            self.replacement_label.sizeHint().width()
        )
        h_layout.addWidget(self.replacement_label)

        self.replacement_textbox = QTextEdit()
        self.replacement_textbox.setPlainText("[EQUATION]")
        self.replacement_textbox.setMaximumWidth(
            self.replacement_label.sizeHint().width() * 2
        )
        h_layout.addWidget(self.replacement_textbox)

        self.process_button = QPushButton("Replace Equations")
        self.process_button.clicked.connect(self.process_text)
        self.replacement_textbox.setFixedHeight(
            self.process_button.sizeHint().height()
        )
        h_layout.addWidget(self.process_button)

        layout.addLayout(h_layout)

        self.output_label = QLabel("Output:")
        layout.addWidget(self.output_label)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        self.setLayout(layout)

    def process_text(self):
        """Process the input text and replace equations."""
        input_str = self.input_text.toPlainText()
        output_str = replace_equations(
            input_str, self.replacement_textbox.toPlainText()
        )
        self.output_text.setPlainText(output_str)

    def open_file(self):
        """Open a LaTeX file and load its content into the input text area."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open LaTeX File",
            "",
            "LaTeX Files (*.tex);;All Files (*)",
            options=options
        )
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.input_text.setPlainText(content)
            except OSError as e:
                self.input_text.setPlainText(f"Error opening file: {e}")


def main():
    """Main function to run the GUI."""
    app = QApplication(sys.argv)
    window = LatexSimplifierGUI()
    window.show()
    sys.exit(app.exec_())
