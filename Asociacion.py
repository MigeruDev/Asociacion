from collections import defaultdict
import numpy as np # linear algebra
# Hallar el soporte, la confianza y el lift

# Abrir y leer el archivo que contiene las transacciones de manera horizontal
# path: String que indica la ubicación del archivo con las transacciones
# data: Matriz donde se guardará las transacciones
# headers: Nombres de items
def read_data_h(path, data, headers, delimiter = ',', hasHeaders = True, hasColID = True):
    file = open(path, 'r')
    # Cabeceras
    if hasHeaders:
        line = file.readline()[:-1]
        head = line.split(delimiter) if \
            not hasColID else line.split(delimiter)[1:]
        for x in head:
            headers.append(x)
    
    # Guardar las transacciones
    for line in file:
        t = line[:-1].split(delimiter) if \
            not hasColID else line[:-1].split(delimiter)[1:]
        data.append([int(x) for x in t])    

def transform_dict(data, headers, items, n):
    # Número de transacciones
    nt = len(items)
    # Creación de la matriz donde se guardan las transacciones
    for _ in range(int(n)):
        data.append([0] * nt)

    for k in items.keys():
        headers.append(k)

    for k in range(len(headers)):
        for it in items[headers[k]]:
            data[it-1][k] = 1

def read_data_v(path, data, headers, delimiter = ',', hasHeaders = True):
    file = open(path, 'r')
    items = defaultdict(list)

    # Leer las cabeceras, en este caso no son necesarias,
    # pero es otro método para hallar las cabeceras
    if hasHeaders:
        file.readline()

    item = []
    # Guardar en un diccionario las posiciones de todos los items
    for line in file:
        item = line[:-1].split(delimiter)
        items[item[1]].append(int(item[0]))

    transform_dict(data, headers, items, item[0])

def read_data_l(path, data, headers, delimiter = ',', hasColID = False):
    file = open(path, 'r')
    items = defaultdict(list)

    nt = 1
    # Guardar en un diccionario las posiciones de todos los items
    for line in file:
        _items = line[:-1].split(delimiter) if \
            not hasColID else line.split(delimiter)[1:]
        for item in _items:
            items[item].append(nt)
        nt += 1

    transform_dict(data, headers, items, nt - 1)

# Función para calcular los soportes individuales
def get_support(data, support):
    for t in data:
        for i in range(len(support)):
            support[i] += t[i]
    for i in range(len(support)):
        support[i] /= len(data)

# Función para calcular los soportes entre todos los elementos
def get_supports(data, supports, n):
    # Realizamos una matriz que nos ayudará a sacar la confianza
    for i in range(n):
        row = [0 for x in range(n)]
        for j in range(i+1,n):
            for t in data:
                if t[i] > 0 and t[j] > 0:
                    row[j] += 1
        supports.append([x/n for x in row])

    for i in range(n):
        for j in range(i+1,n):
            supports[j][i] = supports[i][j]

# Función para calcular los soportes con antecedentes y consecuentes específicos del usuario
def get_custom_support(data, n, antecedente, consecuente = None):
    indices = antecedente + consecuente \
        if consecuente else antecedente
    coincidences = 0
    for t in data:
        v = True
        for i in indices:
            if t[i] == 0:
                v = False
                break
        coincidences = coincidences + 1 \
            if v else coincidences
    return coincidences / n

# Función para calcular la confianza entre antecedentes y consecuentes específicos del usuario
def get_custom_confidence(data, n, antecedente, consecuente):
    return get_custom_support(data, n, antecedente, consecuente) /\
        get_custom_support(data, n, antecedente)

# Función para calcular las confianzas entre todos los elementos
def get_confidences(confidences, support, supports):
    for i in range(len(support)):
        confidence = []
        for j in range(len(support)):
            confidence.append(supports[i][j]/support[i])
        confidences.append(confidence)

# Función para calcular los lifts entre todos los elementos
def get_lifts(lifts, support, supports):
    for i in range(len(support)):
        lift = []
        for j in range(len(support)):
            lf = supports[i][j]/(support[i]*support[j])
            lift.append(lf)
        lifts.append(lift)

if __name__ == "__main__":
    # String que indica la ubicación del archivo con las transacciones
    path = "datos.csv"
    # data: Matriz donde se guardará las transacciones
    data = []
    # Nombres de los items
    headers = []
    # Lista de soportes individuales
    support = []
    # Matriz de soportes entre items
    supports = []
    # Matriz de confianzas entre items
    confidences = []
    # Matriz de Lifts entre items
    lifts = []

    # leer y guardar los datos de los archivos
    read_data_h(path, data, headers)
    # verificar el tamaño de las cabeceras
    support = [0 for x in range(len(headers))] \
        if headers else [0 for x in range(len(data[0]))]

    # hallar el soporte para cada item
    get_support(data, support)
    print("Support\n",support)
    # hallar la matriz de soportes entre cada item
    get_supports(data, supports, len(headers))
    print("Supports\n",np.array(supports))
    # hallar la confianza entre cada unos de los items
    get_confidences(confidences, support, supports)
    print("Confidences\n",np.array(confidences))
    # hallar los Lifts entre los items
    get_lifts(lifts, support, supports)
    print("Lifts\n",np.array(lifts))
    # hallar el soporte para un antecedente y una consecuencia específica
    cc = get_custom_confidence(data, len(headers), [headers.index('B'), headers.index('C')], [headers.index('E')])

    data = []
    headers = []
    read_data_l('Lista.csv', data, headers, delimiter=';')
    print("Datos\n",np.array(data))

