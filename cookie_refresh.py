from seleniumbase import SB
import time

EMAIL = "sandrominori50+ulugarecexisa@gmail.com"
PASSWORD = "DDnmVV45!!"
LOGIN_URL = "https://www.easyhits4u.com/logon/"

with SB(uc=True, headless=True, xvfb=True) as sb:
    sb.open(LOGIN_URL)
    print("⏳ Attendo Turnstile...")
    sb.wait_for_element_visible('input[name="username"]', timeout=90)
    sb.type('input[name="username"]', EMAIL)
    sb.type('input[name="password"]', PASSWORD)
    sb.driver.find_element("name", "password").send_keys("\n")
    print("🔑 Login inviato.")
    time.sleep(8)

    cookies = sb.get_cookies()
    sesids = next((c['value'] for c in cookies if c['name'] == 'sesids'), None)
    user_id = next((c['value'] for c in cookies if c['name'] == 'user_id'), None)

    if sesids and user_id:
        print(f"🎉 SUCCESSO! sesids={sesids} user_id={user_id}")
    else:
        print("❌ Cookie non trovati.")
        print(cookies)