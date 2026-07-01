import requests as req
from dotenv import load_dotenv
import os
from pathlib import Path as P
import json
import random as rdm
load_dotenv(dotenv_path="Core/data/.env")

# KEY NAME PROVIDER: lm_studio, ollama
# KEY MODELS: model_used

DEBUG = True

CUSTOM_PROMPT = P(f"{os.getcwd()}/Core/custom_prompt/")
USER_SETTINGS = P(f"{os.getcwd()}/Core/data/settings.json")
MODS_SETTINGS = P(f"{os.getcwd()}/Core/data/mods.json")

class Response_API():
    def __init__(self):
        with open(USER_SETTINGS,mode='r',encoding='UTF-8') as f:
            self.user_data:dict = json.load(f)

        self.provider:str = self.user_data.get('provider')
        
    # HELPER
    def list_of_models(self,models:list):
        txt = f'YOUR ALL MODELS IN {self.provider.upper()}:\n'
        for idx,model in enumerate(model,1):
            txt += f"| [{idx}] {model}\n"
        return txt.join('\n[MADE BY SOLOMON DEV]')

    def final_payload(self,prompt:str):
        sys_prompt = self.user_data.get('system_prompt')
        custom_prompt = self.user_data.get('custom_prompt')
        combine = "\n\n".join(
            txt for txt in (sys_prompt,custom_prompt,prompt) if txt
        )
        # OLLAMA
        if self.provider == 'ollama':
            payload = {"role": "system", "content": combine }

        # LM STUDIO
        else:
            payload = {"role":"assistant","content":combine}
        return payload
        
    # MAIN CODE

    # DAPETIN MODELS
    def get_models(self):
        models = req.get(f"{os.getenv('IP_PORT_SERVER')}{'/api/tags' if self.provider == 'ollama' else '/v1/models'}")
        all_models = models.json()['name' if provider == 'ollama' else 'id']
        return self.list_of_models([all_models])
    
    # DAPETIN RESPONSE DARI AI
    def response(self,prompt:str):
        try:
            data = req.post(url=f"{os.getenv('IP_PORT_SERVER')}{'/api/tags' if self.user_data.get('provider') == 'olama' else '/v1/models'}",json=self.final_payload(prompt))
            data.raise_for_status()
            response_txt = data.json()['choices'][0]['message']['content']
        except req.ConnectTimeout:
            return 'KENA TIMEOUT. COBA LAGI.'
        except req.ConnectionError:
            return "KONEKSI ERROR. SILAHKAN CEK LM STUDIO / OLLAMA LU. KEKNYA MATI DAH."
        return response_txt
    
    