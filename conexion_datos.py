import pyodbc
server = 'LAPTOP-C9U1MOE1\SQLEXPRESS'
database = 'base_datos'
user ='sa'
password='123456'


class Registro_datos():

    def __init__(self):
        try:
            self.conexion= pyodbc.connect('DRIVER={SQL SERVER}; SERVER='+ server+'; DATABASE='+ database+'; USER='+user+';PWD='+password)
            print('conexion exitosa')

        except :
            print('conexion fallida')

    def agregar_producto(self,codigo, nombre, tp_producto,precio,cantidad):
        cursorInsert = self.conexion.cursor()
        consultar ="Insert into tabla(CODIGO,NOMBRE,TP_PRODUCTO,PRECIO,CANTIDAD) values(?,?,?,?,?)"
        cursorInsert.execute(consultar,(codigo,nombre,tp_producto,precio,cantidad))
        self.conexion.commit()
        cursorInsert.close()

    def mostrar_productos(self):
        cursor = self.conexion.cursor()
        mostrar = "Select * From tabla"
        cursor.execute(mostrar)
        registro = cursor.fetchall()
        return registro

    def buscar_producto(self,nombre_producto):
        cursor = self.conexion.cursor()
        buscar = "Select * From tabla WHERE NOMBRE = {}".format(nombre_producto)
        cursor.execute(buscar)
        name = cursor.fetchall()
        cursor.close()
        return name

    def eliminar_produc(self,nombre):
        cursor = self.conexion.cursor()
        eliminar ="Delete From tabla WHERE NOMBRE ={} ".format(nombre)
        cursor.execute(eliminar)
        self.conexion.commit()
        cursor.close()


        


            


         

    



   

