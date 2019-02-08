import numpy as np


class AsoRule():

    def __init__(self, data):
        # _______________________________________________
        # DataSet
        self.data = data
        # Rows
        self.rows = data.shape[0]
        # Columns
        self.columns = data.shape[1]
        # _______________________________________________

    def soporte(self):
        # Obtener la fecuencia de cada item
        ItemFreq = np.sum(self.data,0)
        # Devuelve la freq dividida entre el numero de transacciones
        return ItemFreq/self.rows

    def soporte_cond(self):
        supports = []
        # Realizamos una matriz que nos ayudará a sacar la confianza
        for i in range(self.rows):
            row = [0 for x in range(self.rows)]
            for j in range(i + 1, self.rows):
                for t in self.data:
                    if t[i] > 0 and t[j] > 0:
                        row[j] += 1
            supports.append([x / self.rows for x in row])

        # Se obtiene la matrix simétrica
        for i in range(self.rows):
            for j in range(i + 1, self.rows):
                supports[j][i] = supports[i][j]
        return np.array(supports)

    def confianza(self,soporte, soporte_condicional):
        # Se obtiene la confianza dividiendo el Soporte i para cara fila de
        # los soportes condicionales
        return soporte_condicional / soporte[:,None]

    def lift(self,soporte,soporte_condicional):
        lifts = []
        for i in range(self.columns):
            lift = []
            for j in range(self.columns):
                lf = soporte_condicional[i][j] / (soporte[i] * soporte[j])
                lift.append(lf)
            lifts.append(lift)
        return np.array(lifts)
