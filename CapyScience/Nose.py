import tkinter as tkin
from tkinter import filedialog
import tensorflow as tf
from PIL import Image, ImageTk, ImageGrab
import numpy as np
from tkintermapview import TkinterMapView

modelo = tf.keras.models.load_model("C:/Users/gusem/OneDrive/Desktop/Gustavo Rivas/Interfaz/Pushear/SIC25-CapyScience/CapyScience/Modelo_quelegustealuis.h5")

def mostrar_resultado(resultado):
    resultado_label.config(text=f"Resultado: {resultado}", font=("Arial", 10))


def clasificar_imagen(imagen_array):
    prediccion = modelo.predict(imagen_array)
    print("Predicción:", prediccion)
    result = max(prediccion[0])
    if result == prediccion[0][0]:
        prediccion = "No WildFire"
    else:
        prediccion = "WildFire"
    mostrar_resultado(prediccion)

def mostrar_imagen(ruta_imagen):
    imagen = Image.open(ruta_imagen).resize((350, 350))  
    imagen_tk = ImageTk.PhotoImage(imagen)  
    imagen_label.config(image=imagen_tk)
    imagen_label.image = imagen_tk

def procesar_imagen(ruta_imagen):
    mostrar_imagen(ruta_imagen)
    imagen = Image.open(ruta_imagen).resize((350, 350)) 
    imagen_array = np.array(imagen) / 255.0  
    imagen_array = np.expand_dims(imagen_array, axis=0)
    clasificar_imagen(imagen_array)

def capturar_imagen():
    x = root.winfo_rootx() + mapFrame.winfo_x()
    y = root.winfo_rooty() + mapFrame.winfo_y()
    x1 = x + mapFrame.winfo_width()
    y1 = y + mapFrame.winfo_height()
    ImageGrab.grab().crop((x, y, x1, y1)).save("captura.jpg")
    print("Imagen capturada y guardada como captura.jpg")
    procesar_imagen("captura.jpg")

def openFile():
    file = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=[("Archivos de imagen", "*.png"), ("Archivos de imagen", "*.jpg")])
    procesar_imagen(file)
    print(file)


#Ventana


root = tkin.Tk()
root.title("Interfaz piloto")
root.resizable(False, False)
root.iconbitmap("C:/Users/gusem/OneDrive/Desktop/Gustavo Rivas/Interfaz/Pushear/SIC25-CapyScience/CapyScience/fuego.ico")

root.tk.call('source', 'C:/Users/gusem/OneDrive/Desktop/Gustavo Rivas/Interfaz/Pushear/SIC25-CapyScience/CapyScience/Azure/azure.tcl')
root.tk.call('set_theme', 'dark')

root.geometry("980x600")

frame = tkin.Frame(root)
frame.grid(row=1, column=0, padx=30,ipady=5)
frame.grid_propagate(False)
frame.config(width="400", height="400")
frame.config(bg = 'black')

button = tkin.Button(root, text="Insertar", font=("Arial", 15), command=openFile)
button.grid(row=2, column=0, pady=10)


mapFrame = tkin.Frame()
mapFrame.grid(row=0, column=1, padx=30, rowspan=2)
mapFrame.grid_propagate(False)
mapFrame.config(width="450", height="450")
mapFrame.config(bg = 'gray')

captureButton = tkin.Button(root, text="Capturar", font=("Arial", 15), command=capturar_imagen)
captureButton.grid(row=2, column=1)

map_widget = TkinterMapView(mapFrame, width=450, height=450)
map_widget.set_tile_server("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}")
map_widget.set_position(6.42375, -66.58973)  # Coordenadas de ejemplo (India)
map_widget.set_zoom(5)
map_widget.pack()

label = tkin.Label(root, text="Inserte una imagen", font=("Arial", 20))
label.grid(row=0, column=0, sticky="n", pady=20)

resultado_label = tkin.Label(frame, text="", font=("Arial", 10))
resultado_label.grid(row=0, column=0, sticky="w")
resultado_label.config(bg="black")

imagen_label = tkin.Label(frame)
imagen_label.grid(row=1, column=0, padx=23, pady=10, sticky="nsew")
imagen_label.config(bg="black")


root.mainloop()