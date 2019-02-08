import numpy as np
import pandas as pd

from NonSupervised.AsoRule import AsoRule

#_______________________________________________________________________________________________________________________
#Leer el archivo con los datos en forma horizontal
data = pd.read_csv("data.csv")
print("Datos\n",data)
headers = np.array(data.columns)
#_______________________________________________________________________________________________________________________
# Convertir los datos a un nparray
data = np.array(data)
rules = AsoRule(data)
#_______________________________________________________________________________________________________________________
# Obtener soporte de cada item
soporte = rules.soporte()
print('\n',pd.DataFrame(soporte,index=headers,columns=['Soporte']))
#_______________________________________________________________________________________________________________________
# Obtener el soporte condicional  Soporte(Xi|Xj)
soporte_condicional = rules.soporte_cond()
print('\nSoporte Condicional\n',pd.DataFrame(soporte_condicional,index=headers,columns=headers))
#_______________________________________________________________________________________________________________________
# Obtener la confianza Confianza(Xi|Xj)
confianza = rules.confianza(soporte,soporte_condicional)
print("\nConfianza\n",pd.DataFrame(confianza,index=headers,columns=headers))
#_______________________________________________________________________________________________________________________
# Obtener el Lift de cada elemento
lift = rules.lift(soporte, soporte_condicional)
print("\nLifts\n",pd.DataFrame(lift,index=headers,columns=headers))


