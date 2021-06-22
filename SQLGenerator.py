class SQLGenerator:
    def __init__(self,tableName) -> None:
        self.tableName = tableName
        self.campos = {}

    def addCampo(self,column, value):
        self.campos[column] = value
    
    def generateSelect(self):
        sqlQuery = "SELECT * FROM " + self.tableName
        return sqlQuery

    def generateFind(self,column,value):
        sqlQuery = "SELECT * FROM "+ self.tableName + " WHERE {0} = '{1}'".format(column,value)
        return sqlQuery

    def generateInsert(self):
        sqlQuery = "INSERT INTO  " + self.tableName + "( "
        contItems = 0
        for key in self.campos.keys():
            contItems += 1
            sqlQuery += str(key)
            if contItems < len(self.campos):
                sqlQuery += ", "
        sqlQuery += ") VALUES ("
        contItems = 0
        for value in self.campos.values():
            contItems += 1
            if type(value) == int:
                sqlQuery += str(value)
            else:
                sqlQuery += "'" + str(value) + "'"
            if contItems < len(self.campos):
                sqlQuery += ", "        
        sqlQuery += ")"
        return sqlQuery

    def generateUpdate(self,column,valor):
        sqlQuery = "UPDATE " + self.tableName + " SET "
        contItems = 0
        for key,value in self.campos.items():
            contItems += 1
            sqlQuery += str(key) + " = " 
            if type(value) == int:
                sqlQuery +=  str(value)
            else:
                sqlQuery += "'" + str(value) + "'"
            if contItems < len(self.campos):
                sqlQuery += ", "
        sqlQuery += " WHERE {} = '{}'".format(column,valor)
        return sqlQuery

    def generateDelete(self,column,value):
        sqlQuery = "DELETE FROM " + self.tableName + " WHERE {0} = {1} LIMIT 1".format(column,value)
        return sqlQuery;

    def __str__(self) -> str:
        cadena = "Tabla "+ self.tableName + "\n"
        for key,value in self.campos.items():
            cadena += " * " + key + ":" + str(value) + "\n"
        return cadena


if __name__ == "__main__":
    sqlG = SQLGenerator('Clientes')
    sqlG.addCampo('nombre','Juan')
    sqlG.addCampo('edad',20)
    sqlG.addCampo('nombre','Jackson')
    print(sqlG)
    print(sqlG.generateInsert())
    print(sqlG.generateUpdate('edad',20))
    print(sqlG.generateDelete('nombre',12555))