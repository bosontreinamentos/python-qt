import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap


class Janela(QMainWindow):
    ''' Classe para criar janela principal com seus widgets'''
    def __init__(self):  # Método construtor
        super().__init__()

        self.topo = 100
        self.alt = 300
        self.lar = 600
        self.esq = 100
        self.titulo = 'Controles variados - I'

        # Criar um botão
        self.botao = QPushButton('Clique aqui', self)
        self.botao.move(150, 50)
        self.botao.setToolTip('Clique para calcular a área do terreno.')
        self.botao.clicked.connect(self.calculaArea)

        # Criar um label
        self.lblNome = QLabel(self)
        self.lblNome.move(150, 200)
        self.lblNome.resize(300, 30)
        self.lblNome.setStyleSheet('font:bold;color:green;font-size:25px')

        # Criar uma caixa de texto para largura do terreno
        self.lblLargura = QLabel(self)
        self.lblLargura.setText('Digite a largura na caixa abaixo:')
        self.lblLargura.move(300,25)
        self.lblLargura.resize(300,20)
        self.txtLargura = QLineEdit(self)
        #self.txtLargura.setEchoMode(QLineEdit.Password) # Modo de exibição para senhas
        self.txtLargura.move(300, 50)

        # Criar uma caixa de texto para profundidade do terreno
        self.lblProfundidade = QLabel(self)
        self.lblProfundidade.setText('Digite a profundidade na caixa abaixo:')
        self.lblProfundidade.move(300,85)
        self.lblProfundidade.resize(300,20)
        self.txtProfundidade = QLineEdit(self)
        self.txtProfundidade.move(300, 110)
        # Pressionando Enter, esta caixa executa a função de cálculo:
        self.txtProfundidade.returnPressed.connect(self.calculaArea)

        # Dial para largura
        self.dial = QDial(self)
        self.dial.setMinimum(5)
        self.dial.setMaximum(20)
        #self.dial.move(380,50)
        self.dial.setGeometry(400,45,40,40)
        self.dial.valueChanged.connect(self.ajustaLargura)

        # Caixa de imagem
        logotipo = QPixmap('logo.png')
        self.lblImagem = QLabel(self)
        self.lblImagem.resize(100,100)
        self.lblImagem.setPixmap(logotipo)
        self.lblImagem.move(10,10)

        # Menu
        self.menu = QMenuBar(self)
        self.menuArquivo = self.menu.addMenu('Arquivo')
        self.sair = QAction('Sair',self)
        self.menuArquivo.addAction(self.sair)
        self.sair.triggered.connect(self.fechaApp)
        self.menuAjuda = self.menu.addMenu('Ajuda')
        self.menu.show()

        # Carregar a janela
        self.carregaJanela()

    # ----- Métodos da Classe ----- #

    def calculaArea(self):
        l = self.txtLargura.text()
        p = self.txtProfundidade.text()
        a = int(l) * int(p)
        res = 'Área calculada: ' + str(a) + ' m\u00b2'
        self.lblNome.setText(res)

    def ajustaLargura(self):
        valor = str(self.dial.value())
        self.txtLargura.setText(valor)

    def carregaJanela(self):
        self.setGeometry(self.esq, self.topo, self.lar, self.alt)
        self.setWindowTitle(self.titulo)
        self.setStyleSheet('background-color:lightblue')
        self.show()

    def clicarBotao(self):
        caixa = QMessageBox()
        a = self.txtLargura.text()
        caixa.setWindowTitle('Bem-vindos!')
        caixa.setText(a)
        caixa.exec()

    def fechaApp(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    tela = Janela()

    sys.exit(app.exec_())


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
