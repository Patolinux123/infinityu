import sys
import math
import random

from enum import Enum

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QStackedWidget, QGraphicsView,
    QGraphicsScene, QGraphicsOpacityEffect, QFrame, QGraphicsItem, QGraphicsTextItem
)
from PySide6.QtCore import Qt, QPropertyAnimation, QRectF
from PySide6.QtGui import QFont, QPainter, QIcon, QFontDatabase, QColor

# =========================
# some stuff
# =========================

PLACEHOLDER_TEXTS = [
    "Escreva uma ideia aqui…",
    "O que você está pensando?",
    "Comece digitando…",
    "Planeje algo incrível…",
    "Escreva maravilhas…",
    "Suas notinhas..."
]

class CardType(Enum):
    TEXT = 1
    TITLE = 2
    CHECKLIST = 3

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
    
    "Infinidade. Para ir além...",
    "Não vai te deixar no vácuo...",
    
    "Organize o caos. Ou abrace ele...",
    "Tentando achar a borda do app...",
    
    "Cérebro 2",
    "Carregando o infinito...",
    
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
class CanvasCard(QGraphicsItem):
    def __init__(self, x, y, card_type):
        super().__init__()

        self.rect = QRectF(0, 0, 220, 140)
        self.setPos(x, y)

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        self.text_item = QGraphicsTextItem(self)
        self.text_item.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.text_item.setDefaultTextColor(QColor("#FFF"))
        self.text_item.setTextWidth(self.rect.width() - 20)
        self.text_item.setPos(10, 10)

        self.text_item.focusInEvent = self._on_focus_in
        self.text_item.focusOutEvent = self._on_focus_out

        self.card_type = card_type

        self.placeholder_text = random.choice(PLACEHOLDER_TEXTS)
        self.is_placeholder = True

        self._apply_placeholder()

        font = QFont("Segoe UI", 10)
        self.text_item.setFont(font)

    def _on_focus_in(self, event):
        if self.is_placeholder:
             self.text_item.setPlainText("")
             self.text_item.setDefaultTextColor(QColor(230, 230, 230))
             self.is_placeholder = False

    def _on_focus_out(self, event):
        if not self.text_item.toPlainText().strip():
             self.is_placeholder = True
             self._apply_placeholder()

    def _apply_placeholder(self):
        self.text_item.setPlainText(self.placeholder_text)
        self.text_item.setDefaultTextColor(QColor(150, 150, 150))

    def boundingRect(self):
        return self.rect.adjusted(-6, -6, 6, 6)
    
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            
                grid = 15
                x = round(value.x() / grid) * grid
                y = round(value.y() / grid) * grid
                return value.__class__(x, y)
        
        return super().itemChange(change, value)

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)

        # card
        painter.setBrush(QColor("#333333"))
        painter.setPen(QColor("#333333"))
        painter.drawRoundedRect(self.rect, 12, 12)

class CanvasScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.setSceneRect(-5000, -5000, 10000, 10000)

    def create_card(self, pos, card_type):
        card = CanvasCard(pos.x(), pos.y(), card_type)
        self.addItem(card)

    def drawBackground(self, painter, rect):
         super().drawBackground(painter, rect)

         grid = 15
         radius = 1.2

         painter.setPen(Qt.NoPen)
         painter.setBrush(QColor(141, 141, 141, 41))  # que número malvado

         left = int(rect.left()) - (int(rect.left()) % grid)
         top = int(rect.top()) - (int(rect.top()) % grid)

         for x in range(left, int(rect.right()), grid):
             for y in range(top, int(rect.bottom()), grid):
                 painter.drawEllipse(x - radius, y - radius, radius * 2, radius * 2)


class CanvasView(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = CanvasScene()
        self.setScene(self.scene)

        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setDragMode(QGraphicsView.RubberBandDrag)

        self.current_card_type = CardType.TEXT

        self._zoom = 0

    def wheelEvent(self, event):
        zoom_factor = 1.08  # antes era 1.15 (muito agressivo)

        if event.angleDelta().y() > 0:
             factor = zoom_factor
             self._zoom += 1
        else:
             factor = 1 / zoom_factor
             self._zoom -= 1

        if -15 < self._zoom < 40:
             self.scale(factor, factor)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = self.mapToScene(event.position().toPoint())
            self.scene.create_card(pos, self.current_card_type)
            event.accept()
        else:
            super().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event):
         if event.button() == Qt.MiddleButton:
             self.setDragMode(QGraphicsView.NoDrag)
             self._pan_start = event.position()
             event.accept()
         else:
             super().mousePressEvent(event)

def mouseMoveEvent(self, event):
    if event.buttons() & Qt.MiddleButton:
        delta = self.mapToScene(self._pan_start.toPoint()) - self.mapToScene(event.position().toPoint())
        self._pan_start = event.position()
        self.translate(delta.x(), delta.y())
        event.accept()
    else:
        super().mouseMoveEvent(event)

def mouseReleaseEvent(self, event):
    if event.button() == Qt.MiddleButton:
        event.accept()
    else:
        super().mouseReleaseEvent(event)

# =========================
# MAIN WINDOW
# =========================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("infinityu")
        self.setWindowIcon(QIcon("iconwhite.ico"))
        self.resize(1280, 720)

        # 🔹 container para o fade
        self.container = QWidget()
        self.container.setStyleSheet("""
            QWidget {
                background-color: #202020;
            }
        """)

        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(0)

        # 🔹 stack (telas)
        self.stack = QStackedWidget()

        # 🔹 telas
        self.canvas = CanvasView()
        self.welcome = WelcomeScreen(self.open_canvas)

        self.stack.addWidget(self.welcome)
        self.stack.addWidget(self.canvas)
        self.stack.setCurrentWidget(self.welcome)

        # 🔹 bottom bar (CRIA AQUI)
        self.bottom_bar = BottomBar(self.canvas)
        self.bottom_bar.hide()  # começa escondida

        # 🔹 adiciona ao layout (ORDEM IMPORTA)
        self.container_layout.addWidget(self.stack, 1)
        self.container_layout.addWidget(self.bottom_bar, 0)

        self.setCentralWidget(self.container)

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
             self.bottom_bar.show()

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
# THE BAR
# =========================

class BottomBar(QWidget):
    def __init__(self, canvas: CanvasView):
        super().__init__()
        self.canvas = canvas

        self.setFixedHeight(64)
        self.setStyleSheet("""
            QWidget {
                background-color: #262626;
                border-top: 1px solid #333;
            }
            QPushButton {
                background-color: #333;
                color: #ddd;
                border-radius: 8px;
                padding: 8px 14px;
            }
            QPushButton:hover {
                background-color: #444;
            }
            QPushButton:checked {
                background-color: #5b7cfa;
                color: white;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(10)

        self.btn_text = QPushButton("Texto")
        self.btn_title = QPushButton("Título")
        self.btn_check = QPushButton("Checklist")

        for btn in (self.btn_text, self.btn_title, self.btn_check):
            btn.setCheckable(True)
            layout.addWidget(btn)

        self.btn_text.setChecked(True)

        self.btn_text.clicked.connect(lambda: self.set_type(CardType.TEXT))
        self.btn_title.clicked.connect(lambda: self.set_type(CardType.TITLE))
        self.btn_check.clicked.connect(lambda: self.set_type(CardType.CHECKLIST))

    def set_type(self, card_type):
        self.canvas.current_card_type = card_type

        # garante apenas um ativo
        for btn in (self.btn_text, self.btn_title, self.btn_check):
            btn.setChecked(False)

        if card_type == CardType.TEXT:
            self.btn_text.setChecked(True)
        elif card_type == CardType.TITLE:
            self.btn_title.setChecked(True)
        elif card_type == CardType.CHECKLIST:
            self.btn_check.setChecked(True)

# =========================
# APP
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    #QFontDatabase.addApplicationFont()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())