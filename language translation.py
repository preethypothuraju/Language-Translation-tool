import streamlit as st
import requests
st.set_page_config(page_title="Language Translation Tool", page_icon="🌍", layout="centered")

LANGUAGES = {
    "Auto-detect": "auto",
    "English": "en", "Telugu": "te", "Hindi": "hi", "Tamil": "ta",
    "Kannada": "kn", "Malayalam": "ml", "Bengali": "bn", "Marathi": "mr",
    "French": "fr", "German": "de", "Spanish": "es", "Japanese": "ja",
    "Korean": "ko", "Chinese": "zh-CN", "Arabic": "ar", "Portuguese": "pt"
}

def translate_text(text, source, target):
    """Translate text using the MyMemory translation API."""
    if not text.strip():
        raise ValueError("Please enter some text to translate.")
    if source == target and source != "auto":
        return text

    url = "https://api.mymemory.translated.net/get"
    params = {
        "q": text, 
        "langpair": f"{source}|{target}",
        "de": "your_email@example.com"
        }
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, params=params, headers=headers, timeout=20)
    response.raise_for_status()
    data = response.json()

    if data.get("responseStatus") != 200:
        message = data.get("responseDetails", "The translation service could not complete the request.")
        raise RuntimeError(message)

    translated = data.get("responseData", {}).get("translatedText")
    if not translated:
        raise RuntimeError("No translated text was returned. Please try again.")
    return translated

st.title("🌍 Language Translation Tool")
st.write("Translate text between supported languages using the MyMemory translation API.")

col1, col2 = st.columns(2)
with col1:
    source_name = st.selectbox("From", list(LANGUAGES.keys()), index=0)
with col2:
    target_name = st.selectbox("To", [name for name in LANGUAGES if name != "Auto-detect"], index=0)

text = st.text_area("Enter text", height=160, placeholder="Type or paste the text you want to translate...")

if st.button("Translate", type="primary", use_container_width=True):
    if not text.strip():
        st.warning("Please enter some text first.")
    else:
        with st.spinner("Translating..."):
            try:
                result = translate_text(text, LANGUAGES[source_name], LANGUAGES[target_name])
                st.session_state["translation_result"] = result
                st.session_state["translation_target"] = target_name
            except requests.RequestException:
                st.error("Could not connect to the translation service. Check your internet connection and try again.")
            except (ValueError, RuntimeError) as exc:
                st.error(str(exc))

if st.session_state.get("translation_result"):
    st.subheader(f"Translation ({st.session_state.get('translation_target', '')})")
    st.text_area("Translated text", value=st.session_state["translation_result"], height=160)
    st.caption("Tip: Select the translated text and copy it. Translation quality may vary by language and context.")

st.divider()
st.caption("Built with Python, Streamlit, Requests, and the MyMemory API.")
