# generowanie wierzcholkow siatki
class Node(object):
    width = 2  # (x, y)

    def __init__(self, globalObj):
        self.height = globalObj.nNodes
        self.nodes = np.zeros((self.height, self.width), dtype=float)

        x, y, nr_wierzcholka = 0, 0, 0
        delta_x = globalObj.Height / globalObj.nNodesH
        delta_y = globalObj.Width / globalObj.nNodesW

        for i in range(globalObj.nNodesW):
            x = i * delta_x

            for j in range(globalObj.nNodesH):
                y = j * delta_y
                self.nodes[nr_wierzcholka, 0] = x
                self.nodes[nr_wierzcholka, 1] = y
                nr_wierzcholka += 1

#odczyt z pliku
class GlobalData(object):

    def __init__(self, filepath):
        self.Wysokosc = 0
        self.Szerokosc = 0
        self.wzWysokosc = 0
        self.wzSzerokosc = 0
        self.l_elem = 0
        self.l_wezlow = 0

        try:
            with open(filepath, 'r') as file:
                x = file.readlines()
            #wysokosc
            self.Wysokosc = float(x[0])
            #szerokosc
            self.Szerokosc = float(x[1])
            #wezlow na wyskosc
            self.wzWysokosc = int(x[2])
            #wezlow na szerokosc
            self.wzSzerokosc = int(x[3])

        except (TypeError, FileNotFoundError) as err:
            print("Occured:", err)

        finally:
            file.close()

        #obliczenie oglolnej liczby wezlow i elementow
        self.l_elem = int((self.wzWysokosc - 1) * (self.wzSzerokosc - 1))
        self.l_wezlow = int(self.wzWysokosc * self.wzSzerokosc)

