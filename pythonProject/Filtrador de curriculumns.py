import tkinter as tk
import imaplib as il
from email import message_from_bytes
import PyPDF2 as pdf
import os

os.rename("archivo_original.pdf", "carpeta/desechados/archivo.pdf")

root = tk.Tk()
root.title("Filtrador de curriculums")
root.geometry("750x750")
root.minsize(750,
             750)
root.maxsize(1000,
             1000)
root.configure(bg="#595958")

# Paleta de colores a usar a lo largo de este proyecto
principal_color = "#595958"
secundary_color = "#BFBDBA"
terciary_color = "#E34849"

# Componente para los textos
def created_text(widget, font_size, row, column, columnspan):
    widget.config(fg="#BFBDBA",
                  bg="#595958",
                  font=("system-ui", font_size, "bold"))
    widget.grid(row=row,
                column=column,
                columnspan=columnspan,
                padx=25,
                pady=12,
                sticky="nsew")
    return widget

# Componente para los botones
def created_button(text, parent_frame, comand, background, row, column, columnspan):
    buttom = tk.Button(parent_frame)
    buttom.config(text=text,
                  command=comand,
                  fg="#221E09",
                  bg=background,
                  highlightbackground="#221E09",
                  highlightthickness=2,
                  font=("system-ui", 17, "bold"))
    buttom.grid(row=row,
                column=column,
                columnspan=columnspan,
                padx=15,
                pady=12,
                sticky="nsew")
    return buttom

# Componente para las entradas de datos
def create_entry(default_text, parent_frame, row, column, columnspan):
    entry = tk.Entry(parent_frame)
    entry.config(fg="#221E09",
                 bg="#BFBDBA",
                 highlightbackground="#221E09",
                 highlightthickness=2,)
    entry.insert(0, default_text)
    entry.grid(row=row,
               column=column,
               columnspan=columnspan,
               padx=25,
               pady=12.5,
               sticky="nsew")
    return entry

# Funcion que permite la navegacion entre navegacion entre ventanas
def mostrar_pagina(page):
    for widget in root.winfo_children():
        widget.grid_forget()
    page()

# Vista  principal del programa
def main():
    frame_main = tk.Frame(root)
    frame_main.config(bg="#595958",
                      highlightbackground="#E34849",
                      highlightthickness=4)

    text_main = created_text(tk.Label(frame_main, text="Bienvenido a tu filtrador de curriculumns"), 19,0, 0, 2)

    buttom_movilidad_iniciar = created_button("Iniciar ", frame_main, lambda: mostrar_pagina(criteria_of_selection), "#E34849", 1, 0, 2)

    text_main_recomendation1 = created_text(tk.Label(frame_main, text="Recomendaciones y consideraciones"), 17, 2, 0, 2)
    text_main_recomendation2 = created_text(tk.Label(frame_main, text="Usar palabras clave relevantes: Asegurarse de que el currículum contiene las mismas palabras clave que se mencionan en la descripción del trabajo."), 15, 3, 0, 2)


    frame_main.grid()

# Vista para ingresar el correo en donde se recibiran los curriculums y el programa trabajara
def email_of_selection():
    frame_email = tk.Frame(root)
    frame_email.config(bg="#595958",
                       highlightbackground="#E34849",
                       highlightthickness=4)

    text_email = created_text(tk.Label(frame_email, text="Correo"), 17, 1, 0, 2)
    Entry_email = create_entry("Ejemplo: menos de 1 año de experiencia", frame_email, 1, 2, 2)

    buttom_movilidad_back = created_button("Retroceder", frame_email, lambda: mostrar_pagina(main), "#E34849", 2, 0, 2)
    buttom_movilidad_continue = created_button("Continuar", frame_email, lambda: mostrar_pagina(criteria_of_selection), "#E34849", 2, 2, 2)

    frame_email.grid()

    # Acceso en el gmail y extraccion de archivos adjuntos ----> Pendiente en trabajar
    def email_access():
        mail = il.IMAP4_SSL("imap.gmail.com")
        mail.login("tuemail@gmail.com", "tupassword")
        mail.select("inbox")

        status, data = mail.search(None, "ALL")
        mail_ids = data[0].split()

        for mail_id in mail_ids:
            status, msg_data = mail.fetch(mail_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = message_from_bytes(response_part[1])
                    # Aquí puedes verificar si el correo tiene un adjunto
                    for part in msg.walk():
                        if part.get_content_maintype() == 'multipart':
                            continue
                        if part.get('Content-Disposition') is None:
                            continue
                        filename = part.get_filename()
                        if filename:
                            filepath = os.path.join("/ruta/a/guardar", filename)
                            with open(filepath, "wb") as f:
                                f.write(part.get_payload(decode=True))

# Vista para ingresar los criterios de seleccion de los curriculums en el que se basara el programa
def criteria_of_selection():
    frame_criteria = tk.Frame(root)
    frame_criteria.config(bg="#595958",
                          highlightbackground="#E34849",
                          highlightthickness=4)

    text_criteria_keys_words = created_text(tk.Label(frame_criteria, text="Palabras claves"), 17, 1,0, 2)
    Entry_criteria_kays_words = create_entry("Puesto Experiencia, Proyectos, Estudios, Modalidad", frame_criteria, 1, 2, 2)

    text_criteria__anti_keys_words = created_text(tk.Label(frame_criteria, text="Excluyentes"), 17, 2, 0, 2)
    Entry_criteria_anti_keys_words = create_entry("Ejemplo: menos de 1 año de experiencia", frame_criteria, 2, 2, 2)

    buttom_movilidad_back = created_button("Retroceder", frame_criteria, lambda: mostrar_pagina(email_of_selection), "#E34849", 2, 0, 2)
    buttom_movilidad_continue = created_button("Finalizar", frame_criteria, lambda: mostrar_pagina(main), "#E34849", 2, 2, 2)

    frame_criteria.grid()

    def extract_text_from_pdf(pdf_path):
        with open(pdf_path, "rb") as f:
            reader = pdf.PdfReader(f)
            text = ""
            for page in range(len(reader.pages)):
                text += reader.pages[page].extract_text()
        return text

    # Funcion de calificacion de los curriculumns -----> Pendiente a trabajar
    def calification(cv):
        score = 0
        text = extract_text_from_cv(cv)
        if "experiencia" in text:
            score += 30
        if "proyecto" in text:
            score += 30
        if "modalidad" in text:
            score += 20
        if "estudios" in text:
            score += 20
        return score

    def move_to_desechados(cv):
        os.rename(cv, "carpeta/desechados/" + os.path.basename(cv))

    # Funcion de filtrado por legibilidad, estructura y calidad de datos ----> Pendiente a trabajar
    def filter_quality():

    # Funcion de filtrado de curriculums por palabras claves ----> Pendiente a trabajar
    def filter_keywords(cvs, keywords):
        valid_cvs = []
        for cv in cvs:
            text = extract_text_from_cv(cv)  # Función que extrae el texto de un CV
            if all(keyword.lower() in text.lower() for keyword in keywords):
                valid_cvs.append(cv)
        return valid_cvs

main()

root.mainloop()