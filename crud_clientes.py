import pyodbc

# Detalles de conexión
servidor = 'DESKTOP-UGNVOKN\\SQLEXPRESS'
base_datos = 'PracticasDB'  # Nombre de tu base de datos

def conectar():
    conexion = pyodbc.connect(
        f'DRIVER={{SQL Server}};'
        f'SERVER={servidor};'
        f'DATABASE={base_datos};'
        'Trusted_Connection=yes;'
    )
    return conexion

def crear_cliente(nombre, email, telefono):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO Clientes (Nombre, Email, Telefono) VALUES (?, ?, ?)", (nombre, email, telefono))
    conexion.commit()
    print("Registro insertado con éxito.")
    conexion.close()

def leer_clientes():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Clientes")
    filas = cursor.fetchall()
    for fila in filas:
        print(f"Id: {fila.Id}, Nombre: {fila.Nombre}, Email: {fila.Email}, Teléfono: {fila.Telefono}, Fecha de Registro: {fila.FechaRegistro}")
    conexion.close()

def actualizar_cliente(id):
    conexion = conectar()
    cursor = conexion.cursor()
    
    # Obtener los datos actuales del cliente
    cursor.execute("SELECT Nombre, Email, Telefono FROM Clientes WHERE Id=?", (id,))
    cliente = cursor.fetchone()
    
    if not cliente:
        print("Cliente no encontrado.")
        conexion.close()
        return
    
    # Guardar los valores actuales
    nombre_actual, email_actual, telefono_actual = cliente
    
    # Solicitar nuevos valores o mantener los actuales
    nuevo_nombre = input(f"Nuevo nombre (actual: {nombre_actual}): ") or nombre_actual
    nuevo_email = input(f"Nuevo email (actual: {email_actual}): ") or email_actual
    nuevo_telefono = input(f"Nuevo teléfono (actual: {telefono_actual}): ") or telefono_actual
    
    # Ejecutar la actualización
    cursor.execute("UPDATE Clientes SET Nombre=?, Email=?, Telefono=? WHERE Id=?", 
                   (nuevo_nombre, nuevo_email, nuevo_telefono, id))
    conexion.commit()
    print("Registro actualizado con éxito.")
    
    conexion.close()



def eliminar_cliente(id):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM Clientes WHERE Id=?", (id,))
    conexion.commit()
    print("Registro eliminado con éxito.")
    conexion.close()

def menu():
    while True:
        print("\n--- Menú ---")
        print("1. Crear nuevo cliente")
        print("2. Leer todos los clientes")
        print("3. Actualizar cliente")
        print("4. Eliminar cliente")
        print("5. Salir")
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == '1':
            nombre = input("Nombre: ")
            email = input("Email: ")
            telefono = input("Teléfono: ")
            crear_cliente(nombre, email, telefono)
        elif opcion == '2':
            print("\nClientes actuales:")
            leer_clientes()
        elif opcion == '3':
            id = int(input("ID del cliente a actualizar: "))
            actualizar_cliente(id)
        elif opcion == '4':
            id = int(input("ID del cliente a eliminar: "))
            eliminar_cliente(id)
        elif opcion == '5':
            print("Saliendo...")
            break
        else:
            print("Opción no válida, por favor intenta de nuevo.")

# Ejecución del menú
if __name__ == "__main__":
    menu()
