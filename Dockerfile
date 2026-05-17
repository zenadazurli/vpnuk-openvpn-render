FROM python:3.11-slim

# 1. Installa Chrome, ChromeDriver, OpenVPN, e altri tool necessari
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    openvpn \
    iptables \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# 2. Aggiungi repository Google Chrome e installa Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# 3. Installa ChromeDriver (la versione aggiornata automaticamente da seleniumbase, ma meglio assicurarsi)
#    SeleniumBase di solito gestisce il download, ma per sicurezza installiamo chromedriver-autoinstaller
RUN pip install chromedriver-autoinstaller

# 4. Copia i file del progetto
COPY client.ovpn /etc/openvpn/client.conf
COPY cookie_refresh.py .
COPY requirements.txt .

# 5. Credenziali VPN (usa il file auth.txt)
RUN echo "deduser169065" > /etc/openvpn/auth.txt && echo "1bcudu7c" >> /etc/openvpn/auth.txt

# 6. Dipendenze Python
RUN pip install --no-cache-dir -r requirements.txt

# 7. Script di avvio (OpenVPN in background, poi Python)
RUN echo '#!/bin/bash\n\
set -e\n\
echo "🔄 Avvio OpenVPN..."\n\
openvpn --config /etc/openvpn/client.conf --daemon --log /tmp/openvpn.log\n\
echo "⏳ Attendo 15 secondi per la VPN..."\n\
sleep 15\n\
echo "🚀 Eseguo script Python..."\n\
python cookie_refresh.py' > /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
