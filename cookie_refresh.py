#!/usr/bin/env python3
# cookie_refresh.py
# Script per il login automatico su EasyHits4U tramite VPN (OpenVPN) ed estrazione cookie.
# Da eseguire su Render come Background Worker (piano Starter).

import os
import time

# Forza le directory scrivibili da SeleniumBase (evita l'errore Permission denied)
os.environ['HOME'] = '/app'
os.environ['TMPDIR'] = '/tmp'

from seleniumbase import SB

# ========================= CONFIGURAZIONE =========================
EMAIL = "sandrominori50+ulugarecexisa@gmail.com"
PASSWORD = "DDnmVV45!!"
LOGIN_URL = "https://www.easyhits4u.com/logon/"

# Opzionale: salvataggio su Supabase (aggiungi variabili d'ambiente su Render)
# SUPABASE_URL = os.environ.get("SUPABASE_URL")
# SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
# ACCOUNT_NAME = "uujkrczveemscvo"

# ========================= FUNZIONE PRINCIPALE =========================
def main():
    print("🚀 Avvio browser e login su EasyHits4U...")

    # uc=True   → undetected-chromedriver per bypassare rilevamenti
    # headless=True  → nessuna interfaccia grafica (necessario su server)
    # xvfb=True      → display virtuale (richiesto da Chrome in headless)
    # NESSUN PROXY → tutto il traffico è già instradato dalla VPN (OpenVPN)
    with SB(uc=True, headless=True, xvfb=True) as sb:
        # 1. Apri la pagina di login
        sb.open(LOGIN_URL)
        print("⏳ Attendo caricamento pagina e risoluzione Turnstile...")

        # 2. Attendi che il campo username diventi interattivo (Turnstile superato)
        sb.wait_for_element_visible('input[name="username"]', timeout=90)
        print("✅ Turnstile risolto, compilo credenziali...")

        # 3. Inserisci email e password
        sb.type('input[name="username"]', EMAIL)
        sb.type('input[name="password"]', PASSWORD)

        # 4. Invia il form con il tasto ENTER (simula comportamento umano)
        sb.driver.find_element("name", "password").send_keys("\n")
        print("🔑 Login inviato.")

        # 5. Attendi il redirect verso l'area autenticata
        time.sleep(8)  # attesa fissa per sicurezza
        current_url = sb.get_current_url()
        if "surf" in current_url or "dashboard" in current_url:
            print("✅ Login riuscito, sessione avviata.")
        else:
            print(f"⚠️ Redirect non rilevato. URL attuale: {current_url}")

        # 6. Estrai i cookie di sessione
        cookies = sb.get_cookies()
        sesids = next((c['value'] for c in cookies if c['name'] == 'sesids'), None)
        user_id = next((c['value'] for c in cookies if c['name'] == 'user_id'), None)

        if sesids and user_id:
            print("\n🎉 SUCCESSO! Cookie di sessione ottenuti:")
            print(f"sesids = {sesids}")
            print(f"user_id = {user_id}")
            # Esempio di salvataggio su Supabase (commentato)
            # if SUPABASE_URL and SUPABASE_KEY:
            #     from supabase import create_client
            #     supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
            #     cookie_string = f"sesids={sesids}; user_id={user_id}"
            #     supabase.table("account_cookies").upsert({
            #         "account_name": ACCOUNT_NAME,
            #         "cookies_string": cookie_string,
            #         "status": "active"
            #     }).execute()
            #     print("💾 Cookie salvati su Supabase.")
        else:
            print("\n❌ Cookie di sessione non trovati.")
            print("Cookie ricevuti:", [(c['name'], c['value'][:30]) for c in cookies])

if __name__ == "__main__":
    main()
