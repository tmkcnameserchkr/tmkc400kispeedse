import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import uuid
import hashlib
import os
import json
import urllib.parse
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import database as db
import requests

st.set_page_config(
    page_title="E2E BY SMART DEVIL KING",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ────────────────────────────────────────────────
# ROYAL / KINGLY THEME CSS (Updated)
# ────────────────────────────────────────────────
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Great+Vibes&family=Playfair+Display:wght@400;700&display=swap');

    * {
        font-family: 'Playfair Display', serif;
    }

    .stApp {
        background-image: linear-gradient(rgba(20, 0, 40, 0.88), rgba(40, 0, 80, 0.78)),
                          url('https://i.ibb.co/0mQfX0b/dark-royal-purple-velvet-texture.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .main .block-container {
        background: rgba(30, 10, 60, 0.68);
        backdrop-filter: blur(12px);
        border-radius: 22px;
        padding: 32px;
        border: 2px solid rgba(255, 215, 0, 0.38);
        box-shadow: 0 12px 45px rgba(255, 215, 0, 0.18),
                    inset 0 0 28px rgba(255, 215, 0, 0.10);
    }

    .main-header {
        background: linear-gradient(135deg, #1a0033, #4b0082, #2a0055);
        border: 2px solid #ffd700;
        border-radius: 25px;
        padding: 2.4rem;
        text-align: center;
        margin-bottom: 2.8rem;
        box-shadow: 0 18px 55px rgba(0, 0, 0, 0.75),
                    0 0 35px rgba(255, 215, 0, 0.30);
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: "👑";
        position: absolute;
        top: -40px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 6.5rem;
        opacity: 0.14;
        color: #ffd700;
    }

    .main-header h1 {
        background: linear-gradient(90deg, #ffd700, #ffeb3b, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Cinzel Decorative', cursive;
        font-size: 3.4rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 0 25px rgba(255, 215, 0, 0.7);
    }

    .main-header p {
        color: #d4af37;
        font-family: 'Great Vibes', cursive;
        font-size: 1.8rem;
        margin-top: 0.7rem;
        letter-spacing: 1.8px;
    }

    .stButton>button {
        background: linear-gradient(45deg, #b8860b, #ffd700, #daa520);
        color: #1a0033;
        border: 2px solid #b8860b;
        border-radius: 16px;
        padding: 1rem 2.4rem;
        font-family: 'Cinzel Decorative', cursive;
        font-weight: 700;
        font-size: 1.2rem;
        transition: all 0.4s ease;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.45);
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-5px) scale(1.04);
        box-shadow: 0 15px 40px rgba(255, 215, 0, 0.75);
        background: linear-gradient(45deg, #ffd700, #ffeb3b, #ffd700);
    }

    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stNumberInput>div>div>input {
        background: rgba(40, 20, 80, 0.75);
        border: 2px solid #b8860b;
        border-radius: 14px;
        color: #ffd700;
        padding: 1rem;
        font-size: 1.1rem;
    }

    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: #d4af37aa;
    }

    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #ffd700;
        box-shadow: 0 0 0 4px rgba(255, 215, 0, 0.35);
        background: rgba(50, 30, 90, 0.85);
    }

    label {
        color: #ffd700 !important;
        font-weight: 600 !important;
        font-size: 1.15rem !important;
        text-shadow: 1px 1px 4px #000;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: rgba(30, 10, 60, 0.65);
        border-radius: 16px;
        padding: 10px;
        border: 1px solid #b8860b;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(75, 0, 130, 0.55);
        color: #d4af37;
        border-radius: 12px;
        padding: 14px 26px;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #b8860b, #ffd700);
        color: #1a0033;
    }

    [data-testid="stMetricValue"] {
        color: #ffd700;
        font-size: 2.6rem;
        font-weight: 700;
        text-shadow: 0 0 18px rgba(255, 215, 0, 0.7);
    }

    [data-testid="stMetricLabel"] {
        color: #d4af37;
        font-weight: 500;
    }

    .console-section {
        background: rgba(20, 0, 40, 0.75);
        border: 2px solid #b8860b;
        border-radius: 16px;
        padding: 22px;
        margin-top: 28px;
    }

    .console-header {
        color: #ffd700;
        font-family: 'Cinzel Decorative', cursive;
        text-shadow: 0 0 18px #ffd700bb;
        margin-bottom: 18px;
    }

    .console-output {
        background: #0f001a;
        border: 2px solid #4b0082;
        border-radius: 14px;
        padding: 18px;
        color: #ffeb3b;
        font-family: 'Courier New', monospace;
        font-size: 13.5px;
        max-height: 480px;
        overflow-y: auto;
    }

    .console-line {
        background: rgba(75, 0, 130, 0.25);
        border-left: 4px solid #ffd700;
        padding: 9px 14px;
        margin: 7px 0;
        color: #ffeb3b;
    }

    .footer {
        background: rgba(30, 10, 60, 0.75);
        border-top: 3px solid #b8860b;
        color: #d4af37;
        font-family: 'Great Vibes', cursive;
        font-size: 1.5rem;
        padding: 2.8rem;
        text-shadow: 1px 1px 5px #000;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

ADMIN_PASSWORD = "DEVIL_KING"
WHATSAPP_NUMBER = "9201776631"
APPROVAL_FILE = "approved_keys.json"
PENDING_FILE = "pending_approvals.json"
USERS_FILE = "users.json"

# ────────────────────────────────────────────────
# TELEGRAM NOTIFICATION SETTINGS
# ────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = ""
ADMIN_CHAT_ID = "9201776631"

def send_to_telegram(message):
    if not TELEGRAM_BOT_TOKEN or not ADMIN_CHAT_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": ADMIN_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        requests.post(url, data=payload, timeout=10)
    except:
        pass

def generate_user_key(username, password):
    combined = f"{username}:{password}"
    key_hash = hashlib.sha256(combined.encode()).hexdigest()[:8].upper()
    return f"KEY-{key_hash}"

def load_approved_keys():
    if os.path.exists(APPROVAL_FILE):
        try:
            with open(APPROVAL_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_approved_keys(keys):
    with open(APPROVAL_FILE, 'w') as f:
        json.dump(keys, f, indent=2)

def load_pending_approvals():
    if os.path.exists(PENDING_FILE):
        try:
            with open(PENDING_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_pending_approvals(pending):
    with open(PENDING_FILE, 'w') as f:
        json.dump(pending, f, indent=2)

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def send_whatsapp_message(user_name, approval_key):
    message = f"👑 HELLO DEVIL KING SIR PLEASE 👑\nMy name is {user_name}\nPlease approve my key:\n🔑 {approval_key}"
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://api.whatsapp.com/send?phone={WHATSAPP_NUMBER}&text={encoded_message}"
    return whatsapp_url

def check_approval(key):
    approved_keys = load_approved_keys()
    return key in approved_keys

# Session state initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_key' not in st.session_state:
    st.session_state.user_key = None
if 'key_approved' not in st.session_state:
    st.session_state.key_approved = False
if 'approval_status' not in st.session_state:
    st.session_state.approval_status = 'not_requested'
if 'automation_running' not in st.session_state:
    st.session_state.automation_running = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0
if 'whatsapp_opened' not in st.session_state:
    st.session_state.whatsapp_opened = False

class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

def log_message(msg, automation_state=None):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    if automation_state:
        automation_state.logs.append(formatted_msg)
    else:
        if 'logs' in st.session_state:
            st.session_state.logs.append(formatted_msg)

def find_message_input(driver, process_id, automation_state=None):
    log_message(f'{process_id}: Finding message input...', automation_state)
    time.sleep(10)
    
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
    except Exception:
        pass
    
    message_input_selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        'div[aria-label*="Message" i][contenteditable="true"]',
        'div[contenteditable="true"][spellcheck="true"]',
        '[role="textbox"][contenteditable="true"]',
        'textarea[placeholder*="message" i]',
        'div[aria-placeholder*="message" i]',
        'div[data-placeholder*="message" i]',
        '[contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ]
    
    for idx, selector in enumerate(message_input_selectors):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                try:
                    is_editable = driver.execute_script("""
                        return arguments[0].contentEditable === 'true' ||
                               arguments[0].tagName === 'TEXTAREA' ||
                               arguments[0].tagName === 'INPUT';
                    """, element)
                    
                    if is_editable:
                        try:
                            element.click()
                            time.sleep(0.5)
                        except:
                            pass
                        return element
                except Exception:
                    continue
        except Exception:
            continue
    return None

def setup_browser(automation_state=None):
    log_message('Setting up Chrome browser...', automation_state)
    
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--window-size=1920,1080')
    
    chromium_paths = [
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/usr/bin/google-chrome',
        '/usr/bin/chrome'
    ]
    
    for chromium_path in chromium_paths:
        if Path(chromium_path).exists():
            chrome_options.binary_location = chromium_path
            log_message(f'Found Chromium at: {chromium_path}', automation_state)
            break
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1920, 1080)
        log_message('Chrome browser setup completed!', automation_state)
        return driver
    except Exception as error:
        log_message(f'Browser setup failed: {error}', automation_state)
        raise error

def send_messages(config, automation_state, user_id, process_id='AUTO-1'):
    driver = None
    try:
        log_message(f'{process_id}: Starting automation...', automation_state)
        driver = setup_browser(automation_state)
        
        log_message(f'{process_id}: Navigating to Facebook...', automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(8)
        
        if config['cookies'] and config['cookies'].strip():
            log_message(f'{process_id}: Adding cookies...', automation_state)
            cookie_array = config['cookies'].split(';')
            for cookie in cookie_array:
                cookie_trimmed = cookie.strip()
                if cookie_trimmed:
                    first_equal_index = cookie_trimmed.find('=')
                    if first_equal_index > 0:
                        name = cookie_trimmed[:first_equal_index].strip()
                        value = cookie_trimmed[first_equal_index + 1:].strip()
                        try:
                            driver.add_cookie({
                                'name': name,
                                'value': value,
                                'domain': '.facebook.com'
                            })
                        except Exception as e:
                            log_message(f'{process_id}: Could not add cookie {name}: {e}', automation_state)
        
        driver.refresh()
        time.sleep(6)
        
        target_url = config.get('profile_link', 'https://www.facebook.com/')
        log_message(f'{process_id}: Navigating to target: {target_url}', automation_state)
        driver.get(target_url)
        time.sleep(8)
        
        message_input = find_message_input(driver, process_id, automation_state)
        
        if not message_input:
            log_message(f'{process_id}: Could not find message input field!', automation_state)
            return False
        
        messages = config.get('messages', ['Hello!'])
        delay = config.get('delay', 5)
        message_limit = config.get('message_limit', 10)
        
        for i in range(message_limit):
            if not automation_state.running:
                log_message(f'{process_id}: Automation stopped by user', automation_state)
                break
            
            message = messages[i % len(messages)]
            log_message(f'{process_id}: Sending message {i+1}: {message[:50]}...', automation_state)
            
            try:
                message_input.clear()
                time.sleep(1)
                message_input.send_keys(message)
                time.sleep(1)
                message_input.send_keys("\n")
                
                automation_state.message_count += 1
                log_message(f'{process_id}: Message {i+1} sent!', automation_state)
                time.sleep(delay)
                
            except Exception as e:
                log_message(f'{process_id}: Error: {e}', automation_state)
                break
        
        return True
        
    except Exception as e:
        log_message(f'{process_id}: Error: {e}', automation_state)
        return False
    finally:
        if driver:
            driver.quit()

# Main App UI
st.markdown("""
<div class="main-header">
    <h1>👑 E2E BY SMART DEVIL KING 👑</h1>
    <p>Royal Automation System</p>
</div>
""", unsafe_allow_html=True)

# Login/Signup Section
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["🔐 LOGIN", "📝 SIGN UP"])
    
    with tab1:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 👑 Existing User Login")
            username = st.text_input("Username", placeholder="Enter your username", key="login_username")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
            login_btn = st.button("👑 Login", use_container_width=True, key="login_btn")
            
            if login_btn:
                if username and password:
                    user_key = generate_user_key(username, password)
                    st.session_state.user_key = user_key
                    st.session_state.username = username
                    
                    if check_approval(user_key):
                        st.session_state.logged_in = True
                        st.session_state.key_approved = True
                        st.success("👑 Welcome to the Kingdom! Access granted!")
                        st.rerun()
                    else:
                        st.session_state.approval_status = 'pending'
                        st.warning("⚠️ Your key is pending approval! Please sign up first or request approval.")
                else:
                    st.error("Please enter both username and password!")
    
    with tab2:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 📝 Create New Account")
            new_username = st.text_input("Choose Username", placeholder="Enter unique username", key="signup_username")
            new_password = st.text_input("Choose Password", type="password", placeholder="Enter strong password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="confirm_password")
            
            signup_btn = st.button("📝 Create Account", use_container_width=True, key="signup_btn")
            
            if signup_btn:
                if new_username and new_password:
                    if new_password == confirm_password:
                        # Check if username already exists
                        pending = load_pending_approvals()
                        approved = load_approved_keys()
                        all_users = {**pending, **approved}
                        
                        user_exists = False
                        for key, data in all_users.items():
                            if isinstance(data, dict) and data.get('username') == new_username:
                                user_exists = True
                                break
                        
                        if not user_exists:
                            user_key = generate_user_key(new_username, new_password)
                            st.session_state.user_key = user_key
                            st.session_state.username = new_username
                            
                            # Save to pending approvals
                            pending = load_pending_approvals()
                            pending[user_key] = {
                                'username': new_username,
                                'timestamp': time.time(),
                                'status': 'pending'
                            }
                            save_pending_approvals(pending)
                            
                            st.session_state.approval_status = 'pending'
                            st.success(f"✅ Account created successfully!")
                            st.info(f"🔑 Your Key: `{user_key}`")
                            st.info("📱 Please request approval from admin using the button below!")
                            
                            # Show WhatsApp approval button
                            whatsapp_url = send_whatsapp_message(new_username, user_key)
                            components.html(f"""
                            <script>
                                window.open('{whatsapp_url}', '_blank');
                            </script>
                            """, height=0)
                            
                            st.balloons()
                        else:
                            st.error("❌ Username already exists! Please choose another name.")
                    else:
                        st.error("❌ Passwords do not match!")
                else:
                    st.error("Please fill all fields!")

# Admin Panel in Sidebar
with st.sidebar:
    st.markdown("## 👑 Royal Admin Panel")
    admin_password = st.text_input("Admin Access Key", type="password", placeholder="Enter master key")
    
    if admin_password == ADMIN_PASSWORD:
        st.success("✅ Admin Access Granted!")
        
        pending = load_pending_approvals()
        approved = load_approved_keys()
        
        st.markdown("### 📋 Pending Approvals")
        if pending:
            for key, data in pending.items():
                st.markdown(f"**User:** {data.get('username', 'Unknown')}")
                st.markdown(f"**Key:** `{key}`")
                if st.button(f"✅ Approve", key=f"approve_{key}"):
                    approved[key] = data
                    save_approved_keys(approved)
                    if key in pending:
                        del pending[key]
                        save_pending_approvals(pending)
                    st.success(f"Approved user: {data.get('username', 'user')}!")
                    st.rerun()
                st.markdown("---")
        else:
            st.info("No pending approvals")
        
        st.markdown("### ✅ Approved Users")
        if approved:
            for key, data in approved.items():
                st.markdown(f"• {data.get('username', 'Unknown')}: `{key}`")
        else:
            st.info("No approved users yet")

# Main App after login
if st.session_state.logged_in:
    if not st.session_state.key_approved and st.session_state.approval_status == 'pending':
        st.warning("⚠️ Your access key is pending approval!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📱 Request Approval via WhatsApp", use_container_width=True):
                whatsapp_url = send_whatsapp_message(st.session_state.username, st.session_state.user_key)
                components.html(f"""
                <script>
                    window.open('{whatsapp_url}', '_blank');
                </script>
                """, height=0)
                st.success("WhatsApp opened! Send message to admin.")
        
        with col2:
            if st.button("🔄 Check Approval Status", use_container_width=True):
                if check_approval(st.session_state.user_key):
                    st.session_state.key_approved = True
                    st.session_state.logged_in = True
                    st.success("✅ Your key has been approved! Welcome!")
                    st.rerun()
                else:
                    st.info("Still pending approval. Please wait for admin.")
    
    elif st.session_state.key_approved:
        st.success(f"👑 Welcome {st.session_state.username}! Full access granted.")
        
        with st.expander("⚙️ Automation Configuration", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                profile_link = st.text_input("🔗 Facebook Profile Link", placeholder="https://www.facebook.com/username")
                cookies = st.text_area("🍪 Facebook Cookies", placeholder="c_user=123456; xs=789abc;...")
            
            with col2:
                message_input_area = st.text_area("💬 Messages (one per line)", placeholder="Hello!\nHow are you?\nNice to meet you!", height=150)
                delay = st.number_input("⏱️ Delay (seconds)", min_value=1, max_value=60, value=5)
                message_limit = st.number_input("📨 Max messages", min_value=1, max_value=100, value=10)
        
        messages = [msg.strip() for msg in message_input_area.split('\n') if msg.strip()]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if not st.session_state.automation_running:
                if st.button("🚀 Start Automation", use_container_width=True):
                    if profile_link and cookies and messages:
                        config = {
                            'profile_link': profile_link,
                            'cookies': cookies,
                            'messages': messages,
                            'delay': delay,
                            'message_limit': message_limit
                        }
                        
                        st.session_state.automation_state.running = True
                        st.session_state.automation_state.logs = []
                        st.session_state.automation_state.message_count = 0
                        st.session_state.automation_running = True
                        
                        def run_automation():
                            send_messages(config, st.session_state.automation_state, st.session_state.user_id)
                            st.session_state.automation_state.running = False
                            st.session_state.automation_running = False
                        
                        thread = threading.Thread(target=run_automation)
                        thread.daemon = True
                        thread.start()
                        
                        st.rerun()
                    else:
                        st.error("Please fill all required fields!")
            else:
                if st.button("🛑 Stop Automation", use_container_width=True):
                    st.session_state.automation_state.running = False
                    st.session_state.automation_running = False
                    st.rerun()
        
        with col2:
            if st.button("🗑️ Clear Logs", use_container_width=True):
                st.session_state.automation_state.logs = []
                st.rerun()
        
        with col3:
            st.metric("📊 Messages Sent", st.session_state.automation_state.message_count)
        
        st.markdown("### 📟 Console Output")
        if st.session_state.automation_state.logs:
            for log in st.session_state.automation_state.logs[-50:]:
                st.text(log)
        else:
            st.info("No logs yet. Start automation to see output...")
        
        if st.session_state.automation_running:
            time.sleep(1)
            st.rerun()

# Footer
st.markdown("""
<div class="footer" style="text-align: center; margin-top: 50px;">
    <p>👑 Powered by SMART DEVIL KING | Royal Automation System 👑</p>
</div>
""", unsafe_allow_html=True)
