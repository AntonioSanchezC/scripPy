import pyodbc

# Detalles de conexión
servidor = 'DESKTOP-UGNVOKN\\SQLEXPRESS'
base_datos = 'PracticasDB'  # Nombre de tu base de datos

# Conexión a SQL Server
try:
    conexion = pyodbc.connect(
        f'DRIVER={{SQL Server}};'
        f'SERVER={servidor};'
        f'DATABASE={base_datos};'
        'Trusted_Connection=yes;'
    )

    print("Conexión exitosa")
    
    cursor = conexion.cursor()
    
    # Crear tabla Clientes (si no existe)
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Clientes' AND xtype='U')
    CREATE TABLE Clientes (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Nombre NVARCHAR(100),
        Email NVARCHAR(100),
        Telefono NVARCHAR(15),
        FechaRegistro DATETIME DEFAULT GETDATE()
    );
    """)
    conexion.commit()
    print("Tabla 'Clientes' creada con éxito.")

    # Insertar un registro en la tabla Clientes
    nombre = 'Juan Pérez'
    email = 'juan.perez@example.com'
    telefono = '123456789'
    
    cursor.execute("INSERT INTO Clientes (Nombre, Email, Telefono) VALUES (?, ?, ?)", (nombre, email, telefono))
    conexion.commit()
    print("Registro insertado con éxito.")

    # Consultar y mostrar los registros
    cursor.execute("SELECT * FROM Clientes")
    filas = cursor.fetchall()
    for fila in filas:
        print(f"Id: {fila.Id}, Nombre: {fila.Nombre}, Email: {fila.Email}, Teléfono: {fila.Telefono}, Fecha de Registro: {fila.FechaRegistro}")

except Exception as e:
    print("Error al conectar a la base de datos:", e)

finally:
    if 'conexion' in locals():
        conexion.close()
