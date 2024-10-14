import tkinter as tk
import tkinter.ttk as ttk
import imaplib as il
from email import message_from_bytes
import PyPDF2
import os
import webbrowser
import logging

# Paleta de colores de la interfaz
principal_color: str = "#D9D9D9"
secundary_color: str = "#0D0D0D"
terciary_color: str = "#A68256"

# Configuración de la ventana principal
root = tk.Tk()
root.title("Filtrador de curriculums")
root.geometry("750x500")
root.minsize(600, 600)
root.configure(bg=principal_color)

# Para un sistema Linux que no soporta .ico
icon_img = tk.PhotoImage(file="logo_filtrador_curriculum.png")
root.iconphoto(True, icon_img)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Configuracion para el manejo de errores
logging.basicConfig(filename="filtrador_log.txt", level=logging.DEBUG, format="%(asctime)s-%(levelname)s-%(message)s")


# Componente para los textos
def created_text(widget, font_size, row, column, columnspan):
    widget.config(fg=secundary_color, bg=principal_color, font=("system-ui", font_size, "bold"))
    widget.grid(row=row, column=column, columnspan=columnspan, padx=25, pady=12, sticky="nsew")
    return widget


# Componente para los botones
def created_button(text, parent_frame, command, background, row, column, columnspan):
    button = tk.Button(parent_frame, text=text, command=command, fg=secundary_color, bg=background,
                       highlightbackground=terciary_color, highlightthickness=2, font=("system-ui", 17, "bold"))
    button.grid(row=row, column=column, columnspan=columnspan, padx=15, pady=12, sticky="nsew")
    return button


# Componente para las entradas de datos
def create_entry(default_text, parent_frame, row, column, columnspan):
    entry = tk.Entry(parent_frame, fg=secundary_color, bg=principal_color, highlightbackground=terciary_color,
                     highlightthickness=2)
    entry.insert(0, default_text)
    entry.grid(row=row, column=column, columnspan=columnspan, padx=25, pady=12.5, sticky="nsew")
    return entry


# Funcion para la navegación entre páginas
def mostrar_pagina(page):
    for widget in root.winfo_children():
        widget.grid_forget()
    page()


# Vista principal
def main():
    frame_main = tk.Frame(root)
    frame_main.config(bg=principal_color, highlightbackground=terciary_color, highlightthickness=8)

    text_main = created_text(tk.Label(frame_main, text="Bienvenido a tu filtrador de curriculums"), 19, 0, 0, 4)

    button_start = created_button("Iniciar", frame_main, lambda: mostrar_pagina(email_of_selection), terciary_color, 1,
                                  0, 4)

    frame_main.grid()


# Vista para ingresar los datos de acceso al correo
def email_of_selection():
    frame_email = tk.Frame(root)
    frame_email.config(bg=principal_color, highlightbackground=terciary_color, highlightthickness=8)

    text_title = created_text(tk.Label(frame_email, text="Acceso a correo"), 17, 1, 0, 4)

    text_email = created_text(tk.Label(frame_email, text="Correo"), 17, 2, 0, 2)
    entry_email = create_entry("Ingresar correo", frame_email, 2, 2, 2)  # proyectotiznadog@gmail.com

    text_password = created_text(tk.Label(frame_email, text="Contraseña"), 17, 3, 0, 2)
    entry_password = create_entry("Ingresar contraseña", frame_email, 3, 2, 2)  # chlu jqle pxqg pbfu

    # Dentro de este correo creado para este proyecto hay un total de 25 curriculum en el area de:
    # manipulacion de alimentos, cocina, software y ventas

    text_alert1 = created_text(tk.Label(frame_email, text="Recuerda seguir los siguentes pasos:"), 17, 4, 0, 4)
    text_alert2 = created_text(tk.Label(frame_email, text="1. habilitar el acceso IMAP en tu correo"), 17, 5, 0, 4)
    text_alert3 = created_text(tk.Label(frame_email, text="2. habilitar la verificacion en 2 pasos de google"), 17, 6,
                               0, 4)
    text_alert4 = created_text(tk.Label(frame_email, text="3. habilitar app passwoord en tu cuenta de google"), 17, 7,
                               0, 4)

    button_back = created_button("Retroceder", frame_email, lambda: mostrar_pagina(main), terciary_color, 8, 0, 2)
    button_next = created_button("Continuar", frame_email,
                                 lambda: email_access(entry_email.get(), entry_password.get()), terciary_color, 8, 2, 2)

    frame_email.grid()

    def show_pdf_location():
        pdf_folder = os.path.abspath("Curriculum filtrado")
        message_label = tk.Label(root, text=f"Los archivos se han guardado en: {pdf_folder}", fg=secundary_color,
                                 bg=principal_color)
        message_label.grid(row=9, column=0, columnspan=4)

        open_button = tk.Button(root, text="Abrir carpeta", command=lambda: webbrowser.open(pdf_folder))
        open_button.grid(row=10, column=0, columnspan=4, padx=15, pady=12, sticky="nsew")

    # Funcion para el acceso a correo y extracción de archivos adjuntos
    def email_access(email_data, password_data):
        try:
            # Busca la carpeta donde se guardaran los curriculum y en caso de no existir la crea
            if not os.path.exists("Curriculum filtrado"):
                os.makedirs("Curriculum filtrado")

            # Se Accede al correo
            mail = il.IMAP4_SSL("imap.gmail.com")
            mail.login(email_data, password_data)
            mail.select("inbox")

            status, data = mail.search(None, "ALL")
            mail_ids = data[0].split()

            for mail_id in mail_ids:
                status, msg_data = mail.fetch(mail_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = message_from_bytes(response_part[1])

                        # Extraer archivos adjuntos
                        for part in msg.walk():
                            if part.get_content_maintype() == 'multipart':
                                continue
                            if part.get('Content-Disposition') is None:
                                continue
                            filename = part.get_filename()
                            if filename:
                                filepath = os.path.join("Curriculum filtrado", filename)
                                with open(filepath, "wb") as f:
                                    f.write(part.get_payload(decode=True))
                                logging.info(f"Archivo adjunto guardado: {filepath}")

            mail.close()
            mail.logout()
            logging.info("Acceso al correo y descarga de archivos exitosos.")
            mostrar_pagina(criteria_of_selection)
        except Exception as e:
            logging.error(f"Error al acceder al correo: {e}")
            print(f"Error al acceder al correo: {e}")


# Vista para ingresar los criterios de selección
def criteria_of_selection():
    frame_criteria = tk.Frame(root)
    frame_criteria.config(bg=principal_color, highlightbackground=terciary_color, highlightthickness=8)

    text_criteria_keys_words = created_text(tk.Label(frame_criteria, text="¿Que es lo que buscas?"), 17, 1, 0, 4)

    text_criteria_keys_words = created_text(tk.Label(frame_criteria, text="Palabras claves"), 17, 2, 0, 2)
    entry_criteria_kays_words = create_entry("Puesto, Experiencia, Proyectos, Estudios, Modalidad", frame_criteria, 2,
                                             2, 2)

    text_criteria_alert = created_text(tk.Label(frame_criteria, text="Recuerda usar palabras relevantes"), 17, 3, 0, 4)

    buttom_back = created_button("Retroceder", frame_criteria, lambda: mostrar_pagina(email_of_selection),
                                 terciary_color, 4, 0, 2)
    buttom_continue = created_button("Finalizar", frame_criteria, lambda: process_cv(entry_criteria_kays_words.get()),
                                     terciary_color, 4, 2, 2)

    frame_criteria.grid()

    def extract_text_from_pdf(pdf_path):
        try:
            with open(pdf_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in range(len(reader.pages)):
                    page_text = reader.pages[page].extract_text()
                    if page_text:
                        text += page_text
                    else:
                        text += "[No se pudo extraer texto de esta página]\n"
            return text
        except Exception as e:
            print(f"Error al leer el archivo PDF: {e}")
            return ""

    # Nota: podria trabajar para hacer mas compleja y completa esta funcion en el futuro
    def filter_keywords_and_quality(cv, keywords):
        text = extract_text_from_pdf(cv)
        required_sections = ["Proyectos"]  # Podria hacerlo un input

        if len(text.split()) < 100:
            return False
        if all(section.lower() in text.lower() for section in required_sections):
            if all(keyword.lower() in text.lower() for keyword in keywords):
                return True
        return False

    # Función para procesar el CV
    def process_cv(keywords_input):
        keywords = [keyword.strip() for keyword in keywords_input.split(",")]
        cv_folder = "Curriculum filtrado"
        cv_files = [f for f in os.listdir(cv_folder) if f.endswith(".pdf")]

        # Crear barra de progreso para que sea mas visual el proceso para el usuario
        progress = ttk.Progressbar(frame_criteria, orient=tk.HORIZONTAL, length=400, mode='determinate')
        progress.grid(row=5, column=0, columnspan=4, padx=15, pady=12, sticky="nsew")

        total_files = len(cv_files)
        for i, filename in enumerate(cv_files, 1):
            cv_path = os.path.join(cv_folder, filename)
            if filter_keywords_and_quality(cv_path, keywords):
                print(f"El currículum {filename} cumple con los criterios.")
            else:
                print(f"El currículum {filename} no cumple con los criterios.")

            # Actualizar la barra de progreso
            progress['value'] = (i / total_files) * 100
            root.update_idletasks()  # Actualizar la interfaz

        # Finalizar
        progress.grid_forget()  # Quitar la barra cuando el proceso haya terminado
        print("Proceso de filtrado finalizado")


# Iniciar la aplicación
main()

root.mainloop()
