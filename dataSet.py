import pandas as pd
import matplotlib.pyplot as plt# Visualización
import seaborn as sns# Visualización


# Cargar el archivo CSV en un DataFrame
df = pd.read_csv('archive\data.csv', encoding='ISO-8859-1')

# Mostrar las primeras filas para asegurarnos de que los datos se cargaron correctamente
# print(df.head())

# Información sobre las columnas, tipos de datos y valores faltantes
print(df.info())

# Resumen estadístico de los datos numéricos
print(df.describe())

# Verificar si hay duplicados
print(f"Duplicados: {df.duplicated().sum()}")

# Eliminar filas duplicadas si las hay
df = df.drop_duplicates()

# Verificar valores faltantes en las columnas
print(df.isnull().sum())

# Eliminar filas con valores nulos en 'CustomerID' o 'Description'
df = df.dropna(subset=['CustomerID', 'Description'])

# Convertir la columna 'InvoiceDate' a tipo datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Verificar nuevamente los valores nulos
print(df.isnull().sum())

# Top 10 productos más vendidos (por cantidad)
top_products = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)
print(top_products)

# Visualización
plt.figure(figsize=(10,5))
sns.barplot(x=top_products.values, y=top_products.index)
plt.title('Top 10 Productos Más Vendidos')
plt.xlabel('Cantidad Vendida')
plt.show()


# Crear una columna para el ingreso total por línea
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# Top 10 productos que más ingresos generaron
ingresos_por_producto = df.groupby('Description')['TotalPrice'].sum().sort_values(ascending=False).head(10)
print(ingresos_por_producto)

# Visualización
plt.figure(figsize=(10,5))
sns.barplot(x=ingresos_por_producto.values, y=ingresos_por_producto.index)
plt.title('Top 10 Productos con Mayor Ingreso')
plt.xlabel('Ingreso Total')
plt.show()
# Guardar los resultados de ingresos por producto en un CSV
ingresos_por_producto.to_csv('ingresos_por_producto.csv')

# Top 10 países con más transacciones
transacciones_por_pais = df['Country'].value_counts().head(10)
print(transacciones_por_pais)

# Visualización
plt.figure(figsize=(10,5))
sns.barplot(x=transacciones_por_pais.values, y=transacciones_por_pais.index)
plt.title('Top 10 Países con Más Transacciones')
plt.xlabel('Número de Transacciones')
plt.show()

