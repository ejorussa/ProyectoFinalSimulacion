# This is a sample Python script.
import distribuciones
from Servidores.cobro import Cobro
from Servidores.estacionamiento import Estacionamiento
from Temporales.auto import Auto
import random
import pandas as pd
import tkinter as tk
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import openpyxl


def agregar_fila(valores, nombre):
    libro_excel = openpyxl.load_workbook(nombre + ".xlsx")
    hoja = libro_excel.active
    for fila in valores:
        hoja.append(fila)
    libro_excel.save(nombre + ".xlsx")


def sistema_estacionamiento(intervalo, hs_sim, media_llegada, de, nombre_excel, demora):
    df = pd.DataFrame([])
    df.to_excel(nombre_excel + ".xlsx")
    box = 0
    reloj = 0
    evento = "inicializacion"
    funcion = 1
    rnd_hs = ""
    tiempo_hs = ""
    estacionamiento = Estacionamiento()
    zona_cobro: Cobro = Cobro(demora)
    vector_txt_0 = ["", "", "llegada_cliente", "", "", "", "", "", "fin_estacionamiento_i", "", "", "", "", "", "", "",
                    "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                    "fin_cobro", "Playa", "", "", "", "", "Empleado Cobro", "", "", "", "", "", "", "", ""]
    vector_txt = ["evento", "reloj", "rnd tipo auto", "Tipo Auto", "rnd1", "rnd2", "tiempo", "proxima_llegada", "rnd",
                  "tiempo", "Fin1", "Fin2", "Fin3", "Fin4", "Fin5",
                  "Fin6", "Fin7", "Fin8", "Fin9", "Fin10", "Fin11", "Fin12", "Fin13", "Fin14", "Fin15", "Fin16",
                  "Fin17", "Fin18", "Fin19", "Fin20", "fin_cobro","Estado", "Lugares", "lugares_p", "lugares_g",
                  "lugares_u", "Estado", "Recaudacion",
                  "cola","ac_recaudado_pequeños", "ac_recaudado_grandes", "ac_recaudado_utilitarios",
                  "c_no_entraron_p", "c_no_entraron_g", "c_no_entraron_u"]  # me falto rnd  del
    auto_contador = 0
    utilitarios_c = 0
    pequeños_c = 0
    grandes_c = 0

    # calculo primera llegadaa
    rnd1 = rnd2 = ""
    rnd1, rnd2, tiempo_llegada, funcion = distribuciones.normal(rnd1, rnd2, media_llegada, de, funcion)
    proxima_llegada = reloj + tiempo_llegada
    rnd_tipo = tipo = ""
    # vector inicial
    vector_ini = [evento, reloj, rnd_tipo, tipo, rnd1, rnd2, tiempo_llegada, proxima_llegada, rnd_hs, tiempo_hs]
    autos = [""] * 20
    vector_fin = [zona_cobro.fin_cobro, estacionamiento.estado, estacionamiento.lugares(), estacionamiento.pequeños(),
                  estacionamiento.grandes(), estacionamiento.utilitarios(), zona_cobro.estado, zona_cobro.recaudacion]
    vector = vector_ini + autos + vector_fin

    # utilizado para ver proximo evento posteriormente
    llaves = 'Llegada cliente', "Fin Estacionamiento 1", "Fin Estacionamiento 2", "Fin Estacionamiento 3", "Fin Estacionamiento 4", "Fin Estacionamiento 5", "Fin Estacionamiento 6", "Fin Estacionamiento 7", "Fin Estacionamiento 8", "Fin Estacionamiento 9", "Fin Estacionamiento 10", "Fin Estacionamiento 11", "Fin Estacionamiento 12", "Fin Estacionamiento 13", "Fin Estacionamiento 14", "Fin Estacionamiento 15", "Fin Estacionamiento 16", "Fin Estacionamiento 17", "Fin Estacionamiento 18", "Fin Estacionamiento 19", "Fin Estacionamiento 20", "Fin de Cobro"
    indices = 7, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31

    # Definir la ruta y el nombre del archivo de Excel
    archivo_excel = nombre_excel + '.xlsx'

    c = 0
    autos = []
    datos = []
    # en caso de querer ver desde el inicio muestro la primer fila de inicializacion
    if intervalo == 0:
        datos.append(vector)
    autos_totales = 0
    identificador_auto = 1
    # Inicia la simulacion
    while reloj <= (hs_sim * 60):
        # Se verifica el próximo evento
        proximos = {}
        for j in range(22):
            if str(vector[indices[j]]) != "":
                proximos[llaves[j]] = (float(vector[indices[j]]))
        minimo = min(proximos.values())
        for nombre, valor in proximos.items():
            if valor == minimo:
                reloj, evento = minimo, nombre
                break
        # Separar el texto y el número en caso de fin estacionamiento i ya que necesito saber que box termina
        if evento != "Llegada cliente" and evento != "Fin de Cobro":
            palabras = evento.split()
            evento = " ".join(palabras[:-1])
            box = int(palabras[-1])

        if evento == "Llegada cliente":
            # Calculamos proxima llegada
            rnd1, rnd2, tiempo_llegada, funcion = distribuciones.normal(rnd1, rnd2, media_llegada, de, funcion)
            proxima_llegada = reloj + tiempo_llegada
            # auto que llega
            autos_totales += 1
            rnd_tipo = random.random()
            auto = Auto(rnd_tipo)
            # auto entra al estacionamiento solo si hay lugares de su tipo
            rnd_hs, entra = estacionamiento.recibir(auto, reloj)
            if entra:
                if intervalo > c:
                    # no puedo asegurar que estan en la sim entonces agrego para validar su estado, si pago se va del SI
                    autos.append(auto)
                elif intervalo <= c <= (intervalo + 500):
                    autos.append(auto)
                    # Modificación del vector cabecera para los clientes ya que estos efectivamente estan en la sim
                    vector_txt += ["Estado", "Tiempo", "Tipo", "Nro Estacionamiento"]
                    vector_txt_0 += [str(identificador_auto)]*4
                    identificador_auto += 1
            else:
                if auto.tipo == "pequeño":
                    pequeños_c += 1
                elif auto.tipo == "grande":
                    grandes_c += 1
                else:
                    utilitarios_c += 1

        elif evento == "Fin Estacionamiento":
            # Le pasamos el auto al cobro modificando los estados de los participantes
            estacionamiento.pasar_a_cobro(box - 1, zona_cobro, reloj)
            evento = "Fin Estacionamiento " + str(box)

        elif evento == "Fin de Cobro":
            # finalizamos el cobro del auto segun el tiempo que se estaciono y la zona cobro atiende al siguiente o se
            # libera
            zona_cobro.finalizar_cobro(reloj)

        # Me aseguro de mostrar los datos cuando corresponde
        if vector[2] == rnd_tipo:
            rnd_tipo = ""
        if vector[8] == rnd_hs:
            rnd_hs = ""
        if evento == "Llegada cliente":
            tipo = auto.tipo
            tiempo = auto.tiempo
        else:
            tipo = ""
            tiempo = ""
            tiempo_llegada = ""
        vector = [evento, reloj, rnd_tipo, tipo, rnd1, rnd2, tiempo_llegada, proxima_llegada, rnd_hs, tiempo] + \
                 estacionamiento.estado_lugares() + [zona_cobro.fin_cobro, estacionamiento.estado,
                                                     estacionamiento.lugares(), estacionamiento.pequeños(),
                                                     estacionamiento.grandes(), estacionamiento.utilitarios(),
                                                     zona_cobro.estado, zona_cobro.recaudacion, len(zona_cobro.cola),
                                                     round(zona_cobro.recaudado_p, 1),
                                                     round(zona_cobro.recaudado_grande, 1),
                                                     round(zona_cobro.recaudado_utiltario, 1),
                                                     pequeños_c, grandes_c, utilitarios_c]
        if funcion == 1:
            rnd1 = rnd2 = ""
            # Vacío las casillas para no repetir los RNDs y los tiempo_demora
            # Elimina el cliente en caso de que no está dentro del tiempo de simulación seleccionado
        if intervalo > c:
            for car in autos:
                if car.estado == "cobrado":
                    autos.remove(car)
        # acomodo la parte del excel para visualizar objetos de forma adecuada y una vez eliminados no mostrarlos
        if intervalo <= c < (intervalo + 500):
            for j in range(len(autos)):
                if autos[j] == 1 or autos[j].estado == "cobrado":
                    vector += ["", "", "", ""]
                    autos[j] = 1
                else:
                    vector += [autos[j].estado, autos[j].tiempo, autos[j].tipo]
                    if autos[j].tipo == "grande" or autos[j].tipo == "utilitario":
                        vector.append(autos[j].ubicacion + 2)
                    else:
                        vector.append(autos[j].ubicacion + 1)

            datos.append(vector)
        c += 1
    datos.insert(0, vector_txt)
    datos.insert(0, vector_txt_0)
    agregar_fila(datos, nombre_excel)
    print("Autos Totales: " + str(autos_totales))
    # Muestro el resultado de la metrica solicitada
    resultado.configure(text="En la hora: " + str(vector[1]) + " la recaudacion termino en: $" +
                             str(round(zona_cobro.recaudacion, 1)))

    # Calculo y muestro los graficos de las metricas que agregue
    etiquetas = ["Pequeños", "Grandes", "Utilitarios"]
    valores = [pequeños_c, grandes_c, utilitarios_c]
    print(valores)
    plt.bar(etiquetas, valores, color='b')
    plt.xlabel("Autos")
    plt.ylabel("Cantidades")
    plt.title("Grafico de autos que no estacionaron y se fueron")
    plt.savefig("grafico1.png", format="png")
    plt.close()
    imagen_nueva = Image.open("grafico1.png")
    imagen_nueva = imagen_nueva.resize((450, 350))
    imagen_nueva = ImageTk.PhotoImage(imagen_nueva)
    img.configure(image=imagen_nueva)
    img.image = imagen_nueva
    etiquetas2 = ["Pequeños", "Grandes", "Utilitarios"]
    valores2 = [round(zona_cobro.recaudado_p, 1), round(zona_cobro.recaudado_grande, 1), round(zona_cobro.recaudado_utiltario, 1)]
    print(valores2)
    plt.bar(etiquetas2, valores2, color='b')
    plt.xlabel("Autos")
    plt.ylabel("Montos")
    plt.title("Grafico de Monto recaudado por cada tipo de auto")
    plt.savefig("grafico.png", format="png")
    plt.close()
    imagen_nueva2 = Image.open("grafico.png")
    imagen_nueva2 = imagen_nueva2.resize((450, 350))
    imagen_nueva2 = ImageTk.PhotoImage(imagen_nueva2)
    img2.configure(image=imagen_nueva2)
    img2.image = imagen_nueva2
    print(vector)


if __name__ == '__main__':
    # Interfaz humilde
    ventana = tk.Tk()
    ventana.title("Inicio")
    ventana.configure(bg="white")
    ventana.geometry("1300x620+10+10")
    titulo_intervalo = tk.Label(ventana, text="Ingrese desde que simulacion desea ver informacion:", background="white")
    titulo_intervalo.pack()
    txt_nros_intervalo = tk.Entry(ventana)
    txt_nros_intervalo.pack()
    titulo_simulaciones = tk.Label(ventana, text="Ingrese la cantidad de horas a simular:", background="white")
    titulo_simulaciones.pack()
    txt_nros_simulaciones = tk.Entry(ventana)
    txt_nros_simulaciones.pack()
    titulo_media_llegada_clientes = tk.Label(ventana, text="Ingrese la media para el evento llegada_cliente:",
                                             background="white")
    titulo_media_llegada_clientes.pack()
    txt_media_llegada_clientes = tk.Entry(ventana)
    txt_media_llegada_clientes.pack()
    titulo_de_llegada_cliente = tk.Label(ventana, text="Ingrese la desviacion estandar para el evento llegada_cliente:",
                                         background="white")
    titulo_de_llegada_cliente.pack()
    txt_de_llegada = tk.Entry(ventana)
    txt_de_llegada.pack()

    titulo_demora = tk.Label(ventana, text="Ingrese tiempo demora coro:", background="white")
    titulo_demora.pack()
    txt_demora = tk.Entry(ventana)
    txt_demora.pack()

    titulo_nombre = tk.Label(ventana, text="Ingrese nombre para el Excel:", background="white")
    titulo_nombre.pack()
    txt_nombre = tk.Entry(ventana)
    txt_nombre.pack()

    btn_simular = tk.Button(ventana, text="Simular", command=lambda: sistema_estacionamiento(
        int(txt_nros_intervalo.get()), int(txt_nros_simulaciones.get()),int(txt_media_llegada_clientes.get()),
        int(txt_de_llegada.get()), txt_nombre.get(), int(txt_demora.get())))
    btn_simular.pack()
    resultado = tk.Label(ventana, text="En la hora: ........ la recaudacion termino en: ......", background="white")
    resultado.pack()
    imagen = Image.new("RGB", (400, 300), "white")
    imagen = ImageTk.PhotoImage(imagen)
    frame_imagen = tk.Frame(ventana)
    frame_imagen.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
    global img
    img = tk.Label(frame_imagen, image=imagen)
    img.pack(side=tk.LEFT, padx=10, pady=10)
    global img2
    img2 = tk.Label(frame_imagen, image=imagen)
    img2.pack(side=tk.RIGHT, padx=10, pady=10)

    ventana.mainloop()
