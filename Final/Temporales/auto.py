import random
class Auto:
    def __init__(self, rnd):
        if rnd < 0.60:
            self.tipo = "pequeño"
        elif rnd < 0.85:
            self.tipo = "grande"
        else:
            self.tipo = "utilitario"
        self.ubicacion = -1
        self.fin_estacionar = ""
        self.estado = ""
        self.tiempo = ""
        self.id = ""

    def asignar_lugar(self, box, reloj):
        self.ubicacion = box
        self.estado = "Estacionado"
        rnd = random.random()
        if rnd < 0.5:
            self.tiempo = 60
            self.fin_estacionar = reloj + 60
        elif rnd < 0.8:
            self.tiempo = 120
            self.fin_estacionar = reloj + 120
        elif rnd < 0.95:
            self.tiempo = 180
            self.fin_estacionar = reloj + 180
        else:
            self.tiempo = 240
            self.fin_estacionar = reloj + 240
        return rnd

    def total(self):
        if self.tipo == "pequeño":
            return (int(self.tiempo)/60) * 1
        elif self.tipo == "grande":
            return (int(self.tiempo)/60) * 1.2
        else:
            return (int(self.tiempo) / 60) * 1.5
