import mysql.connector, re
from mysql.connector import Error


class PublicacaoService:
    def __init__(self, host, user, password, database, port=3306):
        """
        Inicializa a classe de conexão ao MySQL.
        
        :param host: Endereço do servidor MySQL.
        :param user: Usuário do banco de dados.
        :param password: Senha do usuário.
        :param database: Nome do banco de dados.
        :param port: Porta do servidor MySQL (padrão 3306).
        """
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
            if self.connection.is_connected():
                print("Conexão estabelecida com o banco de dados.")
        except Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise
        
    def validar_publicacao(self, titulo, id_tipopublicacao, tags, url, texto, image_link):
        """
        Valida os dados de uma publicação antes de ser salva
        Retorna uma lista de erros de validação
        """
        
        erros = []

        # Título
        if not titulo or len(titulo.strip()) == 0:
            erros.append("O título da publicação deve ser informado.")
        
        # id_tipopublicacao
        if not id_tipopublicacao or id_tipopublicacao <= 0:
            erros.append("O Tipo da publicação deve ser informado.")
        
        # Validação das tags
        if not tags or len(tags.strip()) == 0:
            erros.append("As tags devem ser informadas.")
        else:
            # Permitir uma palavra ou múltiplas separadas por vírgula e espaço
            if not re.match(r'^([a-zA-Z0-9#]+|([a-zA-Z0-9#]+(, [a-zA-Z0-9#]+)*))$', tags):
                erros.append("As tags devem estar no formato correto. Exemplo: 'C#, ASP.Net, Linux' ou apenas 'Python'.")

        # Validação da URL
        if not url or len(url.strip()) == 0:
            erros.append("A URL deve ser informada.")
        
        # Validação do texto
        if not texto or len(texto.strip()) == 0:
            erros.append("O texto da publicação deve ser preenchido.")
        
        # Validação do link da imagem
        if image_link and len(image_link.strip()) > 0:
            # Validação do formato da URL da imagem (deve começar com http://, https://, etc)
            image_link_regex = re.compile(r'^(https?|ftp)://[^\s/$.?#].[^\s]*$', re.IGNORECASE)
            if not image_link_regex.match(image_link):
                erros.append("O link da imagem fornecido não está em um formato válido.")

        return erros
        
    def incluir_publicacao(self, titulo, id_tipopublicacao, tags, url, data_publicacao, ativo, texto, image_link):
        """
        Salva uma nova publicação no banco de dados.
        """
        query = """
        INSERT INTO publicacoes (titulo, id_tipopublicacao, tags, url, data_publicacao, ativo, texto, image_link)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (titulo, id_tipopublicacao, tags, url, data_publicacao, ativo, texto, image_link))
            self.connection.commit()  
            print("Publicação salva com sucesso")
        except Error as e:
            print(f"Erro ao salvar publicação: {e}")
            self.connection.rollback()  
            raise
        finally:
            cursor.close()        
            
    def atualizar_publicacao(self, id_publicacao, titulo, id_tipopublicacao, tags, data_revisao, ativo, texto, image_link):
        """
        Atualiza uma publicação existente no banco de dados.
        """
        query = """
        UPDATE publicacoes
        SET
            titulo = %s,
            id_tipopublicacao = %s,
            tags = %s,
            data_revisao = %s,
            ativo = %s,
            texto = %s,
            image_link = %s
        WHERE id = %s
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (titulo, id_tipopublicacao, tags, data_revisao, ativo, texto, image_link, id_publicacao))
            self.connection.commit()
            print("Publicação atualizada com sucesso")
        except Error as e:
            print(f"Erro ao atualizar publicação: {e}")
            self.connection.rollback()  # Em caso de erro, desfaz as mudanças
            raise
        finally:
            cursor.close()            
        
    def get_titulos_publicados(self):
        """
        Busca todos os titulos publicados
        """
        query = """
        SELECT 
            id,
            titulo
        FROM
            publicacoes
        ORDER BY
            titulo
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except Error as e:
            print(f"Erro ao executar consulta: {e}")
            raise
        finally:
            cursor.close()


    def get_tipos_publicacao(self):
        """
        Busca todos os tipos de publicação
        """
        
        query = """
        SELECT 
            id,
            nome
        FROM 
            tipopublicacao 
        ORDER BY 
            id
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except Error as e:
            print(f"Erro ao executar consulta: {e}")
            raise
        finally:
            cursor.close()
            
    def get_publicacao_by_id(self, id_publicacao):
        """
        Obtém dados da publicação pelo id_publicacao
        """
        query = """
            SELECT id, id_tipopublicacao, titulo, tags, url, data_publicacao, data_revisao, ativo, texto, image_link
            FROM publicacoes
            WHERE id = %s
            LIMIT 1;
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, (id_publicacao,))
            result = cursor.fetchone()
            return result
        except Error as e:
            print(f"Erro ao executar consulta: {e}")
            raise
        finally:
            cursor.close()

    def disconnect(self):
        """Encerra a conexão com o banco de dados."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexão com o banco de dados encerrada.")
