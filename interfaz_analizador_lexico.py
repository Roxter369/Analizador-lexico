import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# Tokens del lenguaje
palabras_reservadas = ['entero', 'decimal', 'booleano', 'cadena', 'si', 'sino', 'mientras', 'hacer', 'verdadero', 'falso']
operadores = ['+', '-', '*', '/', '%', '=', '==', '<', '>', '>=', '<=']
simbolos = ['(', ')', '{', '}', '"', ';']
patron_numeros = r'^\d+$'
patron_identificadores = r'^[a-zA-Z_][a-zA-Z0-9_]*$'

# Función para cargar el archivo
def cargar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        try:
            with open(archivo, 'r') as f:
                contenido = f.read()
            texto_archivo.delete(1.0, tk.END)
            texto_archivo.insert(tk.END, contenido)
        except FileNotFoundError:
            messagebox.showerror("Error", "Archivo no encontrado.")
    else:
        messagebox.showinfo("Información", "No se seleccionó ningún archivo.")

# Función para analizar el contenido
def analizar_contenido():
    contenido = texto_archivo.get(1.0, tk.END).strip()
    if not contenido:
        messagebox.showinfo("Información", "No hay contenido para analizar.")
        return
    tokens = []
    contador_tokens = {}
    palabras = re.findall(r'\w+|[^\w\s]', contenido)
    
    for palabra in palabras:
        tipo_token = clasificar_token(palabra)
        tokens.append((palabra, tipo_token))
        if palabra in contador_tokens:
            contador_tokens[palabra]['cantidad'] += 1
        else:
            contador_tokens[palabra] = {'tipo': tipo_token, 'cantidad': 1}
    
    mostrar_resultados(contador_tokens)

# Clasificación del token
def clasificar_token(palabra):
    if palabra in palabras_reservadas:
        return 'Palabra Reservada'
    elif palabra in operadores:
        return 'Operador'
    elif palabra in simbolos:
        return 'Símbolo'
    elif re.match(patron_numeros, palabra):
        return 'Número'
    elif re.match(patron_identificadores, palabra):
        return 'Identificador'
    else:
        return 'Error'

# Mostrar resultados
def mostrar_resultados(contador_tokens):
    texto_resultados.delete(1.0, tk.END)
    texto_resultados.config(font=("Courier", 10))

    texto_resultados.insert(tk.END, f"{'TOKEN':<20} {'TIPO':<25} {'CANTIDAD':<5}\n")
    texto_resultados.insert(tk.END, "-" * 50 + "\n")
    
    for token, info in contador_tokens.items():
        texto_resultados.insert(tk.END, f"{token:<20} {info['tipo']:<25} {info['cantidad']:<5}\n")

    errores = [t for t, info in contador_tokens.items() if info['tipo'] == 'Error']
    if errores:
        texto_resultados.insert(tk.END, "\nErrores léxicos encontrados:\n")
        for token in errores:
            texto_resultados.insert(tk.END, f"Error: {token}\n")
    else:
        texto_resultados.insert(tk.END, "\nNo se encontraron errores léxicos.")

# Interfaz gráfica
ventana = tk.Tk()
ventana.title("Analizador Léxico")
ventana.geometry("600x500")
ventana.configure(bg="#f0f0f0")

titulo = tk.Label(ventana, text="Analizador Léxico", font=("Arial", 18), bg="#f0f0f0")
titulo.pack(pady=10)

boton_cargar = tk.Button(ventana, text="Cargar archivo", font=("Arial", 12), command=cargar_archivo, bg="#4CAF50", fg="white", width=20)
boton_cargar.pack(pady=5)

texto_archivo = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=60, height=10, font=("Arial", 10))
texto_archivo.pack(pady=10)

boton_analizar = tk.Button(ventana, text="Analizar contenido", font=("Arial", 12), command=analizar_contenido, bg="#2196F3", fg="white", width=20)
boton_analizar.pack(pady=5)

texto_resultados = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=60, height=10)
texto_resultados.pack(pady=10)

# Ejecutar la aplicación
ventana.mainloop()