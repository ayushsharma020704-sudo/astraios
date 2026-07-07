import os
import google.genai as genai
from core.config import settings

client = genai.Client(api_key=settings.GOOGLE_AI_STUDIO_KEY)
models = [m.name for m in client.models.list() if 'flash' in m.name]
with open('models_flash.txt', 'w', encoding='utf-8') as f:
    for m in models:
        f.write(m + '\n')
