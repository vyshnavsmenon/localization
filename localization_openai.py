import json
import os
import time
import requests
import html
import random

# Configuration
BASE_LANG_FILE = 'assets/translations/en-GB.json'
TARGET_LANGS = ['ar', 'bg', 'cs', 'da', 'de', 'el', 'es', 'fi', 'fr', 'he', 'hi', 'hu', 'id', 'it', 'ja', 'ko', 'ms', 'nb', 'nl', 'pl', 'pt', 'ro', 'ru', 'sv', 'th', 'tl', 'tr', 'uk', 'vi', 'zh']  # All available locales
OUTPUT_DIR = 'assets/translations'

# Translation using direct API call to avoid issues with googletrans library
def translate_text(text, target_lang):
    if not text or text.strip() == '':
        return text
    
    try:
        # Add a delay to avoid rate limiting (randomized between 0.5 and 1.5 seconds)
        time.sleep(random.uniform(0.5, 1.5))
        
        # Use the free Google Translate API endpoint
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "en",  # Source language
            "tl": target_lang,  # Target language
            "dt": "t",  # Return translated text
            "q": text  # Text to translate
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            # Parse the response
            result = response.json()
            translated_text = ''
            # Extract all translated parts
            for part in result[0]:
                if part[0]:
                    translated_text += part[0]
            
            # Unescape HTML entities
            translated_text = html.unescape(translated_text)
            print(f"Translated '{text}' → '{translated_text}'")
            return translated_text
        else:
            print(f"Translation request failed with status code {response.status_code} for '{text}'")
            return text
    except Exception as e:
        print(f"Translation failed for '{text}' to '{target_lang}': {e}")
        return text  # fallback to original

def load_base_language_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_existing_translations(lang_code):
    """Load existing translations for a language if available"""
    try:
        file_path = os.path.join(OUTPUT_DIR, f"{lang_code}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading existing translations for {lang_code}: {e}")
    return {}

def translate_dict(base_dict, target_lang, existing_translations=None):
    """Translate only fields that don't already have translations"""
    if existing_translations is None:
        existing_translations = {}
    
    translated = {}
    for key, value in base_dict.items():
        # Check if this key already has a translation
        if key in existing_translations:
            if isinstance(value, dict) and isinstance(existing_translations[key], dict):
                # Recursively merge nested dictionaries
                translated[key] = translate_dict(value, target_lang, existing_translations[key])
            else:
                # Use existing translation
                translated[key] = existing_translations[key]
                print(f"Using existing translation for '{key}'")
        else:
            # No existing translation, create a new one
            if isinstance(value, dict):
                translated[key] = translate_dict(value, target_lang, {})
            elif isinstance(value, str):
                translated[key] = translate_text(value, target_lang)
            else:
                translated[key] = value
    return translated

def save_translation_file(lang_code, data):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    file_path = os.path.join(OUTPUT_DIR, f"{lang_code}.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    base_data = load_base_language_file(BASE_LANG_FILE)
    
    for lang in TARGET_LANGS:
        print(f"\nProcessing {lang}...")
        
        # Load existing translations if available
        existing_translations = load_existing_translations(lang)
        if existing_translations:
            print(f"Found existing translations for {lang}")
        
        # Only translate what's missing
        translated_data = translate_dict(base_data, lang, existing_translations)
        
        # Save the updated translations
        save_translation_file(lang, translated_data)
        print(f"\n{lang}.json saved.")
        
        # Add a delay between languages to avoid rate limiting
        time.sleep(2)

if __name__ == '__main__':
    main()