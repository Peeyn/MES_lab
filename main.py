import numpy as np
import math as mat


class Elem4:
    nE = 4
    n = 1 / mat.sqrt(3)
    pcE = np.array([-n, n, n, -n])
    pcN = np.array([-n, -n, n, n])
    dNdN = np.array([[0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0]])
    dNdE = np.array([[0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0]])
    dNdX = np.array([[0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0]])
    dNdY = np.array([[0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0]])
    detJ = [0.0, 0.0, 0.0, 0.0]
    jakob = np.array([[[0.0, 0.0], [0.0, 0.0]],
                      [[0.0, 0.0], [0.0, 0.0]],
                      [[0.0, 0.0], [0.0, 0.0]],
                      [[0.0, 0.0], [0.0, 0.0]]])
    jakob_odwr = np.array([[[0.0, 0.0], [0.0, 0.0]],
                           [[0.0, 0.0], [0.0, 0.0]],
                           [[0.0, 0.0], [0.0, 0.0]],
                           [[0.0, 0.0], [0.0, 0.0]]])
    globalneH = np.array([[[0.0, 0.0], [0.0, 0.0]],
                          [[0.0, 0.0], [0.0, 0.0]],
                          [[0.0, 0.0], [0.0, 0.0]],
                          [[0.0, 0.0], [0.0, 0.0]]])

    def __init__(self, elem_id, x0, x1, x2, x3, y0, y1, y2, y3):
        self.ID = elem_id
        self.x = np.array([x0, x1, x2, x3])
        self.y = np.array([y0, y1, y2, y3])
        self.suma_H = np.array([[0.0, 0.0, 0.0, 0.0],
                                [0.0, 0.0, 0.0, 0.0],
                                [0.0, 0.0, 0.0, 0.0],
                                [0.0, 0.0, 0.0, 0.0]])
        self.lokalneH = np.array([[[0.0, 0.0], [0.0, 0.0]],
                                  [[0.0, 0.0], [0.0, 0.0]],
                                  [[0.0, 0.0], [0.0, 0.0]],
                                  [[0.0, 0.0], [0.0, 0.0]]])

    def pochodne(self):
        for x in range(self.nE):
            wsp = 0.25
            self.dNdE[x, 0] = wsp * (1 - self.pcN[x])
            self.dNdE[x, 1] = -wsp * (1 - self.pcN[x])
            self.dNdE[x, 2] = -wsp * (1 + self.pcN[x])
            self.dNdE[x, 3] = wsp * (1 + self.pcN[x])

            self.dNdN[x, 0] = wsp * (1 - self.pcE[x])
            self.dNdN[x, 1] = wsp * (1 + self.pcE[x])
            self.dNdN[x, 2] = -wsp * (1 + self.pcE[x])
            self.dNdN[x, 3] = -wsp * (1 - self.pcE[x])

    def jakobian(self):
        dXdE = 0.0
        dYdE = 0.0
        dXdN = 0.0
        dYdN = 0.0

        # jakobian
        for x in range(self.nE):
            for y in range(4):
                dXdE += self.dNdE[x, y] * -self.x[y]
                dXdN += self.dNdN[x, y] * -self.x[y]
                dYdE += self.dNdE[x, y] * -self.y[y]
                dYdN += self.dNdN[x, y] * -self.y[y]
            self.jakob[x, 0, 0] = dXdE
            self.jakob[x, 0, 1] = dXdN
            self.jakob[x, 1, 0] = dYdE
            self.jakob[x, 1, 1] = dYdN
            dXdE = 0.0
            dXdN = 0.0
            dYdE = 0.0
            dYdN = 0.0
            # jakobian odwrócony:
            for x in range(self.nE):
                self.jakob_odwr[x, 0, 0] = self.jakob[x, 1, 1]
                self.jakob_odwr[x, 0, 1] = self.jakob[x, 1, 0]
                self.jakob_odwr[x, 1, 0] = self.jakob[x, 0, 1]
                self.jakob_odwr[x, 1, 1] = self.jakob[x, 0, 0]

            # wyznacznik
            for x in range(self.nE):
                self.detJ[x] = self.jakob[x, 0, 0] * self.jakob[x, 1, 1] - self.jakob[x, 0, 1] * self.jakob[
                    x, 1, 0]

    def pochodne2(self):
        for x in range(self.nE):
            # print("\nPunkt", x, ":")
            for y in range(4):
                self.dNdX[x, y] = -(1 / self.detJ[x]) * (
                        self.jakob_odwr[x, 0, 0] * self.dNdE[x, y] + self.jakob_odwr[x, 0, 1] * self.dNdN[x, y])
                # print(y, "dN/dX=", self.dNdX[x, y])
                self.dNdY[x, y] = -(1 / self.detJ[x]) * (
                        self.jakob_odwr[x, 1, 0] * self.dNdE[x, y] + self.jakob_odwr[x, 1, 1] * self.dNdN[x, y])
                # print(y, "dN/dY=", self.dNdY[x, y])

    def macierzH(self):
        dNdXdNdXT = np.array(
            [[[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]],
             [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]],
             [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]],
             [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]])
        dNdYdNdYT = np.array(
            [[[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]],
             [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]],
             [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]],
             [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]])

        for x in range(self.nE):
            for y in range(4):
                for z in range(4):
                    dNdXdNdXT[x, y, z] = self.dNdX[x, y] * self.dNdX[x, z]
                    dNdYdNdYT[x, y, z] = self.dNdY[x, y] * self.dNdY[x, z]

        # suma dN/dX*dN/dX + dN/dY*dN/dY
        suma_ilocz = np.array(
            [[[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]],
             [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]],
             [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]],
             [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]])
        for x in range(self.nE):
            for y in range(4):
                for z in range(4):
                    suma_ilocz[x, y, z] = dNdYdNdYT[x, y, z] + dNdXdNdXT[x, y, z]
        # print("\nSuma iloczynów:\n", suma_ilocz)

        # pojedyncze macierze
        wsp_K = 25.0
        H = np.array(
            [[[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]],
             [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]],
             [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]],
             [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]])
        for x in range(self.nE):
            for y in range(4):
                for z in range(4):
                    H[x, y, z] = wsp_K * suma_ilocz[x, y, z] * self.detJ[x]

        # print("\nMacierze H:\n", H)
        # macierz główna H:
        for x in range(self.nE):
            for y in range(4):
                self.suma_H[x, y] = 0
                for z in range(4):
                    self.suma_H[x, y] += H[z, x, y]

        # print("Element " + str(self.ID) + ", suma macierzy H: " + "\n", self.suma_H)
        return self.suma_H

    # def agregacja(self):
    #    self.suma_H

    pass


class SOE:
    def __init__(self, nE):
        self.globalneH = np.zeros(shape=(nE * nE, nE * nE))
        print("nE: ", nE)
        przejsc = nE * nE
        #wiersze:
        for k in range(przejsc):
            #self.globalneH[x]=x
            #kolumny:
            for i in range(przejsc):
                #self.globalneH[x,y]=y
                #wartości:
                for j in range(przejsc):
                    self.globalneH[x,y] = z
        print(self.globalneH)


mes0 = Elem4(1, 0.0, 0.033333, 0.0333, 0.0, 0.0, 0.0, 0.0333, 0.0333)
print("x =", mes0.x, "y =", mes0.y, "\nMacierz H:")
mes0.pochodne()
mes0.jakobian()
mes0.pochodne2()
mes0.macierzH()
h0 = mes0.suma_H
print(h0)

gg = SOE(4)
#print(gg.globalneH)

# agregacja:
# for i in range(4):
#    x = mes0.x[0]
