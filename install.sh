#!/usr/bin/env bash
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
  echo "[!] Run as root: sudo ./install.sh"
  exit 1
fi

if [[ ! -f /etc/os-release ]] || ! grep -qi kali /etc/os-release; then
  echo "[!] OBT SCORPION is intentionally packaged for Kali Linux."
  exit 1
fi

echo "[🦂] OBT SCORPION — OMAR BEN TALEB"
echo "[*] Updating package metadata..."
apt-get update

echo "[*] Installing wireless analysis dependencies..."
DEBIAN_FRONTEND=noninteractive apt-get install -y \
  python3 iw iproute2 tshark aircrack-ng hostapd wpasupplicant kmod

chmod +x scorpion.py install.sh

if [[ ! -f config.json ]]; then
  cp config.example.json config.json
fi

cat >/usr/local/bin/scorpion <<EOF
#!/usr/bin/env bash
cd "$(pwd)"
exec sudo python3 "$(pwd)/scorpion.py" "\$@"
EOF
chmod +x /usr/local/bin/scorpion

echo
echo "[✓] Installed."
echo "    Launch with: sudo scorpion"
