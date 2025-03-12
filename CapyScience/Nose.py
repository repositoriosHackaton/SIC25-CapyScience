import tkinter as tkin
from tkinter import filedialog
import tensorflow as tf
from PIL import Image, ImageTk
import numpy as np

modelo = tf.keras.models.load_model("C:/Users/gusem/OneDrive/Desktop/Gustavo Rivas/Interfaz/Modelo_quelegustealuis.h5")


root = tkin.Tk()
root.title("Interfaz piloto")
root.resizable(False, False)
root.iconbitmap("C:/Users/gusem/OneDrive/Desktop/Gustavo Rivas/Interfaz/fuego.ico")

root.tk.call('source', 'Azure/azure.tcl')
root.tk.call('set_theme', 'dark')

root.geometry("800x550")

frame = tkin.Frame()
frame.pack(fill="none", anchor="center", expand="True")
frame.config(width="400", height="500")

imagen_label = tkin.Label(frame, bg="white")
imagen_label.place(bordermode="inside", x=3, y=50)

label = tkin.Label(frame, text="Inserte una imagen", font=("Arial", 20))
label.place(bordermode="inside", x = 60)

resultado_label = tkin.Label(frame, text="", font=("Arial", 20))
resultado_label.place(bordermode="inside", x=0, y=50)


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

def openFile():
    file = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=[("Archivos de imagen", "*.png"), ("Archivos de imagen", "*.jpg")])
    procesar_imagen(file)
    print(file)

button = tkin.Button(frame, text="Insertar", font=("Arial", 15), command= openFile)
button.place(bordermode="inside", x = 140, y = 410)

root.mainloop()