from vaccinazioni import calcola_eta_mesi, calcola_eta_alla_dose, main
import streamlit as st
from datetime import datetime, timedelta

today = datetime.today().date()

st.set_page_config(page_title="Calcolatore Vaccini Pneumococcici Pediatrici", layout="centered")

st.markdown("## 💉 Vaccinazioni Pneumococciche Pediatriche")

data_nascita = st.date_input("📅 Data di nascita del bambino (gg/mm/aaaa)", format="DD/MM/YYYY")
categoria = st.selectbox("🏷️ Categoria del bambino", ["In buona salute", "Con patologia a rischio"])

if data_nascita and categoria:
    eta_mesi = calcola_eta_mesi(data_nascita)
    st.markdown("### 📋 Dati inseriti")
    st.markdown(f"👉 **Età attuale:** {eta_mesi} mesi (Data di nascita: {data_nascita.strftime('%d/%m/%Y')})")
    st.markdown(f"👉 **Categoria:** {categoria}")

ha_vaccinazioni = st.radio("💉 Il bambino ha già ricevuto vaccinazioni antipneumococciche?", ["No", "Sì"], key="radio_vaccinazioni")

dosi_precedenti = []



if ha_vaccinazioni == "Sì":
    n_dosi = st.number_input("👉 Quante dosi ha già ricevuto?", min_value=1, max_value=5, step=1, key="num_dosi")

    for i in range(1, n_dosi + 1):
        data_dose = st.date_input(f"📅 Data dose {i}", format="DD/MM/YYYY", key=f"data_dose_{i}")
        tipo_vaccino = st.selectbox(f"💉 Tipo vaccino dose {i}", ["PCV15", "PCV20", "PCV13", "PPSV23"], key=f"tipo_vaccino_{i}")

        oggi = datetime.today().date()
        data_limite_pcv20 = datetime.strptime("2024-01-01", "%Y-%m-%d").date()
        eta_minima_valida = data_nascita + timedelta(weeks=6)





# Controlli


# Altri Controlli

        if data_dose > oggi:
            st.error(f"⚠️ La dose {i} è nel futuro ({data_dose.strftime('%d/%m/%Y')}). Verifica la data.")
        if data_dose < data_nascita:
            st.error(f"⚠️ La dose {i} è precedente alla data di nascita ({data_dose.strftime('%d/%m/%Y')}).")
        if data_dose < eta_minima_valida:
            st.warning(f"⚠️ La dose {i} è stata somministrata prima delle 6 settimane di vita ({data_dose.strftime('%d/%m/%Y')}).")
        if tipo_vaccino == "PCV20" and data_dose < data_limite_pcv20:
            st.warning(f"⚠️ La dose {i} è con PCV20 prima dell'immissione in commercio (01/01/2024). Verificare.")
# Controllo PPSV23 prima dei 24 mesi (2 anni)
        if tipo_vaccino == "PPSV23":
            eta_mesi_ppsv23 = calcola_eta_alla_dose(data_nascita, data_dose)
            if eta_mesi_ppsv23 < 24:
                st.warning(f"⚠️ La dose {i} di PPSV23 è stata somministrata prima dei 24 mesi ({eta_mesi_ppsv23} mesi, {data_dose.strftime('%d/%m/%Y')}). "
                   "Secondo le raccomandazioni, la dose non è considerata valida. Valutare eventuale ripetizione dopo i 24 mesi.")

        if data_dose in [d["data"] for d in dosi_precedenti]:
            st.error(f"⚠️ La dose {i} ha una data duplicata ({data_dose.strftime('%d/%m/%Y')}). Verifica.")

        eta_dose = calcola_eta_alla_dose(data_nascita, data_dose)

        dosi_precedenti.append({
            "data": data_dose,
            "vaccino": tipo_vaccino,
            "eta_mesi": eta_dose
        })

# Controllo cronologia delle dosi (dopo il ciclo for)
        date_dosi = [d["data"] for d in dosi_precedenti]
        if date_dosi != sorted(date_dosi):
            st.warning("⚠️ Le date delle dosi non sono in ordine cronologico crescente. Verifica l'inserimento. Questo non comporta un alterazione del calcolo del ciclo vaccinale è solo un controllo per prevenire errori di inserimento")


main(data_nascita, eta_mesi, categoria, ha_vaccinazioni, dosi_precedenti)

# ✅ CREDITI IN CALCE
st.markdown("---")
st.markdown("""
💉 _Applicazione per uso educativo e informativo ad uso di personale adeguatamente formato._

 **Sviluppata da Davide Resi** | 📅 Versione: Giugno 2025

 ** Biblio Prevenar20 RCP, vaxneuvance RCP, calendario-vaccinale-RER, Referto Vax-consilium - Schema vaccinazioni pneumococciche pediatriche, tutte in vigore al momento del rilascio della versione**
""")
