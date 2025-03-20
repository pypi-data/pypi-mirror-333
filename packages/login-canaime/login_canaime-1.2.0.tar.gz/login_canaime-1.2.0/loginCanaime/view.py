"""
Módulo view
-----------
Contém o código responsável pela interface gráfica (PySide6) do login,
integrando o design original e utilizando imagens carregadas de URLs para
o ícone da janela e o spinner de carregamento.
"""

import urllib.request

from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt, QSize, QBuffer, QByteArray)
from PySide6.QtGui import QIcon, QMovie, QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class CanaimeLoginView(QMainWindow):
    """
    Classe responsável pela criação e gerenciamento da interface de login utilizando PySide6.

    A interface integra o design original (layout, estilos e widgets) e inclui:
      - Campo de e-mail e senha (com asteriscos).
      - Botão de login e label de status.
      - Janela sem borda com ícone personalizado.
      - Exibição de um spinner animado (GIF) durante o login.
    """

    # URLs para as imagens (ícone e spinner)
    ICON_URL = "https://sejuc.rr.gov.br/wp-content/uploads/2023/10/Brasao-3-1024x1024.png"
    SPINNER_URL = "https://loading.io/assets/mod/spinner/eclipse/lg.gif"

    def __init__(self) -> None:
        """
        Inicializa a interface de login, configura a UI, baixa e aplica as imagens para o ícone e o spinner,
        e conecta os botões de controle da janela.
        """
        super().__init__()
        self._login_result = None
        self.setupUi()

        # Configura a janela: sem borda e com fundo translúcido
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Define o ícone da janela a partir da URL
        self.setWindowIcon(self._load_icon_from_url(self.ICON_URL))

        # Conecta os botões de controle da janela
        self.close_btn.clicked.connect(self.close)
        self.minimize_btn.clicked.connect(self.showMinimized)

        # Configura o campo de senha para exibir asteriscos
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Cria o spinner (QLabel com QMovie) para o carregamento
        self.spinner_label = QLabel(self)
        self.spinner_movie = self._load_movie_from_url(self.SPINNER_URL)
        self.spinner_label.setMovie(self.spinner_movie)
        self.spinner_label.setFixedSize(50, 50)
        self.spinner_label.hide()
        self._position_spinner()

    def _load_icon_from_url(self, url: str) -> QIcon:
        """
        Baixa uma imagem a partir de uma URL e retorna um QIcon.

        Args:
            url (str): URL da imagem.

        Returns:
            QIcon: Ícone carregado.
        """
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = response.read()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            return QIcon(pixmap)
        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")
            return QIcon()

    def _load_movie_from_url(self, url: str) -> QMovie:
        """
        Baixa um GIF animado a partir de uma URL e retorna um QMovie.

        Args:
            url (str): URL do GIF.

        Returns:
            QMovie: Objeto QMovie com o GIF carregado.
        """
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = response.read()
            byte_array = QByteArray(data)
            buffer = QBuffer(byte_array)
            buffer.open(QBuffer.ReadOnly)
            movie = QMovie()
            movie.setDevice(buffer)
            # Manter o buffer vivo enquanto o movie estiver em uso
            self._spinner_buffer = buffer
            return movie
        except Exception as e:
            print(f"Erro ao carregar spinner: {e}")
            return QMovie()

    def _position_spinner(self) -> None:
        """
        Posiciona o spinner no centro da janela.
        """
        spinner_x = (self.width() - self.spinner_label.width()) // 2
        spinner_y = (self.height() - self.spinner_label.height()) // 2
        self.spinner_label.move(spinner_x, spinner_y)

    def resizeEvent(self, event) -> None:
        """
        Reposiciona o spinner quando a janela é redimensionada.
        """
        super().resizeEvent(event)
        self._position_spinner()

    def setupUi(self) -> None:
        """
        Configura a interface de login (layout, estilos e widgets) conforme o design original.
        """
        self.setObjectName("Login")
        self.resize(450, 432)
        self.setMinimumSize(QSize(450, 400))
        self.setMaximumSize(QSize(450, 432))

        # Widget central e estilo
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet(
            "QWidget#centralwidget{\n"
            "	background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0.023, "
            "stop:0 rgba(255, 140, 140, 255), stop:1 rgba(94, 122, 255, 255));\n"
            "	border-radius: 20px;\n"
            "}\n"
            "\n"
            "QFrame#frame{\n"
            "	margin: 60px;\n"
            "	border-radius: 20px;\n"
            "	background-color: rgba(225, 228, 221, 120);\n"
            "}\n"
            "\n"
            "QLineEdit{\n"
            "	min-height: 45px;\n"
            "	border-radius: 20px;\n"
            "	background-color: #FFFFFF;\n"
            "	padding-left: 20px;\n"
            "	color: rgb(140, 140, 140);\n"
            "}\n"
            "\n"
            "QLineEdit:hover{\n"
            "	border: 2px solid rgb(139, 142, 139);\n"
            "}\n"
            "\n"
            "QPushButton#login_btn{\n"
            "	min-height: 45px;\n"
            "	border-radius: 20px;\n"
            "	background-color: rgb(140, 140, 140);\n"
            "	color: #FFFFFF;\n"
            "}\n"
            "\n"
            "QPushButton#login_btn:hover{\n"
            "	border: 2px solid rgb(255, 255, 255);\n"
            "}\n"
            "\n"
            "QLabel{\n"
            "	color: rgb(95, 94, 108);\n"
            "}\n"
            "\n"
            "QPushButton#close_btn{\n"
            "	background-color: rgb(186, 0, 0);\n"
            "	border-radius: 6px;\n"
            "}\n"
            "\n"
            "QPushButton#minimize_btn{\n"
            "	background-color: rgb(226, 226, 0);\n"
            "	border-radius: 6px;\n"
            "}"
        )

        # Layout principal
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # Top bar
        self.top_bar = QFrame(self.centralwidget)
        self.top_bar.setObjectName("top_bar")
        self.top_bar.setMinimumSize(QSize(0, 30))
        self.top_bar.setMaximumSize(QSize(16777215, 30))
        self.top_bar.setFrameShape(QFrame.NoFrame)
        self.top_bar.setFrameShadow(QFrame.Raised)

        self.horizontalLayout = QHBoxLayout(self.top_bar)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.frame_4 = QFrame(self.top_bar)
        self.frame_4.setObjectName("frame_4")
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout.addWidget(self.frame_4)

        self.frame_3 = QFrame(self.top_bar)
        self.frame_3.setObjectName("frame_3")
        self.frame_3.setMaximumSize(QSize(60, 16777215))
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_3 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setContentsMargins(0, 0, 5, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.minimize_btn = QPushButton(self.frame_3)
        self.minimize_btn.setObjectName("minimize_btn")
        self.minimize_btn.setMaximumSize(QSize(12, 12))
        self.horizontalLayout_3.addWidget(self.minimize_btn)

        self.close_btn = QPushButton(self.frame_3)
        self.close_btn.setObjectName("close_btn")
        self.close_btn.setMaximumSize(QSize(12, 12))
        self.horizontalLayout_3.addWidget(self.close_btn)

        self.horizontalLayout.addWidget(self.frame_3)
        self.verticalLayout_2.addWidget(self.top_bar)

        # Frame central
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName("frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)

        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setContentsMargins(30, 30, 30, 30)
        self.verticalLayout.setObjectName("verticalLayout")

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.label_2.setMaximumSize(QSize(16777215, 40))
        self.label_2.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label_2)

        self.email_input = QLineEdit(self.frame)
        self.email_input.setObjectName("email_input")
        self.verticalLayout.addWidget(self.email_input)

        self.password_input = QLineEdit(self.frame)
        self.password_input.setObjectName("password_input")
        self.verticalLayout.addWidget(self.password_input)

        self.login_btn = QPushButton(self.frame)
        self.login_btn.setObjectName("login_btn")
        self.verticalLayout.addWidget(self.login_btn)

        self.status_label = QLabel(self.frame)
        self.status_label.setObjectName("status_label")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.status_label)

        # Não adicionamos os widgets "remember" e "forgot password"

        self.verticalLayout_2.addWidget(self.frame)
        self.setCentralWidget(self.centralwidget)
        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self) -> None:
        self.setWindowTitle(QCoreApplication.translate("Login", "MainWindow", None))
        self.minimize_btn.setText("")
        self.close_btn.setText("")
        self.label_2.setText(
            QCoreApplication.translate(
                "Login",
                "<html><head/><body><p><span style=\" font-size:20pt;\">Sign In</span></p></body></html>",
                None,
            )
        )
        self.email_input.setPlaceholderText(QCoreApplication.translate("Login", "Email", None))
        self.password_input.setPlaceholderText(QCoreApplication.translate("Login", "Password", None))
        self.login_btn.setText(QCoreApplication.translate("Login", "Sign In", None))

    # Métodos auxiliares para o Controller

    def get_username(self) -> str:
        """Retorna o conteúdo do campo de e-mail."""
        return self.email_input.text()

    def get_password(self) -> str:
        """Retorna o conteúdo do campo de senha."""
        return self.password_input.text()

    def disable_login_button(self) -> None:
        """Desabilita o botão de login."""
        self.login_btn.setEnabled(False)

    def enable_login_button(self) -> None:
        """Habilita o botão de login."""
        self.login_btn.setEnabled(True)

    def set_status_message(self, message: str) -> None:
        """Atualiza a mensagem de status exibida."""
        self.status_label.setText(message)
        print(message)

    def start_loading_animation(self) -> None:
        """Exibe o spinner de carregamento e inicia sua animação."""
        self.spinner_label.show()
        if self.spinner_movie:
            self.spinner_movie.start()

    def stop_loading_animation(self) -> None:
        """Oculta o spinner de carregamento e para sua animação."""
        if self.spinner_movie:
            self.spinner_movie.stop()
        self.spinner_label.hide()

    def mousePressEvent(self, event):
        """Captura a posição inicial do mouse para iniciar o arrasto."""
        if event.button() == Qt.LeftButton:
            # Em Qt6, event.globalPosition() retorna um QPointF; convertemos para QPoint
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Move a janela conforme o mouse se arrasta."""
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

