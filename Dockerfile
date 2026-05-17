FROM python:3.11-slim

RUN apt-get update && apt-get install -y openvpn iptables curl && rm -rf /var/lib/apt/lists/*

COPY client.ovpn /etc/openvpn/client.conf
RUN echo "deduser169065" > /etc/openvpn/auth.txt && echo "1bcudu7c" >> /etc/openvpn/auth.txt

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY cookie_refresh.py .

RUN echo '#!/bin/bash\n\
echo "🔄 Avvio OpenVPN..."\n\
openvpn --config /etc/openvpn/client.conf --daemon --log /tmp/openvpn.log\n\
echo "⏳ Attendo 15 secondi..."\n\
sleep 15\n\
echo "🚀 Eseguo script..."\n\
python cookie_refresh.py' > /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]