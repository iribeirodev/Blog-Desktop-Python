import sqlite3
import os

class ConfigService:
    def __init__(self, db_path='database/infoconexao.db'):
        self.db_path = db_path
        
    def _connect(self):
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Arquivo de banco de dados não encontrado: {self.db_path}")
        
        return sqlite3.connect(self.db_path)
    
    def get_default_connection(self):
        """
        Recupera a configuração de conexão marcada como default.
        """
        query = "SELECT url, username, password, driverclassname, type FROM info WHERE isdefault = 1;"
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            conn.close()

            if result:
                return {
                    "url": result[0],
                    "username": result[1],
                    "password": result[2],
                    "driverclassname": result[3],
                    "type": result[4]
                }
            else:
                raise ValueError(f"Nenhuma configuração encontrada como default.")
        except sqlite3.Error as e:
            print(f"Erro ao acessar o banco de dados: {e}")
            return None            
    
    def get_distinct_types(self):
        """
        Retorna os tipos distintos de conexão ('local', 'remote', etc.) presentes na tabela 'info'.

        :return: Lista de tipos distintos.
        """
        query = "SELECT DISTINCT type FROM info;"
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()

            # Retorna uma lista com os tipos distintos encontrados
            return [row[0] for row in result]

        except sqlite3.Error as e:
            print(f"Erro ao acessar o banco de dados: {e}")
            return []
        
    def set_connection_default(self, value_default, type):
        """
        Atualiza qual conexão será considerada padrão

        Args:
            value_default (inteiro): Valor podendo ser 0 ou 1
            type (string): tipo de conexão (local, remota, ...)
        """
        query = "UPDATE info SET isdefault = ? WHERE type = ?;"
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(query, (value_default, type,))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Erro ao fazer update no banco de dados: {e}")
            return None            
        
    def set_connection_info(self, url, username, password, type):
        """
        Atualiza os dados de uma conexão pelo seu tipo

        Args:
            url (string): URL
            username (string): User Name
            password (string): Password
            type (string): tipo de conexão (local, remota, ...)
        """
        query = "UPDATE info SET url = ?, username = ?, password = ? WHERE type = ?;"
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(query, (url, username, password, type,))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Erro ao fazer update no banco de dados: {e}")
            return None   
    
    def get_config(self, type):
        """
        Recupera a configuração de conexão com base no tipo ('local' ou 'remote').

        :param type: Tipo da conexão, pode ser 'local' ou 'remote'.
        Retorna um dicionário com os campos 'url', 'username', 'password', 'driverclassname' e 'type'.
        """
        query = "SELECT url, username, password, driverclassname, type, isdefault FROM info WHERE type = ?;"
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(query, (type,))
            result = cursor.fetchone()
            conn.close()

            if result:
                return {
                    "url": result[0],
                    "username": result[1],
                    "password": result[2],
                    "driverclassname": result[3],
                    "type": result[4],
                    "isdefault": result[5]
                }
            else:
                raise ValueError(f"Nenhuma configuração encontrada para o tipo '{type}'.")

        except sqlite3.Error as e:
            print(f"Erro ao acessar o banco de dados: {e}")
            return None