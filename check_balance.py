import json
import time
from web3 import Web3

# --- CẤU HÌNH ---
rpc_url = "https://rpc.testnet.arc.network"
token_address = "0x3600000000000000000000000000000000000000" # USDC ARC
token_decimals = 6

# --- HÀM HỖ TRỢ ---
def get_w3(proxy=None):
    """Kết nối Web3 (có hoặc không có Proxy)"""
    if proxy:
        return Web3(Web3.HTTPProvider(rpc_url, request_kwargs={
            'proxies': {'http': proxy, 'https': proxy},
            'timeout': 30
        }))
    else:
        return Web3(Web3.HTTPProvider(rpc_url, request_kwargs={'timeout': 30}))

def get_balance(w3, contract, address):
    try:
        # Checksum địa chỉ để tránh lỗi định dạng
        checksum_address = Web3.to_checksum_address(address)
        balance_wei = contract.functions.balanceOf(checksum_address).call()
        return balance_wei / (10 ** token_decimals)
    except Exception as e:
        return -1 # Trả về -1 nếu lỗi

# --- CHƯƠNG TRÌNH CHÍNH ---
def main():
    # 1. Đọc file wallet.txt
    try:
        with open('wallet.txt', 'r') as f:
            wallets = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("❌ Lỗi: Không tìm thấy file wallet.txt")
        return

    # 2. Đọc file proxy.txt (Nếu không có thì chạy mạng thường)
    proxies = []
    try:
        with open('proxy.txt', 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("⚠️ Không tìm thấy file proxy.txt -> Sẽ chạy bằng mạng trực tiếp (Cẩn thận bị chặn nếu check nhiều).")

    print(f"📋 Đã tải {len(wallets)} ví để kiểm tra...")
    print(f"🌍 Số lượng Proxy khả dụng: {len(proxies)}")
    print("-" * 40)

    # 3. Setup Contract
    # Dùng một kết nối tạm để tạo object contract
    w3_temp = get_w3(proxies[0] if proxies else None)
    abi = json.loads('[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]')
    contract = w3_temp.eth.contract(address=Web3.to_checksum_address(token_address), abi=abi)

    total_usdc = 0
    success_count = 0
    
    # Mở file để ghi kết quả
    with open('balance_report.txt', 'w', encoding='utf-8') as outfile:
        outfile.write(f"THỜI GIAN CHECK: {time.ctime()}\n")
        outfile.write("-" * 40 + "\n")

        for i, wallet in enumerate(wallets):
            # Chọn proxy xoay vòng
            current_proxy = proxies[i % len(proxies)] if proxies else None
            
            # Tạo kết nối mới cho mỗi ví để đổi IP
            w3 = get_w3(current_proxy)
            
            if not w3.is_connected():
                print(f"❌ [{i+1}] Lỗi kết nối Proxy, đang thử lại...")
                # Thử lại không proxy nếu proxy chết
                w3 = get_w3(None)

            # Gọi hàm check
            balance = get_balance(w3, contract, wallet)
            
            if balance >= 0:
                print(f"✅ [{i+1}/{len(wallets)}] {wallet[:10]}... : {balance} USDC")
                outfile.write(f"{wallet} | {balance} USDC\n")
                total_usdc += balance
                success_count += 1
            else:
                print(f"❌ [{i+1}/{len(wallets)}] {wallet[:10]}... : Lỗi khi đọc dữ liệu")
                outfile.write(f"{wallet} | ERROR\n")

            # Nghỉ xíu để không spam RPC (0.5 giây)
            time.sleep(0.5)

        # Tổng kết
        summary = f"\n" + "=" * 40 + f"\nTOÀN BỘ SỐ DƯ: {total_usdc} USDC\nSỐ VÍ CHECK THÀNH CÔNG: {success_count}/{len(wallets)}"
        print(summary)
        outfile.write(summary)

    print(f"\n💾 Đã lưu chi tiết vào file 'balance_report.txt'")

if __name__ == "__main__":
    main()