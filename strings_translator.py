import xml.etree.ElementTree as ET
import deepl
import glob
import os
from dotenv import load_dotenv

load_dotenv()

auth_key = os.getenv("DEEPL_API_KEY")

deepl_client = deepl.DeepLClient(auth_key)


langs = ["en", "es", "ar"]
langs_map = {
    "en": "en-GB",
    "es": "ES",
    "ar": "AR"
}

files = glob.glob("strings/raw/*")

for file in files:
    for lang in langs:
        name = os.path.basename(file)
        tree = ET.parse(file)
        root = tree.getroot()

        strings = root.findall("string")
        entries_count = len(strings)
        for index, string_elem in enumerate(strings):
            text_to_translate = string_elem.text

            if text_to_translate and text_to_translate.strip():
                result = deepl_client.translate_text(text_to_translate, target_lang=langs_map[lang])
                translated_text = result.text

                string_elem.text = translated_text

                percentage = int(100 * (index + 1) / entries_count)
                print(f"{percentage:02d}% Translated: {text_to_translate} → {translated_text}")
        
        tree.write("strings/" + lang + "/" + name, encoding="utf-8", xml_declaration=True)

