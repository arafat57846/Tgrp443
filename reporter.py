import os, time, platform
try:
    from telethon.sync import TelegramClient
except:
    os.system("pip install telethon")
from telethon.tl import types
from telethon import functions

# কালার কোড
rd, gn, lgn, yw, lrd, be, pe = '\033[00;31m', '\033[00;32m', '\033[01;32m', '\033[01;33m', '\033[01;31m', '\033[94m', '\033[01;35m'
cn, k, g = '\033[00;36m', '\033[90m', '\033[38;5;130m'

def re(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.001)

def clear():
    if 'Windows' in platform.uname():
        try: from colorama import init
        except: os.system("pip install colorama"); from colorama import init
        init()
        os.system("cls")
    else:
        os.system("clear")

# ব্যানার
banner = f"""{g}
  _____      __      _   _________     ____    
 (_   _)    /  \    / ) (_   _____)   / __ \   
   | |     / /\ \  / /    ) (___     / /  \ \  
   | |     ) ) ) ) ) )   (   ___)   ( ()  () ) 
   | |    ( ( ( ( ( (     ) (       ( ()  () ) 
  _| |__  / /  \ \/ /    (   )       \ \__/ /  
 /_____( (_/    \__/      \_/         \____/
"""
re(banner)
print(f"{lrd}Warning! This is a test reporter. Use responsibly.\n")

# মেথড লিস্ট আউটপুট
methods = [
    "Report Spam",
    "Reporter Other",
    "Reporter Violence",
    "Reporter Pornography",
    "Reporter Copyright",
    "Reporter Fake",
    "Reporter Geo Irrelevant",
    "Reporter Illegal Drugs",
    "Reporter Personal Details"
]

for i, m in enumerate(methods, 1):
    print(f"{lgn}{i}{lrd}  {gn}{m}{lrd}")

# একাউন্ট ইনফো
account_info = f"""{k}
 ____                             _               
|  _ \   ___  _ __    ___   _ __ | |_   ___  _ __ 
| |_) | / _ \| '_ \  / _ \ | '__|| __| / _ \| '__|
|  _ < |  __/| |_) || (_) || |   | |_ |  __/| |    {cn}Channel{k}
|_| \_\ \___|| .__/  \___/ |_|    \__| \___||_|   
             |_|   
[{lgn}+{lrd}] {gn}Channel : {lgn}@Esfelurm{lrd}
"""
clear()
re(account_info)

# Telegram Reporter Class
class TelegramReporter:
    def __init__(self):
        self.api_id = input(f"{lrd}[{lgn}+{lrd}] {gn}Enter Api id account: {g}")
        self.api_hash = input(f"{lrd}[{lgn}+{lrd}] {gn}Enter Api hash account: {g}")
        self.phone_number = input(f"{lrd}[{lgn}+{lrd}] {gn}Enter phone account: {g}")
        clear()
        re(account_info)
        print(f"{lrd}")
        self.method = input(f"{lrd}[{lgn}?{lrd}] {gn}Choose a method : {k}")
        self.channel_username = input(f"{lrd}[{lgn}+{lrd}] {gn}Enter username channel {k}")
        self.message_id = int(input(f"{lrd}[{lgn}+{lrd}] {gn}Enter Message ID to report: {k}"))
        self.number = int(input(f"{lrd}[{lgn}+{lrd}] {gn}Number of reports: {k}"))
        self.client = TelegramClient('session', self.api_id, self.api_hash)

    def report_channel(self):
        with self.client as client:
            client.connect()
            if not client.is_user_authorized():
                client.send_code_request(self.phone_number)
                client.sign_in(self.phone_number, input('Enter the code: '))
            try:
                channel_entity = client.get_entity(self.channel_username)
            except:
                print(f"{rd}Username does not exist")
                return

            # প্রতিটি মেথডের জন্য ম্যাসেজ ও reason সেট করা
            messages = {
                "1": ("This channel contains spam content.", types.InputReportReasonSpam(), "A spam report has been sent"),
                "2": (input(f"{lrd}[{lgn}+{lrd}] {gn}Enter your custom message: {g}"), types.InputReportReasonOther(), "An Other report has been sent"),
                "3": ("This channel contains violent content.", types.InputReportReasonViolence(), "A Violence report has been sent"),
                "4": ("This channel has pornographic content", types.InputReportReasonPornography(), "A Pornography report has been sent"),
                "5": ("Block this channel due to copyright", types.InputReportReasonCopyright(), "A Copyright report has been sent"),
                "6": ("Block this channel due to scam and impersonation", types.InputReportReasonFake(), "A Fake report has been sent"),
                "7": ("Block this channel due to irrelevant geo", types.InputReportReasonGeoIrrelevant(), "A Geo Irrelevant report has been sent"),
                "8": ("Block this channel because of Illegal Drugs", types.InputReportReasonIllegalDrugs(), "An Illegal Drugs report has been sent"),
                "9": ("Block this channel because of Personal Details", types.InputReportReasonPersonalDetails(), "A Personal Details report has been sent")
            }

            if self.method not in messages:
                print(f"{rd}Invalid method")
                return

            message_text, reason_type, print_msg = messages[self.method]

            for _ in range(self.number):
                client(functions.messages.ReportRequest(
                    peer=channel_entity,
                    id=[self.message_id],
                    reason=reason_type,
                    message=message_text
                ))
                print(f"{lrd}[{lgn}+{lrd}] {gn}{print_msg}")

            print(f"\n{k}End of reports!")

# চালানো
reporter = TelegramReporter()
reporter.report_channel()