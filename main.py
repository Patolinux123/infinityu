import sys
import random

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QLabel, QPushButton,
    QStackedWidget, QGraphicsView,
    QGraphicsScene, QGraphicsOpacityEffect, QFrame
)
from PySide6.QtCore import Qt, QPropertyAnimation
from PySide6.QtGui import QFont, QPainter, QIcon, QFontDatabase

# =========================
# WELCOME SCREEN
# =========================
class WelcomeScreen(QWidget):
    def __init__(self, on_create_project, parent=None):
        super().__init__(parent)

        self.on_create_project = on_create_project

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        root.addStretch()

        container = QVBoxLayout()
        container.setAlignment(Qt.AlignCenter)
        container.setSpacing(16)

        title = QLabel("infinityu")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))

        phrases = [
    #O principal
    "Infinidade. Para ir além...",
    "Não vai te deixar no vácuo...",
    #Chat
    "Organize o caos. Ou abrace ele...",
    "Tentando achar a borda do app...",
    #maneiro
    "Cérebro 2",
    "Carregando o infinito...",
    #uff referencias
    "Que o armazenamento esteja com você...",
    "Poder ILIMITADO p%#☠︎︎@...",
    "Com grandes espaços, vem grandes responsabilidades...",
    "Por que está tão sério?",
    "SOU AMENDOBOBO! YEAH!",
    "GRIFFITH!",
    "Também experimente Minecraft!",
    "Alguém lê isso mesmo?",
    "41, o número mais malvado de todos..."
]
        subtitle = QLabel(random.choice(phrases))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px;""color: #888;")

        btn = QPushButton("Começar")
        btn.setFixedSize(150, 44)
        btn.setCursor(Qt.PointingHandCursor)

        btn.setStyleSheet("""
            QPushButton {
                background-color: #5b7cfa;
                color: white;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #6d8cff;
            }
        """)

        btn.clicked.connect(self.on_create_project)

        container.addWidget(title)
        container.addWidget(subtitle)
        container.addWidget(btn, alignment=Qt.AlignCenter)

        root.addLayout(container)
        root.addStretch()


# =========================
# CANVAS
# =========================
class CanvasView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        # view transparente
        self.setBackgroundBrush(Qt.transparent)
        self.setStyleSheet("background: transparent;")
        self.setFrameShape(QFrame.NoFrame)

        # Scene
        self._scene = QGraphicsScene(self)
        self._scene.setBackgroundBrush(Qt.transparent)
        self._scene.setSceneRect(-1000, -1000, 2000, 2000)

        self.setScene(self._scene)

        # Render
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

# =========================
# MAIN WINDOW
# =========================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Infinityu")
        self.setWindowIcon(QIcon("iconblack.ico"))
        self.resize(900, 600)

        # 🔹 container para o fade
        self.container = QWidget()
        self.container.setStyleSheet("""
    QWidget {
        background-color: #292929;
    }
""")
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)

        self.stack = QStackedWidget()
        self.container_layout.addWidget(self.stack)

        self.setCentralWidget(self.container)

        # Telas
        self.canvas = CanvasView()
        self.welcome = WelcomeScreen(self.open_canvas)

        self.stack.addWidget(self.welcome)
        self.stack.addWidget(self.canvas)

        self.stack.setCurrentWidget(self.welcome)

    # =========================
    # FADE TRANSITION
    # =========================

    def open_canvas(self):
         effect = QGraphicsOpacityEffect(self.container)
         self.container.setGraphicsEffect(effect)

         effect.setOpacity(1.0)

         fade_out = QPropertyAnimation(effect, b"opacity")
         fade_out.setDuration(250)
         fade_out.setStartValue(1.0)
         fade_out.setEndValue(0.0)

         def on_fade_out_finished():
        # troca a tela
             self.stack.setCurrentWidget(self.canvas)

             fade_in = QPropertyAnimation(effect, b"opacity")
             fade_in.setDuration(250)
             fade_in.setStartValue(0.0)
             fade_in.setEndValue(1.0)

             def cleanup():
            # remover o efeito
                 self.container.setGraphicsEffect(None)

                # força repaint completo
                 self.container.update()
                 self.canvas.viewport().update()

             fade_in.finished.connect(cleanup)
             fade_in.start()
             self.fade_in = fade_in

         fade_out.finished.connect(on_fade_out_finished)
         fade_out.start()
         self.fade_out = fade_out

# =========================
# APP
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    #QFontDatabase.addApplicationFont()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())