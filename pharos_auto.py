import requests
from web3 import Web3
from eth_account import Account
import time
import os
import random
from pyfiglet import Figlet
from colorama import init, Fore, Style
import sys

init(autoreset=True)

RPC_URL = "https://testnet.dplabs-internal.com"
CHAIN_ID = 688688
API_URL = "https://api.pharosnetwork.xyz"
DELAY_BETWEEN_TX = 15
MINIMUM_BALANCE = 0.000001

w3 = Web3(Web3.HTTPProvider(RPC_URL))
Account.enable_unaudited_hdwallet_features()

OUTPUT_FOLDER = "results"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def show_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    fig = Figlet(font='slant')
    print(Fore.MAGENTA + fig.renderText('Pharos Testnet Auto'))
    print(Fore.WHITE + Style.BRIGHT + "Tools Automate Tx by GreyAch (Adit) | GAC Airdrop\n")
    print(Fore.RED + "1. Generate wallet baru")
    print(Fore.GREEN + "2. Login dan verifikasi akun")
    print(Fore.CYAN + "3. Kirim transaksi")
    print(Fore.YELLOW + "4. Jalankan semua tools")
    print(Fore.WHITE + "5. Exit\n")

def generate_wallet():
    acct, mnemonic = Account.create_with_mnemonic()
    return {
        "address": acct.address,
        "private_key": acct.key.hex() if acct.key.hex().startswith("0x") else "0x" + acct.key.hex(),
        "seed_phrase": mnemonic
    }

def save_generated_wallets(wallets):
    with open(os.path.join(OUTPUT_FOLDER, "phrases_hasil.txt"), "w") as pf, \
         open(os.path.join(OUTPUT_FOLDER, "pv_keys_hasil.txt"), "w") as pkf, \
         open(os.path.join(OUTPUT_FOLDER, "adress_hasil.txt"), "w") as af:
        for wallet in wallets:
            pf.write(wallet["seed_phrase"] + "\n")
            pkf.write(wallet["private_key"] + "\n")
            af.write(wallet["address"] + "\n")

def sign_message(private_key, message="pharos"):
    from eth_account.messages import encode_defunct
    acct = w3.eth.account.from_key(private_key)
    msg = encode_defunct(text=message)
    signed = acct.sign_message(msg)
    return signed.signature.hex()

def login_with_private_key(private_key):
    address = w3.eth.account.from_key(private_key).address
    signature = sign_message(private_key)
    url = f"{API_URL}/user/login?address={address}&signature={signature}"
    headers = {
        "Origin": "https://testnet.pharosnetwork.xyz",
        "Referer": "https://testnet.pharosnetwork.xyz"
    }
    response = requests.post(url, headers=headers)
    try:
        data = response.json()
        return data.get("data", {}).get("jwt")
    except:
        return None

def send_transaction(private_key, to_address, value=MINIMUM_BALANCE):
    account = w3.eth.account.from_key(private_key)
    value_wei = w3.to_wei(value, 'ether')
    nonce = w3.eth.get_transaction_count(account.address)
    tx = {
        'chainId': CHAIN_ID,
        'to': to_address,
        'value': value_wei,
        'gas': 21000,
        'gasPrice': w3.to_wei(1.2, 'gwei'),
        'nonce': nonce,
    }
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_hash.hex(), account.address

def verify_transaction(address, tx_hash, bearer_token):
    url = f"{API_URL}/task/verify?address={address}&task_id=103&tx_hash={tx_hash}"
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Origin': 'https://testnet.pharosnetwork.xyz',
        'Referer': 'https://testnet.pharosnetwork.xyz'
    }
    return requests.post(url, headers=headers).json()

def get_profile_info(address, bearer_token):
    url = f"{API_URL}/user/profile?address={address}"
    headers = {
        'Authorization': f'Bearer {bearer_token}',
        'Origin': 'https://testnet.pharosnetwork.xyz',
        'Referer': 'https://testnet.pharosnetwork.xyz'
    }
    return requests.get(url, headers=headers).json()

def fitur_1_generate_wallet():
    jumlah_wallet = int(input("Jumlah wallet yang ingin dibuat: "))
    wallets = [generate_wallet() for _ in range(jumlah_wallet)]
    save_generated_wallets(wallets)
    print("✅ Wallet berhasil digenerate dan disimpan.")
    input("Tekan Enter untuk kembali ke menu...")

def fitur_2_login_verifikasi():
    with open("privateKeys.txt", "r") as f:
        private_keys = [line.strip() for line in f if line.strip()]
    pilihan = input(f"Akun yang ingin diproses (jumlah atau 'all' untuk semua {len(private_keys)} akun): ").strip().lower()
    if pilihan == "all":
        akun_terpilih = private_keys
    else:
        try:
            jumlah = int(pilihan)
            if jumlah <= 0:
                print("Jumlah harus > 0.")
                return
            akun_terpilih = private_keys[:jumlah]
        except:
            print("Input tidak valid.")
            return

    for i, pk in enumerate(akun_terpilih):
        if not pk.startswith("0x"):
            pk = "0x" + pk
        try:
            account = w3.eth.account.from_key(pk)
            print(f"\n▶️ Wallet #{i+1}: {account.address}")
        except:
            print("❌ Private key tidak valid.")
            continue
        token = login_with_private_key(pk)
        if not token:
            print("❌ Login gagal.")
            continue
        profil = get_profile_info(account.address, token)
        if profil.get("code") == 0:
            poin = profil.get("data", {}).get("user_info", {}).get("TaskPoints", 0)
            print(f"✅ Login berhasil - Poin: {poin}")
        else:
            print("⚠️ Gagal mengambil info profil.")
    input("Tekan Enter untuk kembali ke menu...")

def fitur_3_kirim_transaksi():
    jumlah_tx = int(input("Jumlah transaksi per wallet: "))
    value = float(input("Jumlah ETH yang dikirim per transaksi: "))

    with open("privateKeys.txt", "r") as f:
        private_keys = [line.strip() for line in f if line.strip()]
    with open(os.path.join(OUTPUT_FOLDER, "adress_hasil.txt"), "r") as af:
        destination_addresses = [line.strip() for line in af if line.strip()]

    for i, pk in enumerate(private_keys):
        if not pk.startswith("0x"):
            pk = "0x" + pk
        try:
            account = w3.eth.account.from_key(pk)
            print(f"\n▶️ Wallet #{i+1}: {account.address}")
        except:
            print("❌ Private key tidak valid.")
            continue

        token = login_with_private_key(pk)
        if not token:
            print("❌ Login gagal.")
            continue

        for txi in range(jumlah_tx):
            tujuan = random.choice(destination_addresses)
            print(f"Transaksi #{txi+1} ke {tujuan}")
            try:
                tx_hash, sender = send_transaction(pk, tujuan, value)
                print(f"✅ Transaksi berhasil: {tx_hash}")
                print(f"🔗 Explorer: https://testnet.pharosscan.xyz/tx/{tx_hash}")
                with open(os.path.join(OUTPUT_FOLDER, "tx_log.txt"), "a") as logf:
                    logf.write(f"{sender} -> {tujuan}: {tx_hash}\n")
                verif = verify_transaction(sender, tx_hash, token)
                if verif.get("code") == 0:
                    print("🔒 Verifikasi sukses!")
                profil = get_profile_info(sender, token)
                poin = profil.get("data", {}).get("user_info", {}).get("TaskPoints", 0)
                print(f"🎯 Total Poin: {poin}")
            except Exception as e:
                print(f"❗ Kesalahan: {str(e)}")

            for remaining in range(DELAY_BETWEEN_TX, 0, -1):
                print(f"Menunggu {remaining} detik...", end='\r')
                time.sleep(1)
            print(' ' * 30, end='\r')
    input("Tekan Enter untuk kembali ke menu...")

def main():
    while True:
        show_banner()
        try:
            pilihan = input("Pilih fitur (1-5): ").strip()
        except KeyboardInterrupt:
            print("\nDibatalkan.")
            return

        if pilihan == "1":
            fitur_1_generate_wallet()
        elif pilihan == "2":
            fitur_2_login_verifikasi()
        elif pilihan == "3":
            fitur_3_kirim_transaksi()
        elif pilihan == "4":
            print("Menjalankan fitur 1-3...")
            fitur_1_generate_wallet()
            fitur_2_login_verifikasi()
            fitur_3_kirim_transaksi()
        elif pilihan == "5":
            print("Keluar dari program.")
            sys.exit(0)
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
