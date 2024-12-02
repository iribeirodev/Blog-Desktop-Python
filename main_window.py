from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from config_dialog import ConfigDialog
from PyQt5.uic import loadUi
import sys
import re
from datetime import datetime
from unidecode import unidecode

from enumScreenState import EnumScreenState
from services.config_service import ConfigService
from services.publicacao_service import PublicacaoService

class MainWindow(QMainWindow):
    def __init__(self):
        # Classe de serviço de configuração
        self.config_service = ConfigService()
        # Configuração default
        self.default_config = None
        # Classe de serviço de publicação
        self.publicacao_service = None
        self.current_state = None
                
        super().__init__()
        loadUi("principal.ui", self)
        self.setFixedSize(self.width(), self.height())  

        self.btnLerPublicacao.clicked.connect(self.on_btnLerPublicacao_Click)
        self.btnEditarPublicacao.clicked.connect(self.on_btnEditarPublicacao_Click)
        self.btnNovaPublicacao.clicked.connect(self.on_btnNovaPublicacao_Click)
        self.btnConfiguracoes.clicked.connect(self.on_btnConfiguracoes_Click)
        self.btnSalvarPublicacao.clicked.connect(self.on_btnSalvarPublicacao_Click)
        self.btnCancelar.clicked.connect(self.on_btnCancelar_Click)
        self.cboTipoPublicacao.currentIndexChanged.connect(self.on_cboTipoPublicacao_changed)
        self.txtTituloPublicacao.textChanged.connect(self.on_txtTituloPublicacao_textChanged)
        
        self.default_config = self.config_service.get_default_connection()
        if self.default_config:
            self.exibir_status_conexao(f"Conectado em {self.default_config['url']} como {self.default_config['username']}")
            self.obter_dados_conexao()
            self.obter_titulos_publicados()
            self.obter_tipos_publicacao()
            self.mudar_estado_tela(EnumScreenState.INICIAL)
        else:
            self.exibir_mensagem_alerta("Nenhuma conexão foi definida como padrão !")
            
    def limpar_campos(self):
        """
        Limpa os campos da tela
        """
        self.cboTitulosPublicados.setCurrentIndex(-1)
        self.cboTipoPublicacao.setCurrentIndex(-1)
        self.txtTituloPublicacao.setText("")
        self.txtTagsPublicacao.setText("")
        self.txtURLPublicacao.setText("")
        self.txtPublicadoEm.setText("")
        self.txtRevisadoEm.setText("")
        self.chkPublicacaoAtiva.setChecked(False)
        self.txtLinkImagem.setText("")
        self.txtTextoPublicacao.setPlainText("")
        
    def mudar_estado_tela(self, state: EnumScreenState):
        """
        Habilita ou desabilita controles de acordo com o parâmetro state
        """
        self.current_state = state
        match state:
            case EnumScreenState.INICIAL:
                self.cboTitulosPublicados.setCurrentIndex(-1)
                self.cboTitulosPublicados.setEnabled(True)
                self.cboTipoPublicacao.setCurrentIndex(-1)
                self.cboTipoPublicacao.setEnabled(False)
                
                self.txtTituloPublicacao.setEnabled(False)
                self.txtTituloPublicacao.setReadOnly(True)
                self.txtTituloPublicacao.setText("")
                
                self.txtTagsPublicacao.setEnabled(False)
                self.txtTagsPublicacao.setReadOnly(True)
                self.txtTagsPublicacao.setText("")
                
                self.chkPublicacaoAtiva.setEnabled(False)
                
                self.txtLinkImagem.setEnabled(False)
                self.txtLinkImagem.setReadOnly(True)
                
                self.txtTextoPublicacao.setEnabled(False)
                self.txtTextoPublicacao.setReadOnly(True)
                
                self.btnNovaPublicacao.setEnabled(True)
                self.btnSalvarPublicacao.setEnabled(False)
                self.btnConfiguracoes.setEnabled(True)
                self.btnCancelar.setEnabled(False)
                
                self.btnLerPublicacao.setEnabled(True)
                self.btnEditarPublicacao.setEnabled(True)
                
            case EnumScreenState.NOVO:
                self.cboTitulosPublicados.setEnabled(False)
                self.cboTipoPublicacao.setEnabled(True)
                
                self.txtTituloPublicacao.setEnabled(True)
                self.txtTituloPublicacao.setReadOnly(False)
                
                self.txtTagsPublicacao.setEnabled(True)
                self.txtTagsPublicacao.setReadOnly(False)
                
                self.chkPublicacaoAtiva.setEnabled(True)

                self.txtLinkImagem.setEnabled(True)
                self.txtLinkImagem.setReadOnly(False)
                
                self.txtTextoPublicacao.setEnabled(True)
                self.txtTextoPublicacao.setReadOnly(False)
                
                self.btnNovaPublicacao.setEnabled(False)
                self.btnSalvarPublicacao.setEnabled(True)
                self.btnCancelar.setEnabled(True)
                self.btnConfiguracoes.setEnabled(False)
                
                self.btnLerPublicacao.setEnabled(False)
                self.btnEditarPublicacao.setEnabled(False)
                
                self.limpar_campos()
                
            case EnumScreenState.SELECIONADO:
                self.cboTitulosPublicados.setEnabled(False)
                self.cboTipoPublicacao.setEnabled(True)
                
                self.txtTituloPublicacao.setEnabled(True)
                self.txtTituloPublicacao.setReadOnly(False)
                
                self.txtTagsPublicacao.setEnabled(True)
                self.txtTagsPublicacao.setReadOnly(False)
                
                self.chkPublicacaoAtiva.setEnabled(True)
                
                self.txtLinkImagem.setEnabled(True)
                self.txtLinkImagem.setReadOnly(False)
                
                self.txtTextoPublicacao.setEnabled(True)
                self.txtTextoPublicacao.setReadOnly(False)
                
                self.btnNovaPublicacao.setEnabled(False)
                self.btnSalvarPublicacao.setEnabled(True)
                self.btnConfiguracoes.setEnabled(False)
                self.btnCancelar.setEnabled(True)
                
                self.btnLerPublicacao.setEnabled(False)
                self.btnEditarPublicacao.setEnabled(False)
                
            case EnumScreenState.VISUALIZAR:
                self.cboTitulosPublicados.setEnabled(True)
                self.cboTipoPublicacao.setEnabled(False)
                
                self.txtTituloPublicacao.setEnabled(True)
                self.txtTituloPublicacao.setReadOnly(True)
                
                self.txtTagsPublicacao.setEnabled(True)
                self.txtTituloPublicacao.setReadOnly(True)
                
                self.chkPublicacaoAtiva.setEnabled(False)

                self.txtLinkImagem.setEnabled(True)
                self.txtLinkImagem.setReadOnly(True)
                
                self.txtTextoPublicacao.setEnabled(True)
                self.txtTextoPublicacao.setReadOnly(True)
                
                self.btnNovaPublicacao.setEnabled(True)
                self.btnSalvarPublicacao.setEnabled(False)
                self.btnCancelar.setEnabled(False)
                self.btnConfiguracoes.setEnabled(True)
                
                self.btnLerPublicacao.setEnabled(True)
                self.btnEditarPublicacao.setEnabled(True)
        
    def obter_dados_conexao(self):
        """
        Retorna um dicionário com os dados da conexão default
        """
        url = self.default_config["url"]
        url = url.replace("jdbc:mysql://", "")
        
        # Dividindo a URL em servidor/porta e banco de dados
        server, rest = url.split(':', 1)
        port, database = rest.split('/', 1)
        port = int(port)
        
        return {
            "host": server,
            "port": port,
            "database": database,
            "user": self.default_config['username'],
            "password": self.default_config['password']
        }
        
    def exibir_publicacao(self, id_publicacao):
        """
        Apenas exibe valores para os campos dado o parâmetro id_publicacao
        """
        result = self.publicacao_service.get_publicacao_by_id(id_publicacao)
        if result:
            index = self.cboTipoPublicacao.findData(result['id_tipopublicacao'])
            if index != -1:
                self.cboTipoPublicacao.setCurrentIndex(index)
            self.txtTituloPublicacao.setText(result['titulo'])
            self.txtTagsPublicacao.setText(result['tags'])
            self.txtURLPublicacao.setText(result['url'])
            self.txtPublicadoEm.setText(result['data_publicacao'].strftime('%d/%m/%Y'))
            if not result['data_revisao'] is None:
                self.txtRevisadoEm.setText(result['data_revisao'].strftime('%d/%m/%Y'))
            self.chkPublicacaoAtiva.setChecked(result['ativo'] == 1)
            if not result['image_link'] is None:
                self.txtLinkImagem.setText(result['image_link'])
            self.txtTextoPublicacao.setPlainText(result['texto'])
            self.mudar_estado_tela(EnumScreenState.VISUALIZAR)
        
    def editar_publicacao(self, id_publicacao):
        """
        Após selecionado um item da combo de títulos publicados, recebe o id_publicacao como parâmetro e carrega os campos para edição
        """
        result = self.publicacao_service.get_publicacao_by_id(id_publicacao)
        if result:
            index = self.cboTipoPublicacao.findData(result['id_tipopublicacao'])
            if index != -1:
                self.cboTipoPublicacao.setCurrentIndex(index)
            self.txtTituloPublicacao.setText(result['titulo'])
            self.txtTagsPublicacao.setText(result['tags'])
            self.txtURLPublicacao.setText(result['url'])
            self.txtPublicadoEm.setText(result['data_publicacao'].strftime('%d/%m/%Y'))
            if not result['data_revisao'] is None:
                self.txtRevisadoEm.setText(result['data_revisao'].strftime('%d/%m/%Y'))
            self.chkPublicacaoAtiva.setChecked(result['ativo'] == 1)
            if not result['image_link'] is None:
                self.txtLinkImagem.setText(result['image_link'])
            self.txtTextoPublicacao.setPlainText(result['texto'])
            self.mudar_estado_tela(EnumScreenState.SELECIONADO)
            self.cboTipoPublicacao.setFocus()
        
    def obter_titulos_publicados(self):
        """
        Carrega a combo de títulos publicados
        """
        conn = self.obter_dados_conexao()
        self.publicacao_service = PublicacaoService(conn['host'], conn['user'], conn['password'], conn['database'], conn['port'])
        tipos_publicacao = self.publicacao_service.get_titulos_publicados()
        
        self.cboTitulosPublicados.clear()
        for tipo in tipos_publicacao:
            self.cboTitulosPublicados.addItem(tipo['titulo'], tipo['id'])
            
        self.cboTitulosPublicados.setCurrentIndex(-1)
        
    def obter_tipos_publicacao(self):
        """
        Carrega a combo de tipos de publicação
        """
        conn = self.obter_dados_conexao()
        self.publicacao_service = PublicacaoService(conn['host'], conn['user'], conn['password'], conn['database'], conn['port'])
        tipos_publicacao = self.publicacao_service.get_tipos_publicacao()
        
        self.cboTipoPublicacao.clear()
        for tipo in tipos_publicacao:
            self.cboTipoPublicacao.addItem(tipo['nome'], tipo['id'])
            
        self.cboTipoPublicacao.setCurrentIndex(-1)

    def on_btnSalvarPublicacao_Click(self):
        """
        Click botão btnSalvarPublicacao 
        """
        index = self.cboTipoPublicacao.currentIndex()
        id_tipo_publicacao = self.cboTipoPublicacao.itemData(index)
        
        if self.encontrar_titulo_combobox(self.txtTituloPublicacao.text()) != -1:
            self.exibir_mensagem_alerta("Esse título já foi utilizado em outra publicação.")
            return
        
        erros = self.publicacao_service.validar_publicacao(
            self.txtTituloPublicacao.text(),
            id_tipo_publicacao,
            self.txtTagsPublicacao.text(),
            self.txtURLPublicacao.text(),
            self.txtTextoPublicacao.toPlainText(),
            self.txtLinkImagem.text())
            
        if erros:
            erro_message = "\n".join(erros)
            self.exibir_mensagem_alerta(erro_message)
            return
            
        match self.current_state:
            case EnumScreenState.NOVO:
                self.publicacao_service.incluir_publicacao(
                    self.txtTituloPublicacao.text(),
                    id_tipo_publicacao,
                    self.txtTagsPublicacao.text(),
                    self.txtURLPublicacao.text(),
                    datetime.now().strftime("%Y-%m-%d"),
                    1 if self.chkPublicacaoAtiva.isChecked() else 0,
                    self.txtTextoPublicacao.toPlainText(),
                    self.txtLinkImagem.text()
                )
                
                self.obter_titulos_publicados()
                self.exibir_mensagem_alerta("Publicação salva.")
            case EnumScreenState.SELECIONADO:
                index = self.cboTitulosPublicados.currentIndex()
                id_publicacao = self.cboTitulosPublicados.itemData(index)
                
                self.publicacao_service.atualizar_publicacao(
                    id_publicacao,
                    self.txtTituloPublicacao.text(),
                    id_tipo_publicacao,
                    self.txtTagsPublicacao.text(),
                    datetime.now().strftime("%Y-%m-%d"),
                    1 if self.chkPublicacaoAtiva.isChecked() else 0,
                    self.txtTextoPublicacao.toPlainText(),
                    self.txtLinkImagem.text()
                )
                
                self.obter_titulos_publicados()
                self.exibir_mensagem_alerta("Publicação salva.")
                
        self.mudar_estado_tela(EnumScreenState.INICIAL)
        
    def on_btnConfiguracoes_Click(self):
        """
        Click botão Configurações
        """
        dialog = ConfigDialog(self)
        dialog.exec_()
      
    def on_btnLerPublicacao_Click(self):
        """
        Click botão btnLerPublicacao
        """
        index = self.cboTitulosPublicados.currentIndex()
        if index == -1:
            self.exibir_mensagem_alerta("Primeiro selecione uma publicação na lista")      
            return
        
        selected_id = self.cboTitulosPublicados.itemData(index)
        self.exibir_publicacao(selected_id)
        
    def on_btnEditarPublicacao_Click(self):
        """
        Click botão btnEditarPublicacao
        """
        index = self.cboTitulosPublicados.currentIndex()
        if index == -1:
            self.exibir_mensagem_alerta("Primeiro selecione uma publicação na lista")      
            return
        
        selected_id = self.cboTitulosPublicados.itemData(index)
        self.editar_publicacao(selected_id)
      
    def on_btnNovaPublicacao_Click(self):
        """
        Click botão btnNovaPublicacao
        """
        self.mudar_estado_tela(EnumScreenState.NOVO)      
      
    def on_btnCancelar_Click(self):
        """
        Click botão Cancelar
        """
        self.limpar_campos()
        self.mudar_estado_tela(EnumScreenState.INICIAL)      
        
    def exibir_status_conexao(self, texto):
        """
        Exibe texto na barra de status da janela
        """
        self.statusbar.showMessage(texto)
        
    def exibir_mensagem_alerta(self, texto):
        """
        Usa o componente QMessageBox para exibir uma mensagem do tipo Alerta
        """
        alert = QMessageBox(self)
        alert.setWindowTitle("Atenção")
        alert.setText(texto)
        alert.setIcon(QMessageBox.Warning)
        alert.exec_()      
        
    def encontrar_titulo_combobox(self, texto):
        """
        Percorre os textos de um QComboBox para encontrar um texto específico.
        """
        for i in range(self.cboTitulosPublicados.count()):
            if self.cboTitulosPublicados.itemText(i) == texto:
                return i
            
        return -1  
        
    def formatar_para_url(self, texto):
        """
        Converte o texto para um valor amigável de URL
        """
        texto = unidecode(texto)    # Remove os acentos com unidecode
        texto = texto.lower()
        texto = texto.replace(" ", "_")
    
        # Remove caracteres especiais
        texto = re.sub(r'[^a-z0-9_]', '', texto)
    
        return texto   
        
    def on_cboTitulosPublicados_changed(self, index):
        """
        Mudança de seleção em cboTitulosPublicados
        """
        if index >= 0:
            selected_id = self.cboTitulosPublicados.itemData(index)
            self.editar_publicacao(selected_id)
        
    def on_cboTipoPublicacao_changed(self, index):
        """
        Mudança de seleção em cboTipoPublicacao
        """
        if index >= 0:
            selected_id = self.cboTipoPublicacao.itemData(index)
            selected_nome = self.cboTipoPublicacao.currentText()

    def on_txtTituloPublicacao_textChanged(self):
        """
        Copia o texto do titulo para a url
        """
        text = self.txtTituloPublicacao.text()
        self.txtURLPublicacao.setText(self.formatar_para_url(text))

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()

    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Exiting with error: {e}")

if __name__ == "__main__":
    main()
