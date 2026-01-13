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

def random_sleep(min_s=1, max_s=3):
    time.sleep(random.uniform(min_s, max_s))

def human_type(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.02, 0.1))

def run_faucet_loop():
    # 1. Đọc dữ liệu
    try:
        with open(wallet_file, 'r') as f:
            wallets = [line.strip() for line in f if line.strip()]
        print(f"📂 Tìm thấy {len(wallets)} ví.")
    except FileNotFoundError:
        print("❌ Thiếu file wallet.txt")
        return

    proxies = []
    if os.path.exists(proxy_file):
        with open(proxy_file, 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]

    # 2. Vòng lặp
    for i, wallet_address in enumerate(wallets):
        print(f"\n{'='*40}")
        print(f"🔄 VÍ SỐ {i+1}: {wallet_address[:10]}...")
        
        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        
        if proxies:
            curr_proxy = proxies[i % len(proxies)]
            options.add_argument(f'--proxy-server={curr_proxy}')
            print(f"🌐 Proxy: {curr_proxy}")

        driver = None
        try:
            driver = uc.Chrome(options=options)
            wait = WebDriverWait(driver, 30) # Tăng thời gian chờ lên 30s
            
            driver.get(url)
            time.sleep(5)

            # --- BƯỚC 1: XỬ LÝ COOKIE ---
            try:
                cookie_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept Cookies')]"))
                )
                cookie_btn.click()
                print("🍪 Đã bấm tắt Cookie.")
                time.sleep(3) 
            except:
                print("⏩ Không thấy Cookie, bỏ qua.")

            # --- BƯỚC 2: NHẬP VÍ ---
            print("✍️ Đang nhập ví...")
            input_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Wallet address']")))
            
            # Dùng JS Click để tránh bị che
            driver.execute_script("arguments[0].click();", input_field)
            
            input_field.send_keys(Keys.CONTROL + "a")
            input_field.send_keys(Keys.DELETE)
            time.sleep(0.5)
            
            human_type(input_field, wallet_address)
            time.sleep(1)

            # --- BƯỚC 3: BẤM GỬI ---
            print("👆 Đang bấm nút Send...")
            send_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Send 1 USDC')]")))
            
            # Scroll và Click bằng JS
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", send_button)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", send_button)
            print("🚀 Đã thực hiện lệnh Click!")

            # --- BƯỚC 4: CHỜ KẾT QUẢ (QUAN TRỌNG) ---
            print("⏳ Đang chờ xác nhận từ web (Tối đa 20s)...")
            
            # Chờ một trong 2 trường hợp: Thành công HOẶC Lỗi Limit
            try:
                WebDriverWait(driver, 20).until(
                    EC.or_(
                        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Get more tokens')]")),
                        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Limit Exceeded')]"))
                    )
                )
                
                # Phân loại kết quả
                page_source = driver.page_source
                if "Limit Exceeded" in page_source:
                    print("❌ KẾT QUẢ: Thất bại do giới hạn IP (Limit Exceeded).")
                else:
                    print("✅ KẾT QUẢ: Gửi thành công!")
                    driver.save_screenshot(f"success_{i+1}.png")
                    
            except Exception as e:
                print("⚠️ Không thấy thông báo thành công (Có thể web lag hoặc chưa hiện).")

            # --- [TÍNH NĂNG MỚI] TREO MÁY XEM KẾT QUẢ ---
            print(f"👀 Treo máy 20 giây để bạn kiểm tra màn hình...")
            time.sleep(20) 

        except Exception as e:
            print(f"❌ LỖI NGHIÊM TRỌNG: {e}")
            print("👀 Giữ nguyên màn hình lỗi 30 giây...")
            time.sleep(30) 
        
        finally:
            print("🛑 Đang đóng trình duyệt...")
            try:
                if driver:
                    driver.quit()
            except:
                pass
            
            print("💤 Nghỉ 5 giây trước khi qua ví mới...")
            time.sleep(5)

if __name__ == "__main__":
    run_faucet_loop()