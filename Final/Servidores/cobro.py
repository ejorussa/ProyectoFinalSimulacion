class Cobro:
    def __init__(self, demora):
        self.atendiendo_a = None
        self.estado = "libre"
        self.recaudacion = 0
        self.fin_cobro = ""
        self.cola = []
        self.recaudado_p = 0
        self.recaudado_grande = 0
        self.recaudado_utiltario = 0
        self.demora = demora

    def atender(self, auto, reloj):
        if self.es_libre():
            self.estado = "ocupado"
            self.atendiendo_a = auto
            auto.estado = "siendo cobrado"
            self.fin_cobro = reloj + self.demora
            auto.fin_estacionar = ""


    def es_libre(self):
        if self.estado == "libre":
            return True
        else:
            return False

    def finalizar_cobro(self, reloj):
        self.fin_cobro = ""
        total = self.atendiendo_a.total()
        self.recaudacion += total
        if self.atendiendo_a.tipo == "pequeño":
            self.recaudado_p += total
        elif self.atendiendo_a.tipo == "grande":
            self.recaudado_grande += total
        else:
            self.recaudado_utiltario += total
        self.atendiendo_a.estado = "cobrado"
        self.atendiendo_a = None
        self.estado = "libre"
        if len(self.cola) > 0:
            self.atender(self.cola.pop(), reloj)


