import streamlit as st
from utils import *


def main():
    st.title('Traductor de Ingles a Español.')

    st.write('A continuación podrás traducir frases de inglés a español, con un longitud máxima de 20 palabras.')

    eng_text = st.text_input('Ingrese su texto en inglés', '', max_chars=100)

    if st.button('Traducir'):
        traduction = translate(eng_text, MODEL)
        st.success(traduction)


if __name__ == '__main__':
    MODEL = load_model()
    main()
