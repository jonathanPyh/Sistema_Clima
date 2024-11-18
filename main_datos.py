from tkinter import Entry,Label,Frame,Tk,Button,ttk,Scrollbar,VERTICAL,HORIZONTAL,StringVar,END
from conexion_datos import*


class Registro(Frame):
    def __init__(self,master, *args, **kwargs):
        super().__init__(master,*args,**kwargs)
        
        self.frame1 = Frame(master)
        self.frame1.grid(columnspan=2, column=0,row=0)
        self.frame2 = Frame(master, bg='navy')
        self.frame2.grid(column=0, row=1)
        self.frame3 = Frame(master)
        self.frame3.grid(rowspan=2, column=1, row=1)

        self.frame4 = Frame(master, bg = 'black')
        self.frame4.grid(column=0, row=2)

        self.codigo = StringVar()
        self.nombre = StringVar()
        self.tp_producto = StringVar()
        self.precio = StringVar()
        self.cantidad = StringVar()
        self.buscar = StringVar()

        self.base_datos = Registro_datos()
        self.create_wietgs()

    def create_wietgs(self):
        Label(self.frame1, text= 'R E G I S T R O \t D E \t PRODUCTO', bg='gray22', fg='white', font=('Orbitron',15,'bold')).grid(column=0, row=0)

        Label(self.frame2, text='Agregar Nuevos Productos', fg='white', bg='navy', font=('Rockwell',12,'bold')).grid(columnspan=2,column=0,row=0, pady=5)
        Label(self.frame2, text= 'Codigo', fg='white', bg='navy', font=('Rockwell',13,'bold')).grid(column=0, row=1, pady=15)
        Label(self.frame2, text='Nombre', fg='white', bg='navy', font=('Rockwell', 13,'bold')).grid(column=0, row=2, pady=15)
        Label(self.frame2, text='Tp_producto',fg='white', bg='navy', font=('Rockwell', 13,'bold')).grid(column=0,row=3,pady=15)
        Label(self.frame2, text='Precio', fg='white', bg='navy', font=('Rockwell',13,'bold')).grid(column=0, row=4,pady=15)
        Label(self.frame2,text='Cantidad', fg='white', bg='navy',font=('Rockwell',13,'bold')).grid(column=0,row=5,pady=15)

        Entry(self.frame2, textvariable=self.codigo, font=('Arial',12)).grid(column=1,row=1,padx=5)
        Entry(self.frame2,textvariable=self.nombre, font=('Arial',12)).grid(column=1,row=2)
        Entry(self.frame2,textvariable=self.tp_producto,font=('Arial',12)).grid(column=1,row=3)
        Entry(self.frame2, textvariable=self.precio, font=('Arial',12)).grid(column=1,row=4)
        Entry(self.frame2,textvariable=self.cantidad, font=('Arial',12)).grid(column=1,row=5)

        Label(self.frame4, text='Control', fg='white', bg='black', font=('Rockwell',12,'bold')).grid(columnspan=3, column=0,row=0, pady=1,padx=4)
        Button(self.frame4, command=self.agregar_datos, text='REGISTRAR', font=('Arial',10,'bold'),bg='magenta2').grid(column=0,row=1,pady=10,padx=4)
        Button(self.frame4, command=self.limpiar_datos, text='LIMPIAR', font=('Arial',10,'bold'),bg='orange red').grid(column=1,row=1,padx=10)
        Button(self.frame4,command=self.eliminar_fila,text='ELIMINAR',font=('Arial',10,'bold'),bg='yellow').grid(column=2,row=1,padx=4)
        Button(self.frame4, command=self.buscar_nombre, text='BUSCAR NOMBRE',font=('Arial',8,'bold'),bg='orange').grid(columnspan=2,column=1,row=2)
        Entry(self.frame4,textvariable=self.buscar, font=('Arial,12'),width=10).grid(column=0,row=2,pady=1,padx=8)
        Button(self.frame4,command= self.mostrar_todo,text='Mostrar Datos de SQL',font=('Arial',10,'bold'),bg='green2').grid(columnspan=3,column=0,row=3,pady=8)

        self.table = ttk.Treeview(self.frame3, height=21)
        self.table.grid(column=0,row=0)

        ladox = Scrollbar(self.frame3, orient= HORIZONTAL,command=self.table.xview)
        ladox.grid(column=0,row=1,sticky='ew')
        ladoy = Scrollbar(self.frame3, orient=VERTICAL,command=self.table.yview)
        ladoy.grid(column=1, row=0,sticky='ns')

        self.table.configure(xscrollcommand=ladox.set,yscrollcommand=ladoy.set)

        self.table['columns']=('Nombre', 'Tp_producto','Precio','Cantidad')

        self.table.column('#0', minwidth=100,width=120,anchor='center')
        self.table.column('Nombre', minwidth=100, width=130, anchor='center')
        self.table.column('Tp_producto', minwidth=100, width=120, anchor='center')
        self.table.column('Precio', minwidth=100, width=120, anchor='center')
        self.table.column('Cantidad', minwidth=100, width=105, anchor='center')

        self.table.heading('#0', text='Codigo', anchor='center')
        self.table.heading('Nombre', text='Nombre', anchor='center')
        self.table.heading('Tp_producto', text='Tp_producto', anchor='center')
        self.table.heading('Precio', text='Precio', anchor='center')
        self.table.heading('Cantidad', text='Cantidad', anchor='center')

        estilo = ttk.Style(self.frame3)
        estilo.theme_use('alt')
        estilo.configure(".", font=('Helvetica',12,'bold'), foreground='red2')
        estilo.configure("Treeview", font=('Helvetica',10,'bold'), foreground='black', background='white')
        estilo.map('Treeview', background=[('selected', 'green2')], foreground=[('selected', 'black')])

        self.table.bind("<<TreeviewSelect>>", self.obtener_fila)

    def agregar_datos(self):
        self.table.get_children()
        codigo = self.codigo.get()
        nombre = self.nombre.get()
        tp_producto = self.tp_producto.get()
        precio = self.precio.get()
        cantidad = self.cantidad.get()
        datos = (nombre,tp_producto,precio,cantidad)
        if codigo and nombre and tp_producto and cantidad !='':
            self.table.insert('', 0, text= codigo, values=datos)
            self.base_datos.agregar_producto(codigo,nombre,tp_producto,precio,cantidad)

    def limpiar_datos(self):
        self.table.delete(*self.table.get_children())
        self.codigo.set('')
        self.nombre.set('')
        self.tp_producto.set('')
        self.precio.set('')
        self.cantidad.set('')

    def buscar_nombre(self):
        nombre_producto = self.buscar.get()
        nombre_producto = str("'" + nombre_producto + "'")
        nombre_buscado = self.base_datos.buscar_producto(nombre_producto)
        i =-1
        for dato in nombre_buscado:
            i +=1
            self.table.insert('',i, text=nombre_buscado[i][1:2], values=nombre_buscado[i][2:6])

    def mostrar_todo(self):
        self.table.delete(*self.table.get_children())
        registro = self.base_datos.mostrar_productos()
        i=-1
        for dato in registro:
            i +=1
            self.table.insert('', i, text= registro[i][1:2], values=registro[i][2:6])

    def eliminar_fila(self):
        fila = self.table.selection()
        if len(fila) !=0:
            self.table.delete(fila)
            nombre =("'" + str(self.nombre_borrar) + "'")
            self.base_datos.eliminar_produc(nombre)

    def obtener_fila(self, event):
        current_item = self.table.focus()
        if not current_item:
            return
        data = self.table.item(current_item)
        self.nombre_borrar = data['values'][0]

def main():

        try:
           ventana = Tk()
           ventana.wm_title("Registro de Producto en SQL Server")
           ventana.config(bg='gray22')
           ventana.geometry('900x500')
           ventana.resizable(0, 0)
           app = Registro(ventana)
           app.mainloop()
        except Exception as e:
         print("Error al abrir la ventana:", e)
    

if __name__=="__main__":

        main()