import csv
import json
import requests
from tqdm import tqdm
import os
from dotenv import load_dotenv

load_dotenv()

auth_key = os.getenv("DEEPL_API_KEY")

DEEPL_URL = "https://api-free.deepl.com/v2/translate"

LOCALES = {
    "fr": "fr_FR",
    "en": "en_GB",
    "es": "es_ES",
    "ar": "ar_SA"
}

# FIELDS_TO_TRANSLATE = ["name", "description", "action_name"]
FIELDS_TO_TRANSLATE = ["title", "description", "data"]

# input_csv = "bannieres_publicitaires_qg_dev.csv"
# output_json = "translations_bannieres_qg_dev.json"
input_csv = "informations_sondages_qg_dev.csv"
output_json = "translations_informations_qg_dev.json"


def translate_text(text, target_lang):
    if not text:
        return ""
    response = requests.post(
        DEEPL_URL,
        data={
            "auth_key": auth_key,
            "text": text,
            "target_lang": target_lang.upper()
        }
    )
    result = response.json()
    return result["translations"][0]["text"]


def main():
    # Load existing translations if the file already exists
    if os.path.exists(output_json):
        with open(output_json, encoding="utf-8") as f:
            translations = json.load(f)
    else:
        translations = []

    # Convert list to dict for quick lookup
    translations_dict = {
        (t["informations_id"], t["field"]): t["translations"]
        for t in translations
    }

    # Load CSV rows
    with open(input_csv, newline='', encoding="utf-8") as csvfile:
        reader = list(csv.DictReader(csvfile))

    # Estimate how many translations still need doing
    total_tasks = len(reader) * len(FIELDS_TO_TRANSLATE) * len(LOCALES)
    done_tasks = sum(
        len([loc for loc in LOCALES.values() if loc in translations_dict.get((row["id"], field), {})])
        for row in reader
        for field in FIELDS_TO_TRANSLATE
    )
    remaining_tasks = total_tasks - done_tasks

    with tqdm(total=remaining_tasks, desc="🔄 Translating", ncols=100) as pbar:
        for row in reader:
            informations_id = row["id"]

            for field in FIELDS_TO_TRANSLATE:
                original_text = row.get(field, "")

                key = (informations_id, field)

                if key not in translations_dict:
                    translations_dict[key] = {}

                for lang_code, locale in LOCALES.items():
                    if locale not in translations_dict[key]:
                        try:
                            translated = translate_text(original_text, lang_code)
                            translations_dict[key][locale] = translated
                        except:
                            print("Error translating", original_text, "in", lang_code)
                        pbar.update(1)

    # Rebuild the final list structure
    updated_translations = []
    for (informations_id, field), trans in translations_dict.items():
        updated_translations.append({
            "informations_id": informations_id,
            "field": field,
            "translations": trans
        })

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(updated_translations, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Translations updated in {output_json}")


if __name__ == "__main__":
    main()
