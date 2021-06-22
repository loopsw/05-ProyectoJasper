"""[summary] Gestor de conexiones con la base de datos usando MariaDB
"""
import mariadb # pip install mariadb
### Parámetros para la conexión a la base de datos
config = {
    'server':'localhost',
    'port':3306,
    'user':'userpoo',
    'password':'123Admin',
    'dataBaseName':'poo'
}
class DataBaseConnection:
    def __init__(self) -> None:
        self.server = config.get('server')
        self.port = config.get('port')
        self.user = config.get('user')
        self.password = config.get('password')
        self.dbName = config.get('dataBaseName')
        self.myConnect = None
        self.myCursor = None
        self.result = []

    def executeQuery(self,sql):
        try:
            self.__connect()
            self.myCursor.execute(sql) 
            if self.myCursor.rowcount > 0: # si es update o insert
                self.myConnect.commit()
                self.__disconnect()
                return True
            else:                          # si es select
                result = []
                for row in self.myCursor:
                    result.append(row) 
                self.__disconnect()
                return result           
        except mariadb.Error as e:
            print("Error al ejecutar la query: ",sql,"\nError: ",e)
            self.myConnect.rollback()
            self.__disconnect()
            return False
            
    def __connect(self):
        try:
            self.myConnect = mariadb.connect(
                user = self.user,
                password = self.password,
                host = self.server,
                port = self.port,
                database = self.dbName,
                autocommit=False
            )
            self.myCursor = self.myConnect.cursor()
        except mariadb.Error as e:
            print("Error al conectar con ", self.dbName,"Error: ",{e})

    def __disconnect(self):
        try:
            self.myCursor.close()
            self.myConnect.close()
        except mariadb.Error as e:
            print("Error al cerrar conexión con ",self.dbName,"\nError: ",{e})


if __name__ == "__main__":

    # Instancia a la base de datos
    myDB = DataBaseConnection()
    myDB.executeQuery('SELECT * FROM tipoClientes')
    print(myDB.result)