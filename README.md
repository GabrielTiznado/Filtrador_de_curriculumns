# Proyecto: Sistema de Filtrado de Currículums ATS

📖 Descripción
Sistema de Filtrado de Currículums con Criterios ATS es una herramienta diseñada para automatizar el proceso de selección de candidatos, analizando y filtrando currículums según criterios ATS (Applicant Tracking System). Este sistema ayuda a los reclutadores a identificar rápidamente los candidatos que cumplen con los requisitos específicos de una oferta de trabajo, mejorando la eficiencia y precisión del proceso de contratación.

El sistema está desarrollado en Python y utiliza técnicas de procesamiento de lenguaje natural (NLP) para analizar y puntuar los currículums en función de palabras clave, habilidades, experiencia, y otros criterios definidos.
🚀 Características

    Procesamiento de currículums en lote: Filtra y analiza múltiples currículums a la vez.
    Puntuación basada en criterios ATS: Asigna una puntuación a cada currículum en función de la coincidencia con los criterios definidos.
    Reporte detallado: Genera un reporte con las puntuaciones y el desglose de los resultados para cada candidato.
    Soporte para múltiples formatos: Compatible con archivos PDF y DOCX.
    Interfaz de usuario simple: Opcionalmente, puede integrarse una interfaz gráfica para facilitar el uso del sistema.

🛠️ Tecnologías Utilizadas

    Lenguaje: Python
    Librerías:
    -->NLTK - Procesamiento de lenguaje natural.
    -->Spacy - Extracción de entidades y palabras clave.
    -->PyPDF2 - Lectura de archivos PDF.
    -->python-docx - Manejo de archivos DOCX.
    -->Tkinter - Interfaz gráfica para el usuario.

📄 Uso

    Ejecuta el sistema utilizando el comando python main.py.
    Carga los currículums que deseas filtrar en la carpeta resumes/.
    Configura los criterios ATS en el archivo config/criteria.json.
    Inicia el proceso de filtrado y espera a que se genere el reporte en la carpeta output/.

📊 Configuración de Criterios ATS


📚 Documentación

Si tienes preguntas o sugerencias, no dudes en contactarme a través de mi gmail tiznadog1@gmail.com

📝 Licencia

Este proyecto está bajo la licencia MIT License - consulta el archivo LICENSE.md para más detalles.
