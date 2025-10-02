import json
from tqdm import tqdm

def main():
    input_json = "translations_informations_qg_dev.json"
    output_sql = "insert_translations_informations_qg_dev.sql"
    table = "informations_sondages_translation"
    # input_json = "translations_bannieres_qg_dev.json"
    # output_sql = "insert_translations_bannieres_qg_dev.sql"
    # table = "bannieres_publicitaires_translation"

    with open(input_json, encoding="utf-8") as f:
        translations = json.load(f)

    sql_lines = []
    total_tasks = sum(len(entry["translations"]) for entry in translations)

    with tqdm(total=total_tasks, desc="📝 Generating SQL", ncols=100) as pbar:
        for entry in translations:
            informations_id = entry["informations_id"]
            field = entry["field"]

            for locale, text in entry["translations"].items():
                safe_text = text.replace("'", "''")
                sql_lines.append(
                    f"INSERT INTO {table} "
                    f"(field, informations_id, locale, text) "
                    f"VALUES ('{field}', {informations_id}, '{locale}', '{safe_text}');"
                )
                pbar.update(1)

    with open(output_sql, "w", encoding="utf-8") as f:
        f.write("\n".join(sql_lines))

    print(f"\n✅ SQL queries saved to {output_sql}")

if __name__ == "__main__":
    main()
