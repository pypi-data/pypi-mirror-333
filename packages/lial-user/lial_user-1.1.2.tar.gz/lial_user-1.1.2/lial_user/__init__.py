import pyodbc
import webbrowser
import mysql.connector
from contextlib import contextmanager


class LialUserBdd:
    """ Classe permettant de se connecter à la base de données des utilisateurs du LIAL

    :param MSconnection_dict: Un dictionnaire contenant les informations de connexion à la base de données SQL Server
    :type MSconnection_dict: dict
    :param KLconnection_dict: Un dictionnaire contenant les informations de connexion à la base de données MySQL 
    :type KLconnection_dict: dict
    :param app_id: L'identifiant de l'application dans laquelle on veut des informations (optionnel)
    :type app_id: int, optional"""
    def __init__(self, MSconnection_dict={},KLconnection_dict={},app_id=0):
        self.MSconnection_dict = MSconnection_dict

        self.KLconnection_dict = KLconnection_dict 

        self.connection = None

        self.app_id = app_id

    def connect(self):
        """ Connect to a Microsoft SQL Server database
          """
        try:
            connection_string = f"DRIVER={self.MSconnection_dict['driver']};SERVER={self.MSconnection_dict['server']};DATABASE={self.MSconnection_dict['database']};UID={self.MSconnection_dict['user']};PWD={self.MSconnection_dict['password']}"
            self.connection = pyodbc.connect(connection_string)
            print("Connected to SSMS database successfully!")
            return True
        except pyodbc.Error as e:
            print(f"Error connecting to SSMS database: {str(e)}")
            return False

    def disconnect(self):
        """ Disconnect from the Microsoft SQL Server database"""
        if self.connection:
            self.connection.close()
            print("Disconnected from SSMS database.")

    @contextmanager
    def get_kalilab_connection(self):
        """ Context manager for a MySQL connection

        :return: A MySQL connection
        """
        connection = mysql.connector.connect(
            user=self.KLconnection_dict['user'], password=self.KLconnection_dict['password'],
            host=self.KLconnection_dict['server'], database=self.KLconnection_dict['database']
        )
        try:
            yield connection
        finally:
            connection.close()

    def execute_stored_procedure(self, procedure_name, params):
        """ Éxécute une procédure stockée avec des paramètres

        :param procedure_name: Nom de la procédure stockée
        :type procedure_name: str
        :param params: Les paramètres de la procédure stockée
        :type params: list
        :return: Les résultats de la procédure stockée
        """
        with self.connection.cursor() as cursor:
            cursor.execute(f"{{CALL {procedure_name}({', '.join(['?' for _ in params])})}}", params)
            result = cursor.fetchall()
            return result
        
    def is_user_password_correct(self, user_id, password):
        """ Vérifie si le mot de passe d'un utilisateur est correct

        :param user_id: L'identifiant de l'utilisateur
        :type user_id: str
        :param password: Le mot de passe de l'utilisateur
        :type password: str
        
        :return bool: True si le mot de passe est correct, False sinon"""
        row = self.execute_stored_procedure("dbo.VerifyUserPassword", ([user_id, password]))
        if row[0][0] == 1:
            return True
        else:
            return False

    def is_user_must_change_password(self, user_id):
        """ Vérifie si l'utilisateur doit changer son mot de passe

        :param user_id: L'identifiant de l'utilisateur
        :type user_id: str
        
        :return bool: True si l'utilisateur doit changer son mot de passe, False sinon"""
        row = self.execute_stored_procedure("dbo.IsUserMustChangePassword", ([user_id]))
        if row[0][0] == 1:
            return True
        else:
            return False

    def is_user_already_logged_today(self, user_id, with_password=True,app_id_kalilab=None):
        """ Vérifie si un utilisateur s'est déjà connecté aujourd'hui

        :param user_id: L'identifiant de l'utilisateur
        :type user_id: str
        :param with_password: 1 si on veut vérifier une connexion avec mot de passe, 0 pour sans mot de passe (optionnel)
        :type with_password: bool, optional
        :param app_id_kalilab: L'identifiant de l'application (optionnel si non renseigné, prend la valeur de l'attribut app_id)
        :type app_id_kalilab: int, optional
        
        :return bool: True si l'utilisateur s'est déjà connecté aujourd'hui, False sinon"""
        if app_id_kalilab is None:
            app_id_kalilab = self.app_id
        row = self.execute_stored_procedure("dbo.TestUserLastLogin", ([user_id, app_id_kalilab,with_password]))
        if row[0][0] == 1:
            return True
        else:
            return False
            
    def log_user_activity(self,user_id,with_password,app_id_kalilab=None,heritage_id=None):
        """ Log l'activité d'un utilisateur

        :param user_id: L'identifiant de l'utilisateur
        :type user_id: str
        :param with_password: 1 si on veut logger une connexion avec mot de passe, 0 pour sans mot de passe
        :type with_password: bool
        :param app_id_kalilab: L'identifiant de l'application (optionnel si non renseigné, prend la valeur de l'attribut app_id)
        :type app_id_kalilab: int, optional
        :param heritage_id: L'identifiant de l'héritage (optionnel)
        :type heritage_id: int, optional

        :return bool: True si l'activité a été loggée, False sinon
        """
        if app_id_kalilab is None:
            app_id_kalilab = self.app_id
        row = self.execute_stored_procedure("dbo.LogUserActivity", ([user_id, app_id_kalilab,heritage_id,with_password]))
        if row[0][0] == 1:
            return True
        else:
            return False
        
    def redirect_to_password_change(self,user_id):
        """ Redirige l'utilisateur vers la page de changement de mot de passe

        :param user_id: L'identifiant de l'utilisateur
        :type user_id: str
        
        :return bool: True si la redirection a été effectuée, False sinon"""
        token = self.execute_stored_procedure("dbo.GenerateToken", ([user_id]))
        if token:
            url = f"http://10.0.2.25/A0-LOG-0045/changement-mot-de-passe/{token[0][0]}"
            webbrowser.open(url)
            return True
        else:
            return False
    
    def get_user_for_app(self,role_name=None,app_id_kalilab=None,sous_role_id=None,sous_role_value_id=None, sous_role_value_operator='=',source=None):
        """ Récupère les utilisateurs d'une application

        :param role_name: Le nom du rôle (optionnel)
        :type role_name: str, optional
        :param app_id_kalilab: L'identifiant de l'application (optionnel si non renseigné, prend la valeur de l'attribut app_id)
        :type app_id_kalilab: int, optional
        :param sous_role_id: L'identifiant du sous-rôle (optionnel)
        :type sous_role_id: int, optional
        :param sous_role_value_id: L'identifiant de la valeur du sous-rôle (optionnel)
        :type sous_role_value_id: int, optional
        :param sous_role_value_operator: L'opérateur de comparaison de la valeur du sous-rôle (optionnel)
        :type sous_role_value_operator: str, optional
        :param source: La source du droit (optionnel) autorisation ou heritage
        :type source: str, optional
        
        
        :return list: Les utilisateurs de l'application [id_kalilab, heritage_id, userName]"""
        if app_id_kalilab is None:
            app_id_kalilab = self.app_id
        with self.connection.cursor() as cursor:
            sql = f"""SELECT lahsr.utilisateur_id as user_id,ie.etr_id as user_id_kalilab, heritage_id,sous_role_id,sous_role_value_id
            FROM list_autorisation_heritage_sous_role as lahsr
            INNER JOIN id_etranger as ie on ie.utilisateur_id = lahsr.utilisateur_id and ie.source = 'kalilab'
            where id_kalilab = {app_id_kalilab}"""
            if role_name is not None:
                sql += f" and role = '{role_name}'"
            if sous_role_id is not None:
                sql += f" and sous_role_id = {sous_role_id}"
            if sous_role_value_id is not None:
                sql += f" and sous_role_value_id {sous_role_value_operator} {sous_role_value_id}"
            if source is not None:
                sql += f" and source = '{source}'"
            cursor.execute(sql)
            result = conv_cursor_to_dict(cursor)
        user_ids_str = ', '.join([f"'{str(row['user_id_kalilab'])}'" for row in result])
        user_names = self.get_kalilab_names(user_ids_str)

        for row in result:
            row['user_name'] = user_names.get(row['user_id_kalilab'], None)
        return result

    def get_kalilab_names(self,kalilab_ids):
        """ Récupère les noms des utilisateurs Kalilab

        :param kalilab_ids: Les identifiants des utilisateurs Kalilab formatés au format suivant : "'id1', 'id2', ..." 
        :type kalilab_ids: str
        
        :return dict: Les noms des utilisateurs Kalilab {id: name}"""

        kalilab_names = {}
        if kalilab_ids:
            with self.get_kalilab_connection() as connection:
                sql = f"""SELECT id, CONCAT(prenom, ' ', nom) AS kalilab_name
                        FROM personnel
                        WHERE id IN ({kalilab_ids})"""
                cursor = connection.cursor()
                cursor.execute(sql)
                kalilab_names = {row[0]: row[1] for row in cursor.fetchall()}
        return kalilab_names

    def check_user_right(self,user_id, role_name, app_id_kalilab=None, sous_role_id=None, sous_role_value_id=None,source=None):
        """ Vérifie si un utilisateur a un droit sur une application

        :param user_id: L'identifiant de l'utilisateur
        :type user_id: str
        :param app_id_kalilab: L'identifiant de l'application
        :type app_id_kalilab: int
        :param role_name: Le nom du role
        :type role_name: str
        :param sous_role_id: L'identifiant du sous-rôle (optionnel)
        :type sous_role_id: int, optional
        :param sous_role_value_id: L'identifiant de la valeur du sous-rôle (optionnel)
        :type sous_role_value_id: int, optional
        :param source: La source du droit (optionnel) autorisation ou heritage
        :type source: str, optional

        
        :return bool: True si l'utilisateur a le droit, False sinon
        """
        if app_id_kalilab is None:
            app_id_kalilab = self.app_id
        params = [user_id, app_id_kalilab, role_name,sous_role_id,sous_role_value_id,source]
        row = self.execute_stored_procedure("dbo.CheckUserRight", params)
        if row[0][0] == 1:
            return True
        else:
            return False

def conv_cursor_to_dict(cursor):
    """ Renvois une liste de dictionaire a partir des données du cursor

    :param cursor: un cursor déjà exécuté contenant des données
    :type cursor: pyodbc.connect.cursor
    """
    keys = [column[0] for column in cursor.description]
    res = []
    for row in cursor.fetchall():
        res.append(dict(zip(keys, row)))
    return res


