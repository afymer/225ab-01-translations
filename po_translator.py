import polib
import deepl
from dotenv import load_dotenv

load_dotenv()

auth_key = os.getenv("DEEPL_API_KEY")
deepl_client = deepl.DeepLClient(auth_key)

langs = ["en_GB", "es_ES", "ar_SA"]
langs_map = {
    "en_GB": "en-GB",
    "es_ES": "ES",
    "ar_SA": "AR"
}

for lang in langs:
    file = "po/source/messages_" + lang + ".po"
    print("Translating:", file)
    po = polib.pofile(file)

    entries_to_translate = po.untranslated_entries() + po.fuzzy_entries()
    entries_count = len(entries_to_translate)

    for index, entry in enumerate(entries_to_translate):
        text_to_translate = entry.msgid

        result = deepl_client.translate_text(
            text_to_translate, 
            target_lang=langs_map[lang]
        )

        translated_text = result.text
        entry.msgstr = translated_text

        # If it was fuzzy, clear the fuzzy flag (since now it's retranslated)
        if "fuzzy" in entry.flags:
            entry.flags.remove("fuzzy")

        percentage = int(100 * (index + 1) / entries_count)
        print(f"{percentage:02d}% Translated: {entry.msgid} → {entry.msgstr}")

    po.save("po/translated/messages_" + lang + ".po")
