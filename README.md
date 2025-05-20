# Pharos Testnet Auto Tools

Script Python untuk otomatisasi interaksi dengan Pharos Network Testnet.

---

## 🚀 Features / Fitur

- Membuat wallet baru dengan seed phrase dan private key.  
- Login dan verifikasi akun otomatis di Pharos Testnet.  
- Mengirim transaksi antar wallet dan memverifikasi task.  
- Menjalankan semua fitur sekaligus.

---

## 📋 Requirements / Prasyarat

- Python 3.10 atau lebih baru  
- Pip package manager  
- Sistem operasi: Linux (Ubuntu/Debian) atau Android Termux  

---

## ⚙️ Installation & Usage / Instalasi & Penggunaan

1. **Clone repository**  
```bash
git clone https://github.com/axzss/pharos-testnet-auto.git
cd pharos-testnet-auto
```

2. **Install base packages**

- Ubuntu/Debian:  
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git build-essential libssl-dev libffi-dev python3-dev
```

- Termux (Android):  
```bash
pkg update && pkg upgrade -y
pkg install -y python git clang libffi-dev openssl-dev rust make
```

3. **Create and activate virtual environment (recommended)**  
```bash
python3 -m venv venv
source venv/bin/activate
```

4. **Upgrade pip and install dependencies**  
```bash
pip install --upgrade pip setuptools wheel
pip install web3 eth-account requests colorama pyfiglet
```

Atau install dari `requirements.txt` jika tersedia:  
```bash
pip install -r requirements.txt
```

5. **Siapkan file `privateKeys.txt`**  
Isi private key satu baris per key.

6. **Jalankan script**  
```bash
python3 pharos_auto.py
```

7. **Ikuti menu interaktif:**  
- 1 Generate Wallets  
- 2 Login & Verify  
- 3 Send Transactions  
- 4 Run All  
- 5 Exit  

---

## 🗂️ Output Files / File Output

| File             | EN: Description      | ID: Deskripsi           |
|------------------|----------------------|-------------------------|
| phrases_hasil.txt | Wallet seed phrases  | Daftar seed phrase wallet|
| pv_keys_hasil.txt | Private keys         | Daftar private key      |
| adress_hasil.txt  | Wallet addresses     | Daftar wallet address   |
| tx_log.txt       | Transaction log      | Log transaksi           |

---

## 🛠️ Troubleshooting Modul di Termux & Ubuntu VPS

### Termux (Android)

- Jangan jalankan script atau buat virtual environment di `/sdcard` atau storage bersama, gunakan home directory Termux:  
```bash
cd ~
mkdir pharos && cd pharos
```

- Install build tools yang diperlukan:  
```bash
pkg install clang libffi-dev openssl-dev rust make -y
pip install --upgrade pip setuptools wheel
pip install web3==6.20.1
```

- Gunakan virtual environment untuk isolasi modul:  
```bash
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install web3 eth-account requests colorama pyfiglet
```

### Ubuntu VPS

- Hindari install global tanpa izin, gunakan virtual environment atau `--user`:  
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- Install dependencies system:  
```bash
sudo apt update
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
```

- Upgrade pip sebelum install modul:  
```bash
pip install --upgrade pip setuptools wheel
```

- Cek instalasi modul:  
```bash
python3 -c "import web3, requests, colorama, pyfiglet; print('Modules installed correctly!')"
```

---

## 🧾 Recommended Ubuntu Versions

| Version   | Status      | Notes                           |
|-----------|-------------|--------------------------------|
| 20.04 LTS | Supported   | Stabil dan kompatibel luas      |
| 22.04 LTS | Recommended | Versi LTS terbaru, ideal setup |
| 24.04 LTS | Latest LTS  | Paling mutakhir, pastikan update|

---

## 📄 License

MIT License © 2025 GreyArch

---

## 👤 Credits / Kredit

- Author: Grey Arch  [@archhans](t.me/@archhans)  
- Team / Tim: GAC Airdrop Channel  
- Telegram: [channel](https://t.me/gacairdrop) , [group chat](https://t.me/gacairdropchat)  
- WhatsApp: [channel](https://whatsapp.com/channel/0029VaW2WeAAYlUGjQqhAU3p) , [group chat](https://chat.whatsapp.com/E7Xb3czpGrYAlIeBuw87O2)  

---

## ⚠️ Disclaimer

**EN:** This tool is intended for educational and testing purposes only. Excessive use or abuse may pose risks to your account.  
**ID:** Tools ini hanya untuk keperluan edukasi dan testing. Penggunaan berlebihan atau eksploitasi dapat berisiko terhadap akun Anda.

---

Terima kasih telah menggunakan tools ini!
