import tkinter as tk
from tkinter import messagebox, scrolledtext
import os

ARCHIVO = "contactos.txt"

class GestorContactos:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Contactos")
        self.root.geometry("500x550")

        # Sección de entrada de datos
        frame = tk.LabelFrame(root, text="Registrar contacto")
        frame.pack(padx=10, pady=10, fill="x")

        tk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky="e")
        tk.Label(frame, text="Teléfono:").grid(row=1, column=0, sticky="e")
        tk.Label(frame, text="Email:").grid(row=2, column=0, sticky="e")

        self.entry_nombre = tk.Entry(frame, width=30)
        self.entry_telefono = tk.Entry(frame, width=30)
        self.entry_email = tk.Entry(frame, width=30)

        self.entry_nombre.grid(row=0, column=1, pady=3)
        self.entry_telefono.grid(row=1, column=1, pady=3)
        self.entry_email.grid(row=2, column=1, pady=3)

        tk.Button(frame, text="Guardar contacto", command=self.guardar_contacto).grid(row=3, columnspan=2, pady=10)

        # Sección de búsqueda y eliminación
        frame2 = tk.LabelFrame(root, text="Buscar / Eliminar contacto")
        frame2.pack(padx=10, pady=10, fill="x")

        tk.Label(frame2, text="Nombre a buscar:").grid(row=0, column=0, sticky="e")
        self.entry_buscar = tk.Entry(frame2, width=30)
        self.entry_buscar.grid(row=0, column=1, pady=5)

        tk.Button(frame2, text="Buscar", command=self.buscar_contacto).grid(row=1, column=0, pady=5)
        tk.Button(frame2, text="Eliminar", command=self.eliminar_contacto).grid(row=1, column=1, pady=5)
        tk.Button(frame2, text="Mostrar todos", command=self.mostrar_todos).grid(row=2, columnspan=2, pady=5)

        # Mostramos el área de resultado
        self.resultado = scrolledtext.ScrolledText(root, width=60, height=15)
        self.resultado.pack(padx=10, pady=10)

    def guardar_contacto(self):
        nombre = self.entry_nombre.get().strip()
        telefono = self.entry_telefono.get().strip()
        email = self.entry_email.get().strip()

        if not nombre or not telefono or not email:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return

        with open(ARCHIVO, "a", encoding="utf-8") as archivo:
            archivo.write(f"{nombre},{telefono},{email}\n")

        messagebox.showinfo("Contacto guardado", f"Se guardó el contacto de {nombre}.")
        self.entry_nombre.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)

    def buscar_contacto(self):
        nombre = self.entry_buscar.get().strip().lower()
        encontrado = False
        self.resultado.delete(1.0, tk.END)

        if not os.path.exists(ARCHIVO):
            messagebox.showinfo("Sin datos", "No hay contactos registrados aún.")
            return

        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split(",")
                if nombre in datos[0].lower():
                    self.resultado.insert(tk.END, f"Nombre: {datos[0]}\nTeléfono: {datos[1]}\nEmail: {datos[2]}\n\n")
                    encontrado = True

        if not encontrado:
            self.resultado.insert(tk.END, "Contacto no encontrado.\n")

    def eliminar_contacto(self):
        nombre = self.entry_buscar.get().strip().lower()
        eliminado = False
        nuevas_lineas = []

        if not os.path.exists(ARCHIVO):
            messagebox.showinfo("Sin datos", "No hay contactos para eliminar.")
            return

        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split(",")
                if nombre in datos[0].lower():
                    respuesta = messagebox.askyesno("Confirmar eliminación", 
                        f"¿Deseas eliminar este contacto?\n\nNombre: {datos[0]}\nTeléfono: {datos[1]}\nEmail: {datos[2]}")
                    if respuesta:
                        eliminado = True
                        continue
                nuevas_lineas.append(linea)

        with open(ARCHIVO, "w", encoding="utf-8") as archivo:
            archivo.writelines(nuevas_lineas)

        if eliminado:
            messagebox.showinfo("Eliminado", "El contacto fue eliminado.")
            self.resultado.delete(1.0, tk.END)
        else:
            messagebox.showinfo("No encontrado", "No se encontró un contacto que coincida.")

    def mostrar_todos(self):
        self.resultado.delete(1.0, tk.END)

        if not os.path.exists(ARCHIVO):
            self.resultado.insert(tk.END, "No hay contactos registrados.")
            return

        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()

            if not lineas:
                self.resultado.insert(tk.END, "No hay contactos registrados.")
                return

            for linea in lineas:
                datos = linea.strip().split(",")
                if len(datos) == 3:
                    self.resultado.insert(
                        tk.END,
                        f"Nombre: {datos[0]}\nTeléfono: {datos[1]}\nEmail: {datos[2]}\n\n"
                    )


# Ejecutamos la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = GestorContactos(root)
    root.mainloop()
