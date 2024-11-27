"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    import pandas as pd
    import re
    
    # Leer el archivo de texto
    file_path = 'files/input/clusters_report.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Definir los encabezados
    headers = ['cluster', 'cantidad_de_palabras_clave', 'porcentaje_de_palabras_clave', 'principales_palabras_clave']
    
    # Procesar los datos
    data = []
    current_entry = None
    
    for line in lines[4:]:  # Ignorar encabezado
        if line.strip():  # Ignorar líneas vacías
            if re.match(r'^\s*\d+\s', line):  # Nueva fila comienza con un número
                if current_entry:  # Si hay una entrada previa, agregarla a los datos
                    data.append(current_entry)
                current_entry = re.split(r'\s{2,}', line.strip(), maxsplit=3)
                current_entry = [col.strip() for col in current_entry]
            else:  # Continuación de palabras clave
                current_entry[-1] += ' ' + line.strip()  # Concatenar texto adicional
    
    # Agregar la última entrada
    if current_entry:
        data.append(current_entry)
    
    # Formatear las palabras clave
    for entry in data:
        entry[-1] = re.sub(r'\s+', ' ', entry[-1])  # Eliminar espacios extra
        entry[-1] = entry[-1].replace(', ', ',').replace(' ,', ',').replace(',', ', ')  # Uniformar comas y espacios
    
    # Crear el DataFrame
    df = pd.DataFrame(data, columns=headers)
    
    # Ajustar los nombres de las columnas
    df.columns = [col.lower().replace(' ', '_') for col in df.columns]
    
    # Convertir columnas numéricas a sus tipos adecuados
    df['cluster'] = df['cluster'].astype(int)
    df['cantidad_de_palabras_clave'] = df['cantidad_de_palabras_clave'].astype(int)
    
    # Manejar la conversión de la columna porcentaje_de_palabras_clave
    df['porcentaje_de_palabras_clave'] = df['porcentaje_de_palabras_clave'].replace({',': '.'}, regex=True)  # Reemplazar coma por punto
    df['porcentaje_de_palabras_clave'] = df['porcentaje_de_palabras_clave'].str.strip('%').astype(float)
    
    # Limpiar la columna principales_palabras_clave: quitar espacios extras y asegurar formato
    df['principales_palabras_clave'] = df['principales_palabras_clave'].str.strip()  # Eliminar espacios al principio y final
    
    # Asegurar que las palabras clave están separadas por comas y un espacio después de cada coma
    df['principales_palabras_clave'] = df['principales_palabras_clave'].apply(lambda x: ', '.join([word.strip() for word in x.split(',')]))  # Asegurar espacio después de la coma
    
    # Eliminar cualquier punto final (si existe)
    df['principales_palabras_clave'] = df['principales_palabras_clave'].str.rstrip('.')  # Eliminar punto al final
    
    return df

   
if __name__ == "__main__":
    resultado = pregunta_01()
    if resultado is not None:
        print(resultado)
  

"""
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
