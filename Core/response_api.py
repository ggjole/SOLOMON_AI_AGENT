import requests as req
from dotenv import load_dotenv
import os
from pathlib import Path as P
import json
import random as rdm
load_dotenv(dotenv_path="Core/data/.env")

# KEY NAME PROVIDER: lm_studio, ollama
# KEY MODELS: model_name_used

DEBUG = True
COMMENT_CODE = '//'

# HELPER

# BACA FILE PROMPT
def _cleaner(file_path,random:bool=False):
    with open(file_path,mode='r',encoding='UTF-8') as f:
        main_content = [prompt for prompt in f.read().strip().startswith(COMMENT_CODE)]
    if random:
        file = rdm.choice(file_path)

# LISTING MODELS (FOR LOOKS)
def _listing_models(models:list,provider:str):
    for model in models:'\n-'.join(model)
    txt = f"""
MODELS YANG ANDA MILIKI DI {provider}:
{model if model else f'tidak terdapat model apapun pada {provider}'}
{'-'*20}
[MADE BY SOLOMON]
    """   
# DAPETIN SETTINGS
def _get_settings(which:int = 0):
    if which == 0:
        with open(f"{os.getcwd()}/user_settings/settings.json",mode='r',encoding='UTF-8') as f:
            data = json.load(f)
            return data
    else:
        with open(f"{os.getcwd()}/user_settings/mods.json",mode='r',encoding='UTF-8') as f:
            data = json.load(f)
            return data

# DAPETIN CUSTOM PROMPT
def _final_prompt(custom:bool,prompt:str,provider):
    path = P(f"{os.getcwd()}/Core/custom_prompt/")
    with open(path,mode='r',encoding='UTF-8') as f:
        data:str = f.read() + prompt
        
    # LM STUDIO PAYLOAD
    payload = {'role':'system','content': data if provider == 'lm_studio' and custom else prompt}
    # OLLAMA PAYLOAD
    payload = {'system':data if provider == 'lm_studio' and custom else prompt}

    return payload

# RESPONSE DECORATION
def _response_decoration(response:str,token_used:int=0):
    data = _get_settings()
    txt = f"""
FROM {data[model_name_used]}:
{response}
[MADE BY SOLOMON]
"""


# MAIN CODE

# DAPETIN MODELS
def get_models():
    data = _get_settings()
    provider = data['provider']
    models = req.get(f"{os.getenv('IP_PORT_SERVER')}{'/api/tags' if provider == 'ollama' else '/v1/models'}")
    all_models = models.json()['name' if provider == 'ollama' else 'id']
    return _listing_models(all_models,provider)

# DAPETIN RESPONSE DARI AI
def response(prompt:str,custom_prompt:bool=False):
    user_settings = _get_settings()
    payload = _final_prompt(custom_prompt,prompt,user_settings[provider])
    data = req.post(f"{os.getenv('IP_PORT_SERVER')}{'/api/tags' if user_settings[provider] == 'olama' else '/v1/models'}",json=payload)
    data.raise_for_status()
    response_txt = data.json()['choices'][0]['message']['content']
    return _response_decoration(response_txt)

