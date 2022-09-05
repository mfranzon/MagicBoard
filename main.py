import pandas as pd
from PIL import Image
from utils import pipe_image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import gettext

_ = gettext.gettext

language = st.selectbox(_('Choose your language'), ['en', 'it'])
try:
  localizator = gettext.translation('base', localedir='locales', languages=[language])
  localizator.install()
  _ = localizator.gettext 
except:
    pass

st.markdown("<h1 style='text-align:center;'> Magic Board</h1>", unsafe_allow_html=True)
# Specify canvas parameters in application
drawing_mode = st.sidebar.selectbox(
    _("Drawing tool:"), ("freedraw", "line", "rect", "circle", "transform")
)

stroke_width = st.sidebar.slider(_("Stroke width: "), 1, 25, 3)
stroke_color = st.sidebar.color_picker(_("Stroke color hex: "))
bg_color = st.sidebar.color_picker(_("Background color hex: "), "#eee")
bg_image = st.sidebar.file_uploader(_("Background image:"), type=["png", "jpg"])
n_steps = st.sidebar.slider(_("Number of Steps: "), 1, 50, 5)
strength = st.sidebar.slider(_("Strength value: "), 0.0, 1.0, 0.1)

#realtime_update = st.sidebar.checkbox("Update in realtime", False)

    

# Create a canvas component
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    background_image=Image.open(bg_image) if bg_image else None,
    update_streamlit=False,
    height=450,
    width=680,
    drawing_mode=drawing_mode,
    #point_display_radius=point_display_radius if drawing_mode == 'point' else 0,
    key="canvas",
)

prompt = st.text_input(_('Prompt to generate your cool image'), 
               placeholder=_('write you text here to improve the image with your favourite style'))

if st.button('Submit'):
    image = pipe_image(prompt=prompt,
                       init_image=canvas_result.image_data,
                       n_steps=n_steps,
                       strength=strength)
    st.image(image)
# if canvas_result.json_data is not None:
#     objects = pd.json_normalize(canvas_result.json_data["objects"]) # need to convert obj to str because PyArrow
#     for col in objects.select_dtypes(include=['object']).columns:
#         objects[col] = objects[col].astype("str")
#     #st.dataframe(objects)