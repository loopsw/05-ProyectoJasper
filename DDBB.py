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
    
    def insertClient(self,client):
        sqlQuery = "INSERT INTO clientes( "
        contItems = 0
        for key in client.keys():
            contItems += 1
            sqlQuery += str(key)
            if contItems < len(client):
                sqlQuery += ", "
        sqlQuery += ") VALUES ("
        contItems = 0
        for value in client.values():
            contItems += 1
            if type(value) == int:
                sqlQuery += str(value)
            else:
                sqlQuery += "'" + str(value) + "'"
            if contItems < len(client):
                sqlQuery += ", "        
        sqlQuery += ")"
        self.__executeQuery(sqlQuery)

    def updateClient(self,nif,client):
        sqlQuery = "UPDATE clientes SET "
        contItems = 0
        for key,value in client.items():
            contItems += 1
            sqlQuery += str(key) + " = " 
            if type(value) == int:
                sqlQuery +=  str(value)
            else:
                sqlQuery += "'" + str(value) + "'"
            if contItems < len(client):
                sqlQuery += ", "
        sqlQuery += " WHERE nif = {}".format(nif)
        self.__executeQuery(sqlQuery)

    def deleteClientByDNI(self,dni):
        sqlQuery = "DELETE FROM clientes WHERE nif = {0} LIMIT 1".format(dni)
        self.__executeQuery(sqlQuery)

    def findClientByDNI(self,dni):
        sqlQuery = "SELECT * FROM clientes WHERE nif = {0}".format(dni)
        self.__executeQuery(sqlQuery)
        return self.result

    def __executeQuery(self,sql):
        try:
            self.__connect()
            self.myCursor.execute(sql) 
            if self.myCursor.rowcount > 0: # si es update o insert
                self.myConnect.commit()
                self.result = []
            else:                          # si es select
                for row in self.myCursor:
                    self.result.append(row)            
        except mariadb.Error as e:
            print("Error al ejecutar la query: ",sql,"\nError: ",e)
            self.myConnect.rollback()
            self.result = []
        self.__disconnect()

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

    ### test select
    dni = '123456789'    
    result = myDB.findClientByDNI(dni)
    print(result)
    
    ### test insert
    clientInsert = {
        'nombre':"Jackson Reyes",
        'nif':987654321,
        'direccion':'Cartagena',
        'poblacion':'Cartagena',
        'provincia':'Murcia',
        'cp':30300,
        'telefono':123456789,
        'email':'jackson@reyes.es',
        'recargo':1,
        'tipoCliente':1,
        'fechaAlta': '2021-06-10',
        'observaciones':'no hay 3'
    }     
    myDB.insertClient(clientInsert)

    ### Test update
    clientUpdate = {
        'nombre':"Jackson Reyes",
        'nif':1987654321,
        'direccion':'Cartagena',
        'poblacion':'Cartagena',
        'provincia':'Murcia',
        'cp':30203,
        'telefono':123456789,
        'email':'jackson@reyes.es',
        'recargo':1,
        'tipoCliente':1,
        'fechaAlta': '2021-06-10',
        'observaciones':'no hay 3'
    } 
    nif = 987654321
    #myDB.updateClient(nif,clientUpdate)

    #### Test delete clients
    #myDB.deleteClientByDNI(nif)
