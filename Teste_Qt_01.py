#from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel, QVBoxLayout
from PyQt5.QtWidgets import *

def clicar_botao():
    alert = QMessageBox()
    alert.setText('Bóson Treinamentos!')
    alert.exec()

if __name__=="__main__":
    app = QApplication([])
    app.setStyle('Fusion')
    janela = QWidget()
    janela.setWindowTitle('Teste de Qt para Bóson')
    #janela.setGeometry(300,100,350,150)
    janela.resize(400,400)
    layout = QVBoxLayout()
    layout.addWidget(QPushButton('Top'))
    layout.addWidget(QPushButton('Bottom'))
    #layout.addWidget(QLabel('Bóson Treinamentos!'))

    label = QLabel('Bóson Treinamentos!')
    layout.addWidget(label)

    # Botão que abre caixa de alerta:
    botao = QPushButton('Clique Aqui')
    layout.addWidget(botao)
    botao.clicked.connect(clicar_botao)
    botao.show()

    # ComboBox:
    frutas = ['Abacate','Morango','Melancia','Kiwi','Maçã','Caju']
    cmbFrutas = QComboBox()
    cmbFrutas.addItems(frutas)
    layout.addWidget(cmbFrutas)

    janela.setLayout(layout)
    janela.show()

    app.exec_()
