import streamlit as st
import pandas as pd
from openai import OpenAI
import PyPDF2
from docx import Document
import io
import json

# Konfiguracja strony
st.set_page_config(page_title="HR AI Recruiter Assistant", layout="wide")

# Funkcje pomocnicze do ekstrakcji tekstu
def extract_text_from_pdf(file):
    """
    Ekstrahuje tekst z pliku PDF.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        return f"Błąd odczytu PDF: {str(e)}"

def extract_text_from_docx(file):
    """
    Ekstrahuje tekst z pliku DOCX.
    """
    try:
        doc = Document(file)
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        return "\n".join(text)
    except Exception as e:
        return f"Błąd odczytu DOCX: {str(e)}"

def analyze_cv(client, cv_text, job_profile):
    """
    Analizuje CV kandydata pod kątem profilu stanowiska używając OpenAI gpt-4o.
    Zwraca wynik w formacie JSON.
    """
    system_prompt = """
    Jesteś doświadczonym Senior HR Specjalistą (Rekruterem) z wieloletnim stażem. 
    Twój cel to obiektywna ocena kandydatów na podstawie ich CV oraz podanego opisu stanowiska.
    
    Twoja odpowiedź MUSI być w formacie JSON i zawierać następujące pola:
    {
        "kandydat_imie_nazwisko": "Imię i Nazwisko lub 'Nieznany'",
        "ocena_dopasowania": 0-100 (liczba całkowita),
        "kluczowe_zalety": ["zaleta1", "zaleta2", ...],
        "brakujace_umiejetnosci": ["brak1", "brak2", ...],
        "podsumowanie": "Krótka opinia tekstowa podsumowująca profil kandydata."
    }
    Nie dodawaj żadnego formatowania '```json', zwróć czysty JSON.
    """
    
    user_prompt = f"""
    OPIS STANOWISKA I WYMAGANIA:
    Nazwa stanowiska: {job_profile['title']}
    Wymagane umiejętności (Must-haves): {job_profile['must_haves']}
    Mile widziane (Nice-to-haves): {job_profile['nice_to_haves']}
    Szczegółowy opis: {job_profile['description']}

    TREŚĆ CV KANDYDATA:
    {cv_text}
    
    Dokonaj analizy i zwróć JSON.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.2
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Błąd podczas analizy AI: {str(e)}")
        return None

# --- GŁÓWNA APLIKACJA ---

# 1. Sidebar - Konfiguracja
with st.sidebar:
    st.header("⚙️ Konfiguracja")
    api_key = st.text_input("Podaj OpenAI API Key", type="password")
    if not api_key:
        st.warning("⚠️ Proszę podać klucz API, aby kontynuować.")
        st.stop()
    
    client = OpenAI(api_key=api_key)
    st.success("Klucz API przyjęty!")

st.title("🤖 HR AI Recruiter Assistant")
st.markdown("---")

# 2. Definiowanie Profilu Kandydata
st.header("1. Zdefiniuj Profil Kandydata")
col1, col2 = st.columns(2)

with col1:
    job_title = st.text_input("Nazwa stanowiska", placeholder="np. Senior Python Developer")
    must_haves = st.text_area("Kluczowe wymagania (Must-haves)", placeholder="- Python\n- Django\n- SQL")

with col2:
    nice_to_haves = st.text_area("Mile widziane (Nice-to-haves)", placeholder="- AWS\n- Docker\n- React")
    job_description = st.text_area("Opis stanowiska", placeholder="Szczegóły dotyczące roli, obowiązków i firmy...")

if not job_title or not must_haves:
    st.info("ℹ️ Uzupełnij nazwę stanowiska i kluczowe wymagani, aby przejść dalej.")
    st.stop()

job_profile = {
    "title": job_title,
    "must_haves": must_haves,
    "nice_to_haves": nice_to_haves,
    "description": job_description
}

st.markdown("---")

# 3. Wgrywanie i Przetwarzanie CV
st.header("2. Wgraj CV kandydatów")
uploaded_files = st.file_uploader(
    "Przeciągnij pliki PDF lub DOCX tutaj",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

if uploaded_files:
    if st.button("🚀 Rozpocznij Analizę AI"):
        results = []
        progress_bar = st.progress(0)
        
        for i, file in enumerate(uploaded_files):
            # Ekstrakcja tekstu
            if file.type == "application/pdf":
                text = extract_text_from_pdf(file)
            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                text = extract_text_from_docx(file)
            else:
                st.warning(f"Nieobsługiwany format pliku: {file.name}")
                continue
            
            if not text or len(text) < 10:
                st.warning(f"Nie udało się odczytać tekstu z pliku: {file.name} lub plik jest pusty.")
                continue

            # Analiza AI
            with st.spinner(f"Analizuję kandydata z pliku: {file.name}..."):
                analysis = analyze_cv(client, text, job_profile)
                
            if analysis:
                analysis['filename'] = file.name
                results.append(analysis)
            
            # Aktualizacja paska postępu
            progress_bar.progress((i + 1) / len(uploaded_files))

        progress_bar.empty()
        st.success("✅ Analiza zakończona!")
        st.markdown("---")

        # 4. Prezentacja Wyników
        st.header("3. Ranking Kandydatów")
        
        if results:
            df = pd.DataFrame(results)
            
            # Sortowanie po ocenie
            if 'ocena_dopasowania' in df.columns:
                df = df.sort_values(by='ocena_dopasowania', ascending=False)
            
            # Wyświetlenie głównej tabeli (wybrane kolumny dla czytelności)
            st.dataframe(
                df[['kandydat_imie_nazwisko', 'ocena_dopasowania', 'filename']],
                use_container_width=True,
                column_config={
                    "kandydat_imie_nazwisko": "Kandydat",
                    "ocena_dopasowania": st.column_config.ProgressColumn(
                        "Dopasowanie %",
                        format="%d",
                        min_value=0,
                        max_value=100
                    ),
                    "filename": "Plik źródłowy"
                }
            )
            
            # Szczegółowe karty
            st.subheader("Szczegóły analizy")
            for index, row in df.iterrows():
                with st.expander(f"{row.get('ocena_dopasowania', 0)}% - {row.get('kandydat_imie_nazwisko', 'Nieznany')} ({row.get('filename')})"):
                    st.write(f"**Podsumowanie:** {row.get('podsumowanie')}")
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        st.write("✅ **Kluczowe zalety:**")
                        for adv in row.get('kluczowe_zalety', []):
                            st.write(f"- {adv}")
                    
                    with c2:
                        st.write("❌ **Brakujące umiejętności / Ryzyka:**")
                        for missing in row.get('brakujace_umiejetnosci', []):
                            st.write(f"- {missing}")
        else:
            st.warning("Brak wyników do wyświetlenia.")
