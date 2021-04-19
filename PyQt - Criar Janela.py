import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QMessageBox, QLabel
import pymysql

def conectaBanco():
    global con
    con = pymysql.connect(host='localhost', user='root', database='db_MeusLivros', cursorclass=pymysql.cursors.DictCursor, password='abc123**')

class Janela(QMainWindow):
    '''Classe para criar janela principal de aplicação'''
    def __init__(self):
        super().__init__()

        # Dimensões, posicionamento e título da janela:
        self.top = 100
        self.esq = 100
        self.lar = 600
        self.alt = 200
        self.titulo = 'Criar Janela em PyQt'

        # Criar um botão
        self.botao = QPushButton('Clique aqui', self)
        self.botao.setStyleSheet('QPushButton {background-color:#0000EE;color:red;font:bold}')
        self.botao.move(100, 50) # Dist_hor, dist_vert
        self.botao.clicked.connect(self.clicar_botao)

        # Criar outro botão
        self.btnNome = QPushButton('Escrever Nome', self)
        self.btnNome.setStyleSheet('QPushButton {background-color:#0000EE;color:red;font:bold}')
        self.btnNome.move(200, 50)
        self.btnNome.clicked.connect(self.escrever_nome)

        # Criar Caixa de texto:
        self.txtNome = QLineEdit(self)
        self.txtNome.move(100, 100)
        self.txtNome.resize(150, 30) # largura, altura

        # Criar Label
        self.lblNome = QLabel(self)
        self.lblNome.move(100, 150)
        self.lblNome.resize(250, 30)
        self.lblNome.setStyleSheet('font:bold;color:green;font-size:20px')

        # Último método a ser executado: carregar a janela
        self.CarregaJanela()

    def CarregaJanela(self):
        self.setGeometry(self.esq,self.top,self.lar,self.alt)
        self.setWindowTitle(self.titulo)
        # Cor de fundo da janela, com folha de estilos:
        self.setStyleSheet('QMainWindow {background-color:#0000EE;}')
        self.show()

    def clicar_botao(self):
        alert = QMessageBox()
        alert.setWindowTitle('Bem-vindos!')
        alert.setText('Bóson Treinamentos!')
        alert.exec()

    def escrever_nome(self):
        self.txtNome.setText('Fábio dos Reis')
        self.lblNome.setText('Bóson Treinamentos')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    tela = Janela()
    print(tela.titulo)
    sys.exit(app.exec_())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
