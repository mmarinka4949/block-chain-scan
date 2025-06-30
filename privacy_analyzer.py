"""
Privacy Analyzer — оценка приватности Bitcoin-транзакции.
"""

import requests
import argparse

def fetch_tx(txid):
    url = f"https://api.blockchair.com/bitcoin/raw/transaction/{txid}"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("❌ Не удалось загрузить транзакцию.")
    return r.json()["data"][txid]["decoded_raw_transaction"]

def fetch_address_usage(address):
    url = f"https://api.blockchair.com/bitcoin/dashboards/address/{address}"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()["data"][address]["address"]

def analyze_privacy(txid):
    tx = fetch_tx(txid)
    inputs = tx.get("vin", [])
    outputs = tx.get("vout", [])

    print(f"🔍 Анализ приватности транзакции: {txid}")
    print(f"🔢 Входов: {len(inputs)} | Выходов: {len(outputs)}")

    reused_addresses = 0
    input_addresses = []

    for vin in inputs:
        if "prev_out" in vin and "scriptpubkey_address" in vin["prev_out"]:
            addr = vin["prev_out"]["scriptpubkey_address"]
            input_addresses.append(addr)
            usage = fetch_address_usage(addr)
            if usage and usage["transaction_count"] > 1:
                reused_addresses += 1

    print(f"♻️ Повторно использованных адресов: {reused_addresses}/{len(inputs)}")
    if reused_addresses > 0:
        print("⚠️ Обнаружены адреса, использованные повторно — это снижает приватность.")

    cluster_risk = len(set(input_addresses)) < len(inputs)
    if cluster_risk:
        print("🧠 Все входы могут принадлежать одному владельцу (input clustering).")

    output_values = [o["value"] for o in outputs if "value" in o]
    if len(output_values) >= 2 and abs(output_values[0] - output_values[1]) < 1000:
        print("🔐 Обнаружен возможный output-splitting (equal outputs).")

    print("✅ Анализ завершён.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Privacy Analyzer — анализ приватности транзакции.")
    parser.add_argument("txid", help="TXID для анализа")
    args = parser.parse_args()
    analyze_privacy(args.txid)
