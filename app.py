import streamlit as st
from deep_translator import MyMemoryTranslator
from langdetect import detect, LangDetectException

st.set_page_config(page_title="AI Language Translator", page_icon="🌍", layout="wide")

st.markdown("""
<style>
.stApp {background: linear-gradient(135deg, #10172a, #172554); color: white;}
h1 {color: #60a5fa; text-align: center;}
.subtitle {text-align: center; color: #cbd5e1; font-size: 18px;}
div.stButton > button {border-radius: 10px; font-weight: 600; min-height: 45px;}
</style>
""", unsafe_allow_html=True)

st.title("🌍 AI Language Translator")
st.markdown('<p class="subtitle">Break language barriers with intelligent translation</p>', unsafe_allow_html=True)

# MyMemory uses regional language codes.
LANGUAGES = {
    "English": "en-GB",
    "Hindi": "hi-IN",
    "Bengali": "bn-IN",
    "Spanish": "es-ES",
    "French": "fr-FR",
    "German": "de-DE",
    "Japanese": "ja-JP",
    "Chinese (Simplified)": "zh-CN",
    "Arabic": "ar-SA",
    "Portuguese": "pt-PT",
    "Russian": "ru-RU",
    "Italian": "it-IT",
    "Korean": "ko-KR",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Marathi": "mr-IN",
    "Urdu": "ur-PK",
}

# langdetect returns short codes; map them to MyMemory codes.
DETECTION_CODES = {
    "en": "en-GB", "hi": "hi-IN", "bn": "bn-IN",
    "es": "es-ES", "fr": "fr-FR", "de": "de-DE",
    "ja": "ja-JP", "zh-cn": "zh-CN", "zh-tw": "zh-TW",
    "ar": "ar-SA", "pt": "pt-PT", "ru": "ru-RU",
    "it": "it-IT", "ko": "ko-KR", "ta": "ta-IN",
    "te": "te-IN", "mr": "mr-IN", "ur": "ur-PK",
}

if "history" not in st.session_state:
    st.session_state.history = []
if "last_translation" not in st.session_state:
    st.session_state.last_translation = ""

st.divider()
left, right = st.columns(2)

with left:
    st.subheader("📝 Original Text")
    source_language = st.selectbox("Translate from", ["Auto Detect"] + list(LANGUAGES.keys()))
    source_text = st.text_area("Enter your text", height=220, placeholder="Type or paste your text here...")

with right:
    st.subheader("🌐 Translation")
    target_language = st.selectbox("Translate to", list(LANGUAGES.keys()), index=2)
    if st.session_state.last_translation:
        st.text_area("Translated text", value=st.session_state.last_translation, height=220, disabled=True)
    else:
        st.info("Your translated text will appear here.")

if st.button("🚀 Translate Now", use_container_width=True):
    if not source_text.strip():
        st.warning("Please enter some text first.")
    else:
        try:
            if source_language == "Auto Detect":
                detected_code = detect(source_text).lower()
                source_code = DETECTION_CODES.get(detected_code, detected_code)
                st.info(f"Detected language code: {source_code}")
            else:
                source_code = LANGUAGES[source_language]

            target_code = LANGUAGES[target_language]

            if source_code == target_code:
                result = source_text
            else:
                result = MyMemoryTranslator(
                    source=source_code,
                    target=target_code
                ).translate(source_text)

            if not result:
                st.error("The translation service returned an empty result.")
            else:
                st.session_state.last_translation = result
                st.session_state.history.append({
                    "original": source_text,
                    "translated": result,
                    "source": source_code,
                    "target": target_language
                })
                st.success("Translation completed successfully!")
                st.rerun()

        except LangDetectException:
            st.error("Could not detect the language. Please select the source language manually.")
        except Exception as error:
            st.error(f"Translation failed: {error}")
            st.info("Check your internet connection. The free translation service may also have request limits.")

if st.session_state.last_translation:
    st.download_button(
        "📥 Download Translation",
        data=st.session_state.last_translation,
        file_name="translated_text.txt",
        mime="text/plain",
        use_container_width=True
    )

st.divider()
st.subheader("🕘 Translation History")

if st.session_state.history:
    for index, item in enumerate(reversed(st.session_state.history), start=1):
        with st.expander(f"Translation {index} — {item['target']}"):
            st.write("**Original:**")
            st.write(item["original"])
            st.write("**Translated:**")
            st.write(item["translated"])
            st.caption(f"From {item['source']} to {item['target']}")

    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.session_state.last_translation = ""
        st.rerun()
else:
    st.info("Your translation history will appear here.")

st.divider()
st.caption("Developed using Python • Streamlit • Deep Translator • Language Detection")
