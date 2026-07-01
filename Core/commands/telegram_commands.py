from telegram.ext import ContextTypes as ct
from telegram import Update as up
import random as rdm
from pathlib import Path
import os
import json
import subprocess
from Core.response_api import Response_API

RESPONSE_API = Response_API()


USER_DATA = Path(f"{os.getcwd()}/Core/data/settings.json")
SYSTEM_PROMPT_MAPPING = Path(f"{os.getcwd()}/Core/data/mapping_system_prompt.json")
SYSTEM_PROMPT_DOWNLOAD_DIR = Path(f"{os.getcwd()}/Core/system_prompt/")

# BASIC COMMANDS (USER FRIENDLY)
class Basic_commands():
    def __init__(self):
        self.available_command = ['list','system_prompt']
        with open(SYSTEM_PROMPT_MAPPING,mode='r',encoding='UTF-8') as f:
            self.register_sys_prompt_path:dict = json.load(f)
        with open(USER_DATA,mode='r',encoding='UTF-8') as f:
            self.user_data:dict = json.load(f)
            
    async def welcome_txt(self,u:up,c:ct.DEFAULT_TYPE):
        all_text = rdm.choice([f'HALO {u.effective_user.first_name}!!',f'SELAMAT DATANG {u.effective_user.first_name} !!'])
        await u.message.reply_text(all_text)

    async def setings(self,u:up,c:ct.DEFAULT_TYPE):
        if not c.args:
            await u.message.reply_text(
                "Format: /setings <settings_name> [settings_value] [file_name]"
            )
            return
        settings_name = c.args[0] # SETTINGS NAME
        settings_value = c.args[1] if len(c.args) > 1 else None # SETTINGS VALUE
        self.file_name = c.args[2] if len(c.args) > 2 else None # buat dapetin file
        if settings_name not in self.available_command:
            await u.message.reply_text(f"SETTINGAN {settings_name} TIDAK ADA. SILAHKAN KETIK /settings list UNTUK MELIHAT SETTINGS YANG ADA.")
            return
        
        if settings_name == 'list':
            text = ''
            all_settings_name = list(self.user_data.keys())
            for idx,options_name in enumerate(all_settings_name,1):
                text += f"|[{idx}] {options_name} |\n"
            text = 'USER DATA ANDA CORRUPT, SAAT INI TIDAK ADA CARA UNTUK RECOVERY, JADI SILAHKAN HUBUNGI DEVELOPER: @SOLOMON_DEVELOPER' if text == '' else text
            await u.message.reply_text(text)
            return

        if settings_value is None:
            await u.message.reply_text(
                f"Value untuk {settings_name} belum diisi. "
                f"Format: /setings {settings_name} <value>"
            )
            return
        elif settings_name == 'system_prompt':
            await self._system_prompt_handler(u,c,mode=settings_value)
    
        self.user_data[settings_name] = settings_value
        with open(USER_DATA,mode='w',encoding='UTF-8') as f:
            self.user_data = json.dump(self.user_data,f,ensure_ascii=False,indent=4)
        return "BERHASIL DI UBAH."

    async def AI_Response(self,u:up,c:ct):
        msg = u.message.text
        feedback = RESPONSE_API.response(msg)
        await u.message.reply_text(feedback)
        return

    async def _system_prompt_handler(self,u:up,c:ct.DEFAULT_TYPE,mode):
        if mode == 'add':
            doc = u.message.document
            if not doc:
                await u.message.reply_text("TOLONG BERIKAN FILE PROMPT DENGAN FORMAT:\n FILE.TXT")
                return
            file = await c.bot.get_file(doc.file_name)
            for idx,file_name in enumerate(self.register_sys_prompt_path,1):
                idx+=1
                self.register_sys_prompt_path[idx] = file
            os.makedirs(SYSTEM_PROMPT_DOWNLOAD_DIR,exist_ok=True)
            await file.download_to_drive(custom_path=SYSTEM_PROMPT_DOWNLOAD_DIR)
            return await u.message.reply_text("BERHASIL DI TAMBAHKAN KE SISTEM.")

        elif mode == 'delete':
            files = SYSTEM_PROMPT_DOWNLOAD_DIR/self.register_sys_prompt_path.get(self.file_name)
            if files.exists():
                files.unlink()
            else:
                return 'FILE SUDAH TERHAPUS.'
        elif mode == 'edit':
            subprocess.run(['xdg-open',self.register_sys_prompt_path.get(self.file_name)],check=True)
        
        else:
            return f"MODE {mode} TIDAK TERSEDIA DI SISTEM INI."
        




    


# ADVANCE COMMANDS (NOT USER FRIENDLY)
class Advance_commands():
    def __init__(self):
        pass
    def info_app(self,u:up,c:ct.DEFAULT_TYPE):
        pass
    def change_provider(self,u:up,c:ct.DEFAULT_TYPE):
        pass
        

# DEV COMMANDS (FOR DEVELOPER)
class Dev_commands():
    def __init__(self):
        pass
    def get_a_fucking_error_logs(self,u:up,c:ct.DEFAULT_TYPE):
        pass
    def pull_request(self,u:up,c:ct.DEFAULT_TYPE):
        pass
    def give_issues_source_code(self,u:up,c:ct.DEFAULT_TYPE):
        pass
    def tracking_agent_node(self,u:up,c:ct.DEFAULT_TYPE):
        pass

