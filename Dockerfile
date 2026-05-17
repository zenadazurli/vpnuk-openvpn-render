FROM selenium/standalone-chrome:latest

USER root

# Installa Python e OpenVPN
RUN apt-get update && apt-get install -y python3 python3-pip openvpn iptables && \
    rm -rf /var/lib/apt/lists/*

# Copia i file del progetto
COPY client.ovpn /etc/openvpn/client.conf
COPY cookie_refresh.py /app/cookie_refresh.py
COPY requirements.txt /app/requirements.txt

# Crea file credenziali VPN
RUN echo "deduser169065" > /etc/openvpn/auth.txt && echo "1bcudu7c" >> /etc/openvpn/auth.txt

# Installa dipendenze Python
RUN pip3 install --no-cache-dir -r /app/requirements.txt

# Script di avvio: avvia OpenVPN in background, attiva display virtuale, poi esegue Python
RUN echo '#!/bin/bash\n\
set -e\n\
# Avvia OpenVPN\n\
echo "🔄 Avvio OpenVPN..."\n\
openvpn --config /etc/openvpn/client.conf --daemon --log /tmp/openvpn.log\n\
sleep 15\n\
# Usa il display già fornito da selenium/standalone-chrome (DISPLAY=:99)\n\
cd /app\n\
echo "🚀 Eseguo script Python..."\n\
python3 cookie_refresh.py' > /entrypoint.sh && chmod +x /entrypoint.sh

USER seluser
ENTRYPOINT ["/entrypoint.sh"]
