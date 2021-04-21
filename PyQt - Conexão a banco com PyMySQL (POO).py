from PyQt5.QtWidgets import *
import pymysql
import sys

def conectaBanco():
    global con
    con = pymysql.connect(host='localhost',user='root',database='db_MeusLivros',cursorclass=pymysql.cursors.DictCursor,password='abc123**')

def msgProblemaBD():
    msgProblema = QMessageBox()
    msgProblema.setWindowTitle('Problema')
    msgProblema.setText('Problema ao obter os dados. Tente novamente.')
    msgProblema.exec()

def msgSucesso():
    msgSucesso = QMessageBox()
    msgSucesso.setWindowTitle('Sucesso!')
    msgSucesso.setText('Registro inserido com sucesso!')
    msgSucesso.exec()

class Janela(QMainWindow):
    ''' Classe principal '''
    def __init__(self): # método construtor da classe
        super().__init__()

        self.topo = 200
        self.esq = 200
        self.alt = 500
        self.lar = 800
        self.titulo = 'Acesso a banco de dados - I'

        # Criar botão para consulta de editora
        self.btnConsulta = QPushButton('Consultar Livro', self)
        self.btnConsulta.move(150, 50)
        self.btnConsulta.setStyleSheet('background-color:#0000EE;color:red;font:bold')
        self.btnConsulta.setToolTip('Clique aqui para consultar o livro')
        self.btnConsulta.clicked.connect(self.consultaLivro)

        # Caixas de texto para consulta de livro:
        self.lblLivro = QLabel(self)
        self.lblLivro.move(200,80)
        self.lblLivro.resize(250,30)
        self.lblLivro.setText('Digite o código do livro a pesquisar:')
        self.txtIdLivro = QLineEdit(self)
        self.txtNomeLivro = QLineEdit(self)
        self.txtIdLivro.move(200,105)
        self.txtIdLivro.resize(250,30)
        self.txtNomeLivro.move(200,150)
        self.txtNomeLivro.resize(250,30)

        # Combobox para exibir resultado da consulta de editoras
        self.lblEditora = QLabel(self)
        self.lblEditora.move(500, 50)
        self.lblEditora.resize(350, 20)
        self.lblEditora.setText('Editoras:')
        self.cmbEditoras = QComboBox(self)
        self.cmbEditoras.move(500,75)
        self.consultaEditoras()
        self.cmbEditoras.addItems(self.listaEditoras)
        self.cmbEditoras.activated.connect(self.informaEditora)

        # Caixa de texto para mostrar item selecionado no ComboBox
        self.txtEditora = QLineEdit(self)
        self.txtEditora.move(500,110)
        self.txtEditora.resize(200,20)    

        # Caixa de Listagem
        self.listaEd = QListWidget(self)
        self.listaEd.addItems(self.listaEditoras)
        self.listaEd.move(300,250)
        self.listaEd.resize(150,100)
        self.listaEd.addItem('Bóson Books')
        self.listaEd.sortItems() # Ordenar itens da lista
        self.listaEd.clicked.connect(self.informaEditoraLista)        

        # Botão para limpar a lista
        self.btnLimpaLista = QPushButton(self)
        self.btnLimpaLista.setText('Limpar Lista')
        self.btnLimpaLista.move(150,250)
        self.btnLimpaLista.clicked.connect(self.listaEd.clear)

        # Barra de menus
        self.menu = QMenuBar(self)
        self.menuArquivo = self.menu.addMenu('Arquivo')
        self.menuDados = self.menu.addMenu('Dados')
        self.menuAjuda = self.menu.addMenu('Ajuda')
        # Cadastrar autor
        self.cadastraAutor = QAction('Cadastrar Autor', self)
        self.menuDados.addAction(self.cadastraAutor)
        self.cadastraAutor.triggered.connect(self.abreJanelaAutor)
        # Cadastrar editora
        self.cadastraEditora = QAction('Cadastrar Editora', self)
        self.menuDados.addAction(self.cadastraEditora)
        self.cadastraEditora.triggered.connect(self.abreJanelaEditora)
        # Sair
        self.sair = QAction('Sair', self)
        self.menuArquivo.addAction(self.sair)
        self.sair.triggered.connect(self.fechaApp)
        self.menu.show()

        self.carregaJanela()

        
################# Métodos ##################

    def consultaEditoras(self):
        # Preparar um cursor com o método .cursor()
        try:
            conectaBanco()
            with con.cursor() as c:
                # Criar a consulta e executá-la no banco
                sql = "SELECT NomeEditora FROM tbl_editoras"
                c.execute(sql)
                res = c.fetchall()
                # Criar lista com os dados retornados
                self.listaEditoras = []
                for linha in res:
                    self.listaEditoras.append(linha['NomeEditora'])
        except Exception:
            msgProblemaBD()
        finally:           
            # Desconectar do servidor
            con.close()

    def consultaLivro(self):
        try:
            conectaBanco()
            IdLivro = self.txtIdLivro.text()
            with con.cursor() as c:
                sql = "SELECT NomeLivro FROM tbl_livros WHERE IdLivro = " + IdLivro + ";"
                c.execute(sql)
                res = c.fetchone()
                self.txtNomeLivro.setText(res['NomeLivro'])
        except Exception:
            msgProblemaBD()
        finally:
            con.close()

    def informaEditora(self):
        self.txtEditora.setText(self.cmbEditoras.currentText())

    def informaEditoraLista(self):
            self.editora = self.listaEd.currentItem()
            self.txtEditora.setText(self.editora.text())

    def abreJanelaAutor(self):
        self.janelaAutor = JanelaAutor(self)
        self.janelaAutor.show()

    def abreJanelaEditora(self):
        self.janelaEditora = JanelaEditora(self)
        self.janelaEditora.show()

    def fechaApp(self):
        self.close()

    def carregaJanela(self):
        self.setGeometry(self.esq, self.topo, self.lar, self.alt)
        self.setWindowTitle(self.titulo)
        self.setStyleSheet('background-color:lightgreen')
        self.show()

#------------ Janela de Autores ------------#

class JanelaAutor(QMainWindow):
    def __init__(self, parent=None):
        super(JanelaAutor, self).__init__(parent)

        self.topo = 300
        self.esq = 300
        self.alt = 700
        self.lar = 500
        self.titulo = 'Cadastrar Autores'

        # Criar botão para cadastro de autores
        self.btnCadastraAutor = QPushButton('Cadastrar Autor', self)
        self.btnCadastraAutor.move(100, 220)
        self.btnCadastraAutor.setStyleSheet('background-color:#0000CC;color:yellow;font:bold')
        self.btnCadastraAutor.setToolTip('Clique aqui para cadastrar um novo autor')
        self.btnCadastraAutor.clicked.connect(self.cadastraAutor)
        self.btnCadastraAutor.clicked.connect(self.carregaAutores)

        # Caixas de texto para cadastro de autor:
        self.lblNomeAutor = QLabel(self)
        self.lblNomeAutor.move(100,80)
        self.lblNomeAutor.resize(250,30)
        self.lblNomeAutor.setText('Nome do autor:')
        self.txtNomeAutor = QLineEdit(self)   
        self.txtNomeAutor.move(100,110)
        self.txtNomeAutor.resize(200,30)
        self.lblSobrenomeAutor = QLabel(self)
        self.lblSobrenomeAutor.move(100,150)
        self.lblSobrenomeAutor.resize(250,30)
        self.lblSobrenomeAutor.setText('Sobrenome do autor:')
        self.txtSobrenomeAutor = QLineEdit(self)
        self.txtSobrenomeAutor.move(100,180)
        self.txtSobrenomeAutor.resize(250,30)

        # Tabela de Autores
        self.tabelaAutores = QTableWidget(self)
        self.tabelaAutores.move(100,300)
        self.tabelaAutores.resize(250,300)
        

        self.configuraJanela()

    def configuraJanela(self):
        self.setGeometry(self.esq, self.topo, self.lar, self.alt)
        self.setWindowTitle(self.titulo)
        self.setStyleSheet('background-color:lightblue')
        self.carregaAutores()

    def cadastraAutor(self):
        try:
            conectaBanco()
            self.nomeAutor = self.txtNomeAutor.text()
            self.sobrenomeAutor = self.txtSobrenomeAutor.text()
            with con.cursor() as cur:           
                sql = "INSERT INTO tbl_autores (NomeAutor, SobrenomeAutor) VALUES " + "('" + self.nomeAutor + "','" + self.sobrenomeAutor + "');"
                cur.execute(sql)
                con.commit()
                cur.close()
        except Exception:
            msgProblemaBD()
        else:
            msgSucesso()
        finally:
            con.close()

    def carregaAutores(self):
        try:
            conectaBanco()
            with con.cursor() as c:
                sql = 'SELECT * FROM tbl_autores;'
                c.execute(sql)
                self.resAutores = c.fetchall()
        except Exception:
            msgProblemaBD()
        else:
            self.linhas = len(self.resAutores)
            self.colunas = len(self.resAutores[0])
            self.tabelaAutores.setRowCount(self.linhas)
            self.tabelaAutores.setColumnCount(self.colunas)
            
            # Ajustar cabeçalho e dimensões da tabela
            self.tabelaAutores.setHorizontalHeaderLabels((list(self.resAutores[0].keys())))
            self.tabelaAutores.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            
            for l in range(self.linhas):
              for c in range(self.colunas):
                item = (list(self.resAutores[l].values())[c])
                self.tabelaAutores.setItem(l, c, QTableWidgetItem(str(item)))
        finally:           
            # Desconectar do servidor
            con.close()
	
#------------ Janela de Editoras ------------#

class JanelaEditora(QMainWindow):
    def __init__(self, parent=None):
        super(JanelaEditora, self).__init__(parent)

        self.topo = 100
        self.esq = 300
        self.alt = 550
        self.lar = 500
        self.titulo = 'Cadastrar Editoras'       

        # Caixa de texto para cadastro de editora:
        self.lblNomeEditora = QLabel(self)
        self.lblNomeEditora.move(100,80)
        self.lblNomeEditora.resize(250,30)
        self.lblNomeEditora.setText('Nome da editora:')
        self.txtNomeEditora = QLineEdit(self)   
        self.txtNomeEditora.move(100,110)
        self.txtNomeEditora.resize(200,30)

        # Criar botão para cadastro de editoras
        self.btnCadastraEditora = QPushButton('Cadastrar Editora', self)
        self.btnCadastraEditora.move(100, 150)
        self.btnCadastraEditora.setStyleSheet('background-color:#0000CC;color:yellow;font:bold')
        self.btnCadastraEditora.setToolTip('Clique aqui para cadastrar uma nova editora')
        self.btnCadastraEditora.clicked.connect(self.cadastraEditora)
        self.btnCadastraEditora.clicked.connect(self.carregaEditoras)

        # Tabela de Editoras
        self.tabelaEditoras = QTableWidget(self)
        self.tabelaEditoras.move(100,200)
        self.tabelaEditoras.resize(250,300)
        
        # Configurar janela
        self.configuraJanela()

    def configuraJanela(self):
        self.setGeometry(self.esq, self.topo, self.lar, self.alt)
        self.setWindowTitle(self.titulo)
        self.setStyleSheet('background-color:lightblue')
        self.carregaEditoras()

    def cadastraEditora(self):
        try:
            conectaBanco()
            self.nomeEditora = self.txtNomeEditora.text()
            with con.cursor() as cur:           
                sql = "INSERT INTO tbl_editoras (NomeEditora) VALUES " + "('" + self.nomeEditora + "');"
                cur.execute(sql)
                con.commit()
                cur.close()
        except Exception:
            msgProblemaBD()
        else:
            msgSucesso()
        finally:
            con.close()

    def carregaEditoras(self):
        try:
            conectaBanco()
            with con.cursor() as c:
                sql = 'SELECT * FROM tbl_editoras;'
                c.execute(sql)
                self.resEditoras = c.fetchall()
        except Exception:
            msgProblemaBD()
        else:
            self.linhas = len(self.resEditoras)
            self.colunas = len(self.resEditoras[0])
            self.tabelaEditoras.setRowCount(self.linhas)
            self.tabelaEditoras.setColumnCount(self.colunas)
            
            # Ajustar cabeçalho e dimensões da tabela
            self.tabelaEditoras.setHorizontalHeaderLabels((list(self.resEditoras[0].keys())))
            self.tabelaEditoras.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            
            for l in range(self.linhas):
              for c in range(self.colunas):
                item = (list(self.resEditoras[l].values())[c])
                self.tabelaEditoras.setItem(l, c, QTableWidgetItem(str(item)))
        finally:           
            # Desconectar do servidor
            con.close()

#-------------- Rotina Principal --------------#
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    tela = Janela()
    sys.exit(app.exec_())
