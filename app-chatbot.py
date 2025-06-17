import streamlit as st
import requests

st.set_page_config(page_title="Asistente Médico", page_icon="🩺")

st.title("🩺 Asistente Médico de Triaje")
st.markdown("Introduce una consulta clínica y obtendrás una recomendación basada en guías clínicas.")

prompt = st.text_area("Consulta médica", placeholder="Ej. ¿Qué hago si el paciente tiene disnea y ECG anómalo?", height=150)

if st.button("Obtener recomendación"):
    if prompt.strip() == "":
        st.warning("Por favor, escribe una consulta.")
    else:
        with st.spinner("Generando recomendación..."):
            response = requests.post(
                "https://nysx5f0h8j.execute-api.eu-west-3.amazonaws.com/dev/ask",
                headers={"Content-Type": "application/json"},
                json={"prompt": prompt}
            )
            if response.status_code == 200:
                data = response.json()
                st.success("✅ Recomendación generada:")
                st.markdown(data["recommendation"])
                with st.expander("📄 Fragmentos de contexto utilizados"):
                    for frag in data["context_fragments"]:
                        st.markdown(f"- {frag}")
                with st.expander("📁 Guías utilizadas"):
                    for loc in data["locations"]:
                         st.markdown(f"- `{loc}`")
            else:
                st.error(f"Error: {response.json().get('error', 'Error inesperado')}")
