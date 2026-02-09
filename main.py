import sys
import math
import random

from enum import Enum

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QStackedWidget, QGraphicsView, QPinchGesture,
    QGraphicsScene, QGraphicsOpacityEffect, QFrame, QGraphicsItem, QGraphicsTextItem, QAbstractScrollArea, QGestureEvent, QPanGesture
)
from PySide6.QtCore import Qt, QPropertyAnimation, QRectF, QTimer, QEvent
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
    "41, o número mais malvado de todos...",
    "Tão incrível quanto macacos árticos...",
    "A épica nunca pediria sua senha...",
    "Eu... te... vi... Lá no canto da sala...",
    "UwU",

    "As coisa cai...",
    "Só sabo que nada sebo...",
    "Penso. Logo desisto...",
    "O homem nasce bom. As assinaturas o corrompem...",

    "nada 👍",
    "Só inicia logo o app 😒",
    "Não se envergonhe, é só clicar aqui 👇",

    "Robux grátis >aqui<",
    "Não se esqueça de alimentar o seu Pou..."
    "Eu sempre volto..."


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
    def __init__(self, x, y):
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
        self.setSceneRect(-3000, -3000, 4000, 2000)

    def create_card(self, pos):
        card = CanvasCard(pos.x(), pos.y())
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

class FloatingButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

        self.setFixedSize(42, 42)
        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet("""
            QPushButton {
                background-color: #2f2f2f;
                color: #ddd;
                border-radius: 10px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #3a3a3a;
            }
            QPushButton:pressed {
                background-color: #444;
            }
        """)

class CanvasView(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = CanvasScene()
        self.setScene(self.scene)

        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        #add ui

        #ativar e desativar barras
        #self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 🔹 botões flutuantes
        self.tools_btn = FloatingButton("🧰", self)
        self.settings_btn = FloatingButton("⚙️", self)

        self.tools_btn.clicked.connect(self.on_tools_clicked)
        self.settings_btn.clicked.connect(self.on_settings_clicked)

        #zoom trackpad
        self.grabGesture(Qt.PinchGesture)
       
        #pan
        self._panning = False
        self._pan_start = None

        #pan trackpad
        self.grabGesture(Qt.PanGesture)

        self.zoom_factor = 1.0
        self.zoom_min = 0.5
        self.zoom_max = 3.14

        # 🔹 indicador de zoom
        self.zoom_label = QLabel("100%", self)
        self.zoom_label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 40);
                color: white;
                padding: 4px 8px;
                border-radius: 6px;
                font-size: 12px;
            }
        """)

        self.zoom_label.setAlignment(Qt.AlignCenter)
        self.zoom_label.adjustSize()
        self.zoom_label.hide()

        # efeito de opacidade
        self.zoom_effect = QGraphicsOpacityEffect(self.zoom_label)
        self.zoom_label.setGraphicsEffect(self.zoom_effect)
        self.zoom_effect.setOpacity(1.0)

        # timer para esconder
        self.zoom_hide_timer = QTimer(self)
        self.zoom_hide_timer.setSingleShot(True)
        self.zoom_hide_timer.timeout.connect(self._fade_out_zoom_label)

        self.zoom_label.move(12, 12)
        self.zoom_label.show()

    def event(self, event):
        if event.type() == QEvent.Gesture:
            return self.gestureEvent(event)
        return super().event(event)

    def gestureEvent(self, event):
        pan = event.gesture(Qt.PanGesture)
        if pan:
            delta = pan.delta()

            hbar = self.horizontalScrollBar()
            vbar = self.verticalScrollBar()

            hbar.setValue(hbar.value() - int(delta.x()))
            vbar.setValue(vbar.value() - int(delta.y()))

        pinch = event.gesture(Qt.PinchGesture)

        if pinch:
           self.handle_pinch(pinch)

        return True

    def handle_pinch(self, pinch: QPinchGesture):
        if pinch.state() == Qt.GestureStarted:
            self._pinch_start_zoom = self._zoom
            return

        scale = pinch.scaleFactor()

        zoom_step = 1.08
        zoom_delta = math.log(scale, zoom_step)

        new_zoom = self._zoom + zoom_delta

        MIN_ZOOM = -15
        MAX_ZOOM = 40

        if MIN_ZOOM <= new_zoom <= MAX_ZOOM:
            self.scale(scale, scale)
            self._zoom = new_zoom
            self.update_zoom_label()

    def _position_zoom_label(self):
        margin_bottom = 20  # espaço acima da barra
        x = (self.width() - self.zoom_label.width()) // 2
        y = self.height() - self.zoom_label.height() - margin_bottom
        self.zoom_label.move(x, y)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # 🔹 reposiciona label de zoom
        self._position_zoom_label()

        # 🔹 reposiciona botões flutuantes
        margin = 32
        y = self.height() - self.tools_btn.height() - margin

        self.tools_btn.move(margin, y)
        self.settings_btn.move(
            self.width() - self.settings_btn.width() - margin,
            y
    )

    def on_tools_clicked(self):
        print("Ferramentas clicado")

    def on_settings_clicked(self):
        print("Configurações clicado")

    def _fade_out_zoom_label(self):
        anim = QPropertyAnimation(self.zoom_effect, b"opacity", self)
        anim.setDuration(300)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)

        def hide():
            self.zoom_label.hide()

        anim.finished.connect(hide)
        anim.start()

        self._zoom_fade_anim = anim  # evita GC

    def wheelEvent(self, event):
        zoom_step = 1.12  # mais suave

        if event.angleDelta().y() > 0:
            new_zoom = self.zoom_factor * zoom_step
        else:
            new_zoom = self.zoom_factor / zoom_step

        if self.zoom_min <= new_zoom <= self.zoom_max:
            factor = new_zoom / self.zoom_factor
            self.zoom_factor = new_zoom
            self.scale(factor, factor)

            percent = int(self.zoom_factor * 100)
            self.zoom_label.setText(f"{percent}%")
            self.zoom_label.adjustSize()
            self._position_zoom_label()

            # mostrar label
            self.zoom_hide_timer.stop()
            self.zoom_label.show()
            self.zoom_effect.setOpacity(1.0)

            # esconder após 1s
            self.zoom_hide_timer.start(1000)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = self.mapToScene(event.position().toPoint())
            self.scene.create_card(pos)
            event.accept()
        else:
            super().mouseDoubleClickEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self._panning = True
            self._pan_start = event.position()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._panning and self._pan_start is not None:
            delta = event.position() - self._pan_start
            self._pan_start = event.position()

            hbar = self.horizontalScrollBar()
            vbar = self.verticalScrollBar()

            hbar.setValue(hbar.value() - int(delta.x()))
            vbar.setValue(vbar.value() - int(delta.y()))

            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self._panning = False
            self.setCursor(Qt.ArrowCursor)
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

        # 🔹 adiciona ao layout (ORDEM IMPORTA)
        self.container_layout.addWidget(self.stack, 1)

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