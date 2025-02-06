from Servidores.cola import Cola


class Estacionamiento:
    def __init__(self):
        self.cola = Cola()
        self.listos = []
        self.disponibles = ["pequeños", "grandes", "utilitarios"]
        self.estado = "Hay Lugares:" + str(self.disponibles)

    def lugares(self):
        return self.cola.lugares()

    def pequeños(self):
        return self.cola.pequeños()

    def grandes(self):
        return self.cola.grandes()

    def utilitarios(self):
        return self.cola.utilitarios()

    def recibir(self, auto, reloj):
        if auto.tipo == "pequeño":
            if self.pequeños() > 0:
                for i in range(10):
                    if self.cola.lugares_pequeños[i] == "libre":
                        self.cola.lugares_pequeños[i] = auto
                        self.actualizar_pequeño()
                        rnd = auto.asignar_lugar(i, reloj)
                        return rnd, True
        elif auto.tipo == "grande":
            if self.grandes() > 0:
                for i in range(6):
                    if self.cola.lugares_grandes[i] == "libre":
                        self.cola.lugares_grandes[i] = auto
                        self.actualizar_grande()
                        rnd = auto.asignar_lugar(i + 9, reloj)
                        return rnd, True
        elif auto.tipo == "utilitario":
            if self.utilitarios() > 0:
                for i in range(4):
                    if self.cola.lugares_utilitarios[i] == "libre":
                        self.cola.lugares_utilitarios[i] = auto
                        self.actualizar_utilitario()
                        rnd = auto.asignar_lugar(i + 15, reloj)
                        return rnd, True
        return "", False

    def pasar_a_cobro(self, box, cobrador, reloj):
        if box < 10:
            if cobrador.es_libre():
                cobrador.atender(self.cola.lugares_pequeños[box], reloj)
                self.cola.lugares_pequeños[box] = "libre"
                self.actualizar_pequeño()
            else:
                self.cola.lugares_pequeños[box].estado = "Esperando cobro"
                cobrador.cola.insert(0, self.cola.lugares_pequeños[box])
                self.cola.lugares_pequeños[box] = "libre"
                self.actualizar_pequeño()
        elif box < 16:
            if cobrador.es_libre():
                cobrador.atender(self.cola.lugares_grandes[box - 10], reloj)
                self.cola.lugares_grandes[box - 10] = "libre"
                self.actualizar_grande()
            else:
                self.cola.lugares_grandes[box - 10].estado = "Esperando cobro"
                cobrador.cola.insert(0, self.cola.lugares_grandes[box - 10])
                self.cola.lugares_grandes[box - 10] = "libre"
                self.actualizar_grande()
        elif box < 20:
            if cobrador.es_libre():
                cobrador.atender(self.cola.lugares_utilitarios[box - 16], reloj)
                self.cola.lugares_utilitarios[box - 16] = "libre"
                self.actualizar_utilitario()
            else:
                self.cola.lugares_utilitarios[box - 16].estado = "Esperando cobro"
                cobrador.cola.insert(0, self.cola.lugares_utilitarios[box - 16])
                self.cola.lugares_utilitarios[box - 16] = "libre"
                self.actualizar_utilitario()

    def estado_lugares(self):
        v = []
        for i in range(10):
            if self.cola.lugares_pequeños[i] == "libre":
                v.append("")
            else:
                v.append(self.cola.lugares_pequeños[i].fin_estacionar)
        for i in range(6):
            if self.cola.lugares_grandes[i] == "libre":
                v.append("")
            else:
                v.append(self.cola.lugares_grandes[i].fin_estacionar)
        for i in range(4):
            if self.cola.lugares_utilitarios[i] == "libre":
                v.append("")
            else:
                v.append(self.cola.lugares_utilitarios[i].fin_estacionar)
        return v

    def actualizar_pequeño(self):
        if self.pequeños() == 0:
            if "pequeños" in self.disponibles:
                self.disponibles.remove("pequeños")
                self.estado = "Hay Lugares:" + str(self.disponibles)
        elif not ("pequeños" in self.disponibles):
            self.disponibles.insert(0, "pequeños")
            self.estado = "Hay Lugares:" + str(self.disponibles)
        if self.pequeños() == self.utilitarios() == self.grandes() == 0:
            self.estado = "lleno"

    def actualizar_grande(self):
        if self.grandes() == 0:
            if "grandes" in self.disponibles:
                self.disponibles.remove("grandes")
                self.estado = "Hay Lugares:" + str(self.disponibles)
        elif not ("grandes" in self.disponibles):
            self.disponibles.insert(0, "grandes")
            self.estado = "Hay Lugares:" + str(self.disponibles)
        if self.pequeños() == self.utilitarios() == self.grandes() == 0:
            self.estado = "lleno"

    def actualizar_utilitario(self):
        if self.utilitarios() == 0:
            if "utilitarios" in self.disponibles:
                self.disponibles.remove("utilitarios")
                self.estado = "Hay Lugares: " + str(self.disponibles)
        elif not ("utilitarios" in self.disponibles):
            self.disponibles.insert(0, "utilitarios")
            self.estado = "hay disponibles lugares: " + str(self.disponibles)
        if self.pequeños() == self.utilitarios() == self.grandes() == 0:
            self.estado = "lleno"



