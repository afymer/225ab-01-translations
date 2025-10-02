langs=("en_GB" "es_ES" "ar_SA")


for lang in "${langs[@]}"; do
    src="po/translated"
    
    dst="$matchmaking_root/public/locale/$lang"
    mkdir -p "$dst"
    cp "$src/messages_$lang.po" "$dst/LC_MESSAGES/messages.po"
done
