# 🤖 HR AI Recruiter Assistant

Aplikacja oparta na **Streamlit** i **OpenAI GPT-4o**, służąca do automatyzacji procesu wstępnej selekcji kandydatów. Narzędzie analizuje pliki CV (PDF/DOCX) i porównuje je z wymaganiami na dane stanowisko, generując ranking dopasowania oraz szczegółowe podsumowanie zalet i braków kandydata.

## ✨ Główne Funkcjonalności

* **Analiza CV:** Obsługa formatów `.pdf` oraz `.docx`.
* **Silnik AI:** Wykorzystuje model `gpt-4o` do inteligentnej ekstrakcji informacji i oceny kompetencji.
* **Szablony Stanowisk:** Wbudowane, gotowe profile dla ról takich jak *Junior DevOps Engineer* czy *IT Support Specialist*.
* **Ranking Kandydatów:** Automatyczna ocena dopasowania w skali 0-100%.
* **Szczegółowy Raport:** Wypunktowanie kluczowych zalet oraz brakujących umiejętności dla każdego kandydata.
* **Interfejs:** Przejrzysty UI zbudowany w Streamlit.

## 🛠️ Wymagania

* Python 3.8 lub nowszy
* Klucz API do OpenAI (z dostępem do modelu GPT-4o)

## 🚀 Instalacja i Uruchomienie (macOS / Linux)

Postępuj zgodnie z poniższymi krokami, aby uruchomić projekt lokalnie:

1.  **Sklonuj repozytorium lub pobierz pliki:**
    Upewnij się, że masz pliki `app.py`, `requirements.txt` w jednym folderze.

2.  **Stwórz wirtualne środowisko:**
    ```bash
    python3 -m venv venv
    ```

3.  **Aktywuj środowisko:**
    ```bash
    source venv/bin/activate
    ```

4.  **Zainstaluj wymagane biblioteki:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Uruchom aplikację:**
    ```bash
    streamlit run app.py
    ```

## 📖 Instrukcja Obsługi

1.  **Konfiguracja:** Po uruchomieniu aplikacji, w panelu bocznym (po lewej stronie) wprowadź swój **OpenAI API Key**.
2.  **Profil Stanowiska:**
    * Wybierz gotowy szablon z listy (np. *Junior DevOps*) – pola wypełnią się automatycznie.
    * Lub wypełnij formularz ręcznie (Nazwa stanowiska, Wymagania Must-have, etc.).
3.  **Wgranie CV:** Przeciągnij pliki CV kandydatów (PDF lub DOCX) w wyznaczone pole.
4.  **Analiza:** Kliknij przycisk **🚀 Rozpocznij Analizę AI**.
5.  **Wyniki:** Po chwili zobaczysz tabelę z rankingiem oraz szczegółowe karty dla każdego kandydata.

## 🧰 Wykorzystane Technologie

* [Streamlit](https://streamlit.io/) - Interfejs użytkownika
* [OpenAI API](https://openai.com/) - Analiza tekstu (GPT-4o)
* [Pandas](https://pandas.pydata.org/) - Przetwarzanie danych i tabele
* [PyPDF2](https://pypi.org/project/PyPDF2/) - Odczyt plików PDF
* [python-docx](https://python-docx.readthedocs.io/) - Odczyt plików DOCX

## ⚠️ Uwagi

* Aplikacja wysyła treść CV do API OpenAI. Upewnij się, że masz zgodę na przetwarzanie danych w ten sposób (zgodnie z RODO/GDPR), lub zanonimizuj dane przed wgraniem.
* Korzystanie z API wiąże się z kosztami zgodnie z cennikiem OpenAI.

---
*Projekt stworzony w celach edukacyjnych i demonstracyjnych.*