from PyQt5.QtWidgets import QDialog, QComboBox, QMessageBox
from PyQt5.uic import loadUi
from enumScreenState import EnumScreenState
from services.config_service import ConfigService
from typing import Union
import sys

class ConfigDialog(QDialog):
    """
    Janela de Configurações
    """
    def __init__(self, parent=None):
        # Classe de serviço de configuração
        self.config_service = ConfigService()

        super().__init__(parent)
        loadUi("configuracoes.ui", self)
        self.setFixedSize(self.width(), self.height())
        self.carregar_combo_tipo_conexao()
        self.cboLocalConexao.currentIndexChanged.connect(self.on_cboLocalConexao_currentIndexChanged)
        self.btnDefault.clicked.connect(self.on_btnDefault_Click)
        self.btnAplicar.clicked.connect(self.on_btnAplicar_Click)
        self.mudar_estado_tela(EnumScreenState.INICIAL)
        
    def mudar_estado_tela(self, state: EnumScreenState):
        """
        Habilita ou desabilita controles de acordo com o parâmetro state
        """
        match state:
            case EnumScreenState.INICIAL:
                self.txtURL.setEnabled(False)
                self.txtUsername.setEnabled(False)
                self.txtPassword.setEnabled(False)
                self.btnDefault.setEnabled(False)
                self.btnAplicar.setEnabled(False)
                self.lblIsDefault.setText("")
            case EnumScreenState.SELECIONADO:
                self.txtURL.setEnabled(True)
                self.txtUsername.setEnabled(True)
                self.txtPassword.setEnabled(True)
                self.btnDefault.setEnabled(True)
                self.btnAplicar.setEnabled(True)
            
    def exibir_mensagem_reiniciar(self):
        """
        Exibe mensagem de reinicialização do aplicativo
        """
        alert = QMessageBox()
        alert.setWindowTitle("Atenção")
        alert.setText("Para que a nova configuração tenha efeito, será necessário reiniciar a aplicação.")
        alert.setIcon(QMessageBox.Information)
        alert.setStandardButtons(QMessageBox.Ok)
        alert.exec_()
        
    def exibir_mensagem_alerta(self, texto):
        alert = QMessageBox(self)
        alert.setWindowTitle("Atenção")
        alert.setText(texto)
        alert.setIcon(QMessageBox.Warning)
        alert.exec_()   
        
    def carregar_combo_tipo_conexao(self):
        """
        Carregar a combo com o tipo de conexão
        """
        tipos_conexao = self.config_service.get_distinct_types()
        
        if tipos_conexao:
            self.cboLocalConexao.clear()
            
        for tipo in tipos_conexao:
            self.cboLocalConexao.addItem(tipo)
            
        self.cboLocalConexao.setCurrentIndex(-1)             
        
    def on_btnDefault_Click(self):
        """
        Atualiza qual conexão será considerada a padrão
        """
        self.exibir_mensagem_reiniciar()
        tipo_selecionado = self.cboLocalConexao.currentText()
        if tipo_selecionado:
            total_items = self.cboLocalConexao.count()
            # Deixa o item selecionado com isdefault = 1 e os outros com isdefault = 0
            for index in range(total_items):
                item_text = self.cboLocalConexao.itemText(index)
                if item_text == tipo_selecionado:
                    self.config_service.set_connection_default(1, item_text)
                else:
                    self.config_service.set_connection_default(0, item_text)
            sys.exit(0)
            
    def on_btnAplicar_Click(self):
        """
        Atualiza a informação de conexão de acordo com os valores preenchidos.
        """
        if not self.txtURL.text().strip():
            self.exibir_mensagem_alerta("A URL deve ser informada")
            self.txtURL.setFocus()
            return
        
        if not self.txtUsername.text().strip():
            self.exibir_mensagem_alerta("O User Name deve ser informado")
            self.txtUsername.setFocus()
            return
        
        if not self.txtPassword.text().strip():
            self.exibir_mensagem_alerta("O Password deve ser informado")
            self.txtPassword.setFocus()
            return
        
        self.exibir_mensagem_reiniciar()
        self.config_service.set_connection_info(
            self.txtURL.text(), 
            self.txtUsername.text(), 
            self.txtPassword.text(), 
            self.cboLocalConexao.currentText())
        sys.exit(0)
        
    def on_cboLocalConexao_currentIndexChanged(self):
        """
        Carregar as configurações ao selecionar um item da combo
        """
        tipo_selecionado = self.cboLocalConexao.currentText()
        
        if tipo_selecionado:
            self.mudar_estado_tela(EnumScreenState.SELECIONADO)
            config = self.config_service.get_config(tipo_selecionado)
            if config:
                self.txtURL.setText(config['url'])
                self.txtUsername.setText(config['username'])
                self.txtPassword.setText(config['password'])
                isDefault = "Sim" if config['isdefault'] == 1 else "Não"
                self.lblIsDefault.setText(isDefault)
            