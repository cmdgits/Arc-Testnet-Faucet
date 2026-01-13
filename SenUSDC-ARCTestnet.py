import json
import time
import random
import os
from web3 import Web3
from dotenv import load_dotenv

# --- CẤU HÌNH MÔI TRƯỜNG ---
# 1. Load Private Key từ file .env
load_dotenv()
sender_private_key = os.getenv("SENDER_PRIVATE_KEY")

if not sender_private_key:
    print("❌ LỖI: Không tìm thấy SENDER_PRIVATE_KEY trong file .env")
    print("Vui lòng tạo file .env và thêm dòng: SENDER_PRIVATE_KEY=...")
    exit()

# 2. THÔNG TIN MẠNG ARC & TOKEN
rpc_url = "https://rpc.testnet.arc.network"
chain_id = 5042002
token_address = "0x3600000000000000000000000000000000000000" # USDC Contract
token_decimals = 6 

# 3. CẤU HÌNH THỜI GIAN CHỜ (GIÂY)
min_delay = 30 
max_delay = 60  

# --- HÀM HỖ TRỢ ---
def get_w3_connection(proxy_string):
    """Kết nối Web3 qua Proxy"""
    return Web3(Web3.HTTPProvider(rpc_url, request_kwargs={
        'proxies': {'http': proxy_string, 'https': proxy_string},
        'timeout': 60
    }))

def get_token_balance(w3, contract, address):
    """Lấy số dư Token hiện tại"""
    try:
        balance_wei = contract.functions.balanceOf(Web3.to_checksum_address(address)).call()
        return balance_wei / (10 ** token_decimals)
    except Exception:
        return 0

# --- HÀM GỬI TOKEN ---
def send_transaction(proxy, receiver_address, current_nonce, amount_to_send):
    try:
        # 1. Kết nối
        w3 = get_w3_connection(proxy)
        if not w3.is_connected():
            print(f"❌ Proxy lỗi: {proxy}")
            return False

        # Setup Contract & Account
        erc20_abi = json.loads('[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
        contract = w3.eth.contract(address=Web3.to_checksum_address(token_address), abi=erc20_abi)
        
        sender_account = w3.eth.account.from_key(sender_private_key)
        sender_address = sender_account.address

        # Kiểm tra số dư trước khi gửi
        current_balance = get_token_balance(w3, contract, sender_address)
        if current_balance < amount_to_send:
            print(f"❌ Số dư không đủ! (Có: {current_balance}, Cần: {amount_to_send})")
            return False

        # 2. Build Transaction
        tx_build = contract.functions.transfer(
            Web3.to_checksum_address(receiver_address),
            int(amount_to_send * (10 ** token_decimals))
        ).build_transaction({
            'chainId': chain_id,
            'gas': 250000,
            'gasPrice': w3.eth.gas_price, 
            'nonce': current_nonce,
        })
        
        # 3. Ký & Gửi
        signed_tx = w3.eth.account.sign_transaction(tx_build, sender_private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        print(f"⏳ Đang gửi tới {receiver_address}...")
        
        # 4. Chờ xác nhận
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        
        if receipt.status == 1:
            print(f"✅ Giao dịch thành công! (Hash: {w3.to_hex(tx_hash)})")
            
            # Cập nhật số dư
            new_sender_balance = get_token_balance(w3, contract, sender_address)
            receiver_balance = get_token_balance(w3, contract, receiver_address)
            
            print(f"   💰 Ví chính còn lại: {new_sender_balance} USDC")
            print(f"   📥 Ví phụ nhận được: {receiver_balance} USDC")
            return True
        else:
            print(f"❌ Giao dịch thất bại (Reverted).")
            return False

    except Exception as e:
        print(f"⚠️ Lỗi xử lý: {e}")
        return False

# --- CHƯƠNG TRÌNH CHÍNH ---
try:
    # --- NHẬP DỮ LIỆU TỪ NGƯỜI DÙNG ---
    print("=== TOOL GỬI USDC ARC TESTNET ===")
    try:
        amount_input = float(input("👉 Nhập số lượng USDC muốn gửi cho mỗi ví: "))
        if amount_input <= 0:
            print("Số lượng phải lớn hơn 0!")
            exit()
    except ValueError:
        print("Vui lòng nhập số hợp lệ!")
        exit()

    # Đọc file dữ liệu
    with open('wallet.txt', 'r') as f:
        receivers = [line.strip() for line in f if line.strip()]
    with open('proxy.txt', 'r') as f:
        proxies = [line.strip() for line in f if line.strip()]

    if not receivers or not proxies:
        print("Thiếu file wallet.txt hoặc proxy.txt")
        exit()

    # Khởi tạo ban đầu để lấy Nonce
    w3_init = get_w3_connection(proxies[0])
    sender_addr = w3_init.eth.account.from_key(sender_private_key).address
    current_nonce = w3_init.eth.get_transaction_count(sender_addr, 'pending')
    
    # In thông tin ban đầu
    erc20_abi_temp = json.loads('[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]')
    contract_temp = w3_init.eth.contract(address=Web3.to_checksum_address(token_address), abi=erc20_abi_temp)
    start_balance = get_token_balance(w3_init, contract_temp, sender_addr)

    print(f"\n--- THÔNG TIN CHẠY ---")
    print(f"Ví gửi: {sender_addr}")
    print(f"Số dư hiện tại: {start_balance} USDC")
    print(f"Số lượng sẽ gửi mỗi ví: {amount_input} USDC")
    print(f"Tổng số ví nhận: {len(receivers)}")
    print("----------------------------------\n")
    
    confirm = input("Bấm Enter để bắt đầu (hoặc Ctrl+C để hủy)...")

    for i, receiver in enumerate(receivers):
        proxy = proxies[i % len(proxies)]
        print(f"🔹 [{i+1}/{len(receivers)}] Đang xử lý ví: {receiver[:10]}... | Proxy: {proxy.split('@')[-1]}")
        
        # Truyền amount_input vào hàm gửi
        success = send_transaction(proxy, receiver, current_nonce, amount_input)
        
        if success:
            current_nonce += 1
            delay_time = random.randint(min_delay, max_delay)
            print(f"💤 Nghỉ {delay_time}s...\n")
            time.sleep(delay_time)
        else:
            print("⚠️ Lỗi, thử ví tiếp theo sau 10s...\n")
            time.sleep(10)

except KeyboardInterrupt:
    print("\nĐã dừng chương trình.")
except Exception as e:
    print(f"Lỗi hệ thống: {e}")