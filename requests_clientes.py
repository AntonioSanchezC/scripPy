import requests
import pyodbc

# Detalles de conexión
servidor = 'DESKTOP-UGNVOKN\\SQLEXPRESS'  # Cambia por tu servidor SQL Server
base_datos = 'PracticasDB'  # Cambia por tu base de datos

# Conexión a SQL Server
try:
    conexion = pyodbc.connect(
        f'DRIVER={{SQL Server}};'
        f'SERVER={servidor};'
        f'DATABASE={base_datos};'
        'Trusted_Connection=yes;'
    )
    cursor = conexion.cursor()
    print("Conexión exitosa a la base de datos")
    
    # Verificar si la tabla 'posts' ya existe
    cursor.execute('''
    SELECT COUNT(*) 
    FROM sysobjects 
    WHERE name='posts' AND xtype='U'
    ''')
    
    existe_tabla = cursor.fetchone()[0]  # Devuelve 1 si existe, 0 si no

    if existe_tabla:
        # URL del API
        url = "https://jsonplaceholder.typicode.com/posts"

        # Hacer la solicitud GET
        response = requests.get(url)

        # Verificar que la solicitud fue exitosa
        if response.status_code == 200:
            data = response.json()  # Convertir la respuesta a JSON

            
            try:
                insertados = 0  # Contador de registros insertados
                omitidos = 0  # Contador de registros omitidos
                ids_insertados = []  # Lista para almacenar los IDs de registros insertados
                ids_omitidos = []  # Lista para almacenar los IDs de registros omitidos
                
                for post in data:
                # Verificar si el ID ya existe en la base de datos
                
                    cursor.execute('SELECT COUNT(*) FROM posts WHERE id = ?', post['id'])
                    id_existe = cursor.fetchone()[0]  # Devuelve 1 si el id ya existe

                    if not id_existe:

                        cursor.execute('''
                        INSERT INTO posts (id, userId, title, body)
                        VALUES (?, ?, ?, ?)
                        ''', (post['id'], post['userId'], post['title'], post['body']))
                        ids_insertados.append(post['id'])  # Almacenar el ID insertado
                        insertados += 1
                    else:
                        ids_omitidos.append(post['id'])  # Almacenar el ID omitido
                        omitidos += 1


                # Guardar los cambios
                conexion.commit()
                # Mensaje final con detalles
                print(f"Datos insertados correctamente: {insertados} registro(s).")
                if ids_insertados:
                    print(f"IDs de los registros insertados: {ids_insertados}")

                print(f"Registros omitidos por existir antes de usar la aplicacion: {omitidos} registro(s).")
                if ids_omitidos:
                    print(f"IDs de los registros omitidos: {ids_omitidos}")

            except Exception as e:
                print("Error al insertar datos:", e)
        else:
            print("Error al obtener los datos:", response.status_code)



    else:
        # Crear la tabla si no existe
        cursor.execute('''
        CREATE TABLE posts (
            id INT PRIMARY KEY,
            userId INT,
            title NVARCHAR(255),
            body NVARCHAR(MAX)
        )
        ''')
        conexion.commit()
        print("Tabla 'posts' creada exitosamente, vuelva a iniicar el programa para insertar los datos de la url en la base de datos PracticasBD")

except Exception as e:
    print("Error al conectar con la base de datos:", e)

finally:
    # Cerrar la conexión si existe
    if 'conexion' in locals():
        conexion.close()
