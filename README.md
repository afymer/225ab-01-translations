## Configuration
Pour la configuration il suffit d'ajouter dans un fichier .env:
- DEEPL_API_KEY=XXX
- matchmaking_root="/XXX/YYY/.../matchmaking"
- boxer_root="~/XXX/YYY/.../boxer-2"

Ces variables doivent être des variables d'environnement pour l'utilisation des scripts bash, un script `set_env.sh` est fourni pour n'avoir qu'une commande à écrire.

Création d'un environnement virtuel (`python -m venv .venv`, activé avec `source ./.venv/bin/activate` sous linux).

Installation des dépendences: `pip install -r requirements.txt`

## Utilisation
Plusieurs scripts bash:
- `sh scraper_po.sh`: récupérer les fichiers .po du qg (penser à les générer avec gettext et mettre à jour avec msgmerge)
- `sh scraper_strings.sh`: récupérer les fichiers strings de l'app android
- `sh save_po.sh`: réécrire les fichiers .po après traduction (penser à les compiler en .mo)
- `sh save_strings.sh`: réécrire les fichiers strings après traduction

Plusieurs scripts python:
- `python generate_sql.py`: génère le SQL pour insérer directement les traductions dynamiques dans la BDD (temporaire, ne sera pas utilisé in fine)
- `python po_translator.py`: traduit avec DeepL les fichiers .po
- `python strings_translator.py`: traduit avec DeepL les fichiers strings
- `python translate_csv.py`: traduit le CSV exporté de la BDD et génère un json correspondant, destiné à être utilisé en entrée de `generate_sql.py`
