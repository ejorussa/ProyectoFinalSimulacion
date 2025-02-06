class Cola:
    def __init__(self):
        self.lugares_pequeños = ["libre"]*10
        self.lugares_grandes = ["libre"]*6
        self.lugares_utilitarios = ["libre"]*4
    def lugares(self):
        return self.pequeños() + self.grandes() + self.utilitarios()
    def pequeños(self):
        c = 0
        for i in range(10):
            if self.lugares_pequeños[i] != "libre":
                c += 1
        return 10 - c
    def grandes(self):
        c = 0
        for i in range(6):
            if self.lugares_grandes[i] != "libre":
                c += 1
        return 6 - c
    def utilitarios(self):
        c = 0
        for i in range(4):
            if self.lugares_utilitarios[i] != "libre":
                c += 1
        return 4 - c
