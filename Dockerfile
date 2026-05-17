FROM python:3.11-slim

# Installa Chrome, ChromeDriver, OpenVPN e utilità
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    openvpn \
    iptables \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Installa Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /etc/apt/trusted.gpg.d/google.gpg \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file del progetto
COPY client.ovpn /etc/openvpn/client.conf
COPY cookie_refresh.py /app/
COPY requirements.txt /app/

# Crea file credenziali VPN
RUN echo "deduser169065" > /etc/openvpn/auth.txt && echo "1bcudu7c" >> /etc/openvpn/auth.txt

# Installa le dipendenze Python
RUN pip install --no-cache-dir -r requirements.txt

# Crea la directory per i file scaricati di SeleniumBase (evita PermissionError)
RUN mkdir -p /app/downloaded_files && chmod 777 /app/downloaded_files

# Script di avvio
RUN echo '#!/bin/bash\n\
set -e\n\
echo "🔄 Avvio OpenVPN..."\n\
openvpn --config /etc/openvpn/client.conf --daemon --log /tmp/openvpn.log\n\
sleep 15\n\
echo "🚀 Eseguo script Python..."\n\
python /app/cookie_refresh.py' > /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
