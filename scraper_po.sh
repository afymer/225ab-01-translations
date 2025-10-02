langs=("en_GB" "es_ES" "ar_SA")

for lang in "${langs[@]}"; do
    dst="po/source"
    
    src="$matchmaking_root/public/locale/$lang"
    mkdir -p "$dst"
    cp "$src/LC_MESSAGES/messages.po" "$dst/messages_$lang.po"
done
