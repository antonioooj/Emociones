import streamlit as st
import pandas as pd
from PIL import Image
import os
import base64
from io import BytesIO  # Importar BytesIO desde io
import time
import plotly.express as px




# Archivo para guardar las selecciones
csv_file = 'selecciones.csv'

# Crear el archivo CSV si no existe
if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=["Selecciones"])
    df.to_csv(csv_file, index=False)

st.set_page_config(layout="wide")
# Mostrar una gran imagen en la parte superior.
st.image('./Media/header.png', use_column_width=True)

# Insertar un espacio vertical de 60px
st.markdown(f'<div style="margin-top: 60px;"></div>', unsafe_allow_html=True)
# Título de la aplicación
st.title("Gráfico de emociones")


# Lista de imágenes y sus pies de imagen
imagenes = [
    {"file": "./Media/contento.png", "caption": "Contento"},
    {"file": "./Media/triste.png", "caption": "Triste"},
    {"file": "./Media/contento.png", "caption": "Enfadado"},
    {"file": "./Media/triste.png", "caption": "Aburrido"}
]

with st.sidebar:
    st.header("¿Como te sientes hoy?")
    # Función para codificar una imagen en base64
    def pil_image_to_base64(image):
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
        # Contenedor para el pop-up
    popup_placeholder = st.empty()

    # Mostrar las imágenes y permitir la selección haciendo clic en cada una
    for imagen in imagenes:
        img = Image.open(imagen["file"])
        img_base64 = pil_image_to_base64(img)
        image_html = f'<img src="data:image/png;base64,{img_base64}" style="cursor:pointer;width:200px;height:200px;" />'
        if st.button(imagen["caption"], key=imagen["caption"]):
            st.session_state.selected_image = imagen

    # Manejo de selección
    if "selected_image" in st.session_state:
        selection = st.session_state.selected_image
        st.success(f"Has seleccionado {selection['caption']}")

        # Mostrar el pop-up con la imagen seleccionada
        with popup_placeholder.container():
            st.image(selection["file"], caption=selection["caption"], use_column_width=True)
        
        # Esperar 2 segundos antes de limpiar el pop-up
        time.sleep(2)
        popup_placeholder.empty()

        # Guardar la selección en el archivo CSV
        df = pd.read_csv(csv_file)
        df = df.append({"Selecciones": selection["caption"]}, ignore_index=True)
        df.to_csv(csv_file, index=False)
        del st.session_state.selected_image

        
# Mostrar resultados guardados
#st.subheader("Resultados de las selecciones")
df = pd.read_csv(csv_file)
#st.dataframe(df)

# Gráfica de los resultados
#if not df.empty:
 #   st.bar_chart(df['Selecciones'].value_counts())                                                                          



# Gráfica de los resultados con colores personalizados usando plotly
if not df.empty:
    selection_counts = df['Selecciones'].value_counts().reset_index()
    selection_counts.columns = ['Seleccion', 'Count']
    
    # Mantener el orden original de las imágenes
    ordered_selections = [imagen["caption"] for imagen in imagenes]
    selection_counts['Seleccion'] = pd.Categorical(selection_counts['Seleccion'], categories=ordered_selections, ordered=True)
    
    # Colores personalizados
    colors = ['#33FF57','#F3FF33','#FF5733','#3357FF']  # Ejemplo de colores, puedes personalizarlos
    
    fig = px.bar(selection_counts.sort_values('Seleccion'), x='Seleccion', y='Count', color='Seleccion',
                 color_discrete_sequence=colors, title="Distribución de Selecciones")
    st.plotly_chart(fig)