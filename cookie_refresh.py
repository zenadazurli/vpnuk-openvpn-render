# cookie_refresh.py
import time
from seleniumbase import SB

# Credenziali EasyHits4U
EMAIL = "sandrominori50+ulugarecexisa@gmail.com"
PASSWORD = "DDnmVV45!!"
LOGIN_URL = "https://www.easyhits4u.com/logon/"

def main():
    print("🚀 Avvio browser e login su EasyHits4U...")
    
    # Usa uc=True per superare rilevamenti, headless=True, xvfb=True per ambiente senza GUI
    # Niente proxy: tutto il traffico già instradato dalla VPN (OpenVPN)
    with SB(uc=True, headless=True, xvfb=True) as sb:
        sb.open(LOGIN_URL)
        print("⏳ Attendo caricamento pagina e risoluzione Turnstile...")
        
        # Aspetta che il campo username diventi visibile (segno che Turnstile è superato)
        sb.wait_for_element_visible('input[name="username"]', timeout=90)
        print("✅ Turnstile risolto, compilo credenziali...")
        
        sb.type('input[name="username"]', EMAIL)
        sb.type('input[name="password"]', PASSWORD)
        
        # Invia il form con il tasto Enter (simula comportamento umano)
        sb.driver.find_element("name", "password").send_keys("\n")
        print("🔑 Login inviato.")
        
        # Attendi il redirect all'area autenticata (max 30 secondi)
        time.sleep(8)
        # Verifica che l'URL sia cambiato (opzionale)
        current_url = sb.get_current_url()
        if "surf" in current_url or "dashboard" in current_url:
            print("✅ Login riuscito, sessione avviata.")
        else:
            print(f"⚠️ Redirect non rilevato. URL attuale: {current_url}")
        
        # Estrai i cookie di sessione
        cookies = sb.get_cookies()
        sesids = next((c['value'] for c in cookies if c['name'] == 'sesids'), None)
        user_id = next((c['value'] for c in cookies if c['name'] == 'user_id'), None)
        
        if sesids and user_id:
            print("\n🎉 SUCCESSO! Cookie di sessione ottenuti:")
            print(f"sesids = {sesids}")
            print(f"user_id = {user_id}")
            # Qui puoi salvare i cookie su Supabase o in un database
            # Esempio: supabase.table("account_cookies").upsert(...).execute()
        else:
            print("\n❌ Cookie di sessione non trovati.")
            print("Cookie ricevuti:", [(c['name'], c['value'][:30]) for c in cookies])

if __name__ == "__main__":
    main()
