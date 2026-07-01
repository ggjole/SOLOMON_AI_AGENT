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
SYSTEM_PROMPT_DOWNLOAD_DIR = Path(f"{os.getcwd()}/Core/system_prompt/")

# BASIC COMMANDS (USER FRIENDLY)
class Basic_commands():
    def __init__(self):
        pass
            
    def _overwrite(self,keys:str,value:str):
        with open(USER_DATA,mode='r',encoding='UTF-8') as f:
            self.user_data:dict = json.load(f)
        self.user_data[keys] = value
        with open(USER_DATA,'w',encoding='utf-8') as f:
            json.dump(self.user_data)


    async def welcome_txt(self,u:up,c:ct.DEFAULT_TYPE):
        all_text = rdm.choice([f'HALO {u.effective_user.first_name}!!',f'SELAMAT DATANG {u.effective_user.first_name} !!'])
        await u.message.reply_text(all_text)

    async def AI_Response(self,u:up,c:ct.DEFAULT_TYPE):
        msg = u.message.text
        feedback = RESPONSE_API.response(msg)
        await u.message.reply_text(feedback)
        return

    async def settings(self,u:up,c:ct.DEFAULT_TYPE):
        settings_name = c.args[0]
        settings_value = c.args[1] if len(c.args) > 1 else None
        with_file = u.message.document if u.message.document is not None else None
        
        if settings_name == 'list' :
            txt = 'SETTINGS:\n'
            for idx,settings in enumerate(self.settings):
                txt+=f'[{idx}] | {settings}\n'
            await u.message.reply_text(txt)
            return
        elif settings_name == 'system_prompt':
            self.settings_handlers('sys_prompt')
        
        # OVERWRITE
        self._overwrite(settings_name,settings_value)
        await u.message.reply_text("BERHASIL DIUBAH.")
        return

    async def settings_handlers(self,u:up,c:ct.DEFAULT_TYPE,type_of_settings:str,arguments:str):
        if type_of_settings == 'sys_prompt':
            if arguments == 'add':
                doc = u.message.document
                given_files = await c.bot.get_file(doc.id)
                await given_files.download_to_drive(SYSTEM_PROMPT_DOWNLOAD_DIR/doc.file_name)
                self._overwrite("system_prompt_used",SYSTEM_PROMPT_DOWNLOAD_DIR/doc.file_name)
                await u.message.reply_text("BERHASIL DI TAMBAHKAN.")
                return
            elif arguments == 'remove':
                if self.user_data.get('system_prompt_used').exist():
                    self.user_data.get('system_prompt_used').unlink()
                    await u.message.reply_text('BERHASIL DIHAPUS.')
                    return
                else:
                    await u.message.reply_text('SYSTEM PROMPT SUDAH TERHAPUS DARI PERANGKAT ANDA.')
                    return
            elif arguments == 'edit':
                current = self.user_data.get("system_prompt_used")
                if not current or not Path(current).exists():
                    await u.message.reply_text("BELUM ADA SYSTEM PROMPT YANG AKTIF.")
                    return
                subprocess.run(["xdg-open", current], check=True)
                await u.message.reply_text("FILE DIBUKA UNTUK DIEDIT.")

                    
                    



        



    


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

