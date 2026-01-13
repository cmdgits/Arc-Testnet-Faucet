import time
import random
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# --- CẤU HÌNH ---
url = "https://faucet.circle.com/"
wallet_file = "wallet.txt"
proxy_file = "proxy.txt"

def human_type(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.01, 0.03))

def force_click(driver, element):
    """Hàm ép click bằng Javascript (Bất chấp nút bị che)"""
    try:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", element)
        return True
    except:
        return False

def run_faucet_v18():
    print("--- TOOL FAUCET V18 (SPAN TARGET) ---")
    
    try:
        with open(wallet_file, 'r') as f:
            wallets = [line.strip() for line in f if line.strip()]
        if not wallets: return
        print(f"📂 Tìm thấy {len(wallets)} ví.")
    except:
        print(f"❌ Thiếu file wallet.txt")
        return

    proxies = []
    if os.path.exists(proxy_file):
        with open(proxy_file, 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]

    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    
    if proxies:
        options.add_argument(f'--proxy-server={proxies[0]}')

    driver = None
    try:
        print("🚀 Khởi động Chrome...")
        driver = uc.Chrome(options=options, use_subprocess=True)
        wait = WebDriverWait(driver, 40)
        
        driver.get(url)
        time.sleep(5)

        # Tắt Cookie
        try:
            cookie_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept Cookies')]"))
            )
            force_click(driver, cookie_btn)
            print("🍪 Đã tắt Cookie.")
            time.sleep(2)
        except:
            pass

        # --- VÒNG LẶP ---
        for i, wallet_address in enumerate(wallets):
            print(f"\n{'='*40}")
            print(f"🔄 VÍ SỐ {i+1}/{len(wallets)}: {wallet_address[:10]}...")

            # 1. XỬ LÝ MÀN HÌNH CŨ (Nếu lỡ bị kẹt)
            try:
                # Tìm nút quay lại theo cấu trúc HTML bạn cung cấp
                back_btns = driver.find_elements(By.XPATH, "//button[./span[contains(text(), 'Get more tokens')]]")
                if back_btns:
                    print("🔄 Đang ở màn hình kết quả cũ -> Bấm quay lại.")
                    force_click(driver, back_btns[0])
                    time.sleep(2)
            except:
                pass

            # 2. NHẬP VÍ
            print("✍️ Đang nhập ví...")
            try:
                input_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Wallet address']")))
                
                force_click(driver, input_field)
                input_field.send_keys(Keys.CONTROL + "a")
                input_field.send_keys(Keys.DELETE)
                time.sleep(0.5)
                
                human_type(input_field, wallet_address)
                time.sleep(5)
            except Exception as e:
                print(f"⚠️ Lỗi nhập liệu: {e}")
                driver.refresh(); time.sleep(5); continue

            # 3. BẤM SEND
            print("👆 Bấm Send...")
            try:
                send_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Send 1 USDC')]")))
                force_click(driver, send_button)
            except:
                print("❌ Lỗi nút Send."); continue

            # 4. CHỜ KẾT QUẢ & QUAY LẠI (SỬA THEO HTML BẠN GỬI)
            print("⏳ Đang chờ kết quả...")
            try:
                # Chờ dòng chữ "Tokens sent" hiện ra trước
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Tokens sent')]"))
                )
                print("✅ THÀNH CÔNG! (Đã thấy chữ 'Tokens sent')")

                # Tìm nút quay lại chính xác theo HTML bạn cung cấp
                # Logic: Tìm thẻ <button> mà bên trong có thẻ <span> chứa chữ "Get more tokens"
                try:
                    print("🔙 Đang tìm nút quay lại...")
                    back_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[./span[contains(text(), 'Get more tokens')]]"))
                    )
                    
                    time.sleep(5) # Nghỉ 1 nhịp
                    force_click(driver, back_btn)
                    print("🆗 Đã bấm nút quay lại.")
                
                except:
                    print("⚠️ Không bấm được nút quay lại -> Sẽ Refresh trang.")
                    driver.refresh()

                # Chờ ô input hiện ra lại
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Wallet address']"))
                )
                print("✨ Sẵn sàng cho ví mới.")

            except Exception as e:
                # Xử lý trường hợp Limit hoặc Lỗi khác
                if "Limit exceeded" in driver.page_source:
                    print("⚠️ BỊ LIMIT! -> F5 bỏ qua.")
                    driver.refresh()
                else:
                    print(f"⚠️ Lỗi chờ kết quả: {e}")
                    driver.refresh()
                time.sleep(5)

    except Exception as e:
        print(f"\n❌ LỖI HỆ THỐNG: {e}")

    finally:
        print("\n🛑 Đang đóng trình duyệt...")
        if driver:
            try: driver.service.process.kill()
            except: pass

if __name__ == "__main__":
    run_faucet_v18()