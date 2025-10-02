langs=("en" "es" "ar")


for lang in "${langs[@]}"; do
    src="strings/$lang"

    
    dst="$boxer_root/auth/presentation/src/main/res/values-$lang"
    mkdir -p "$dst"
    cp "$src/strings-auth-main.xml" "$dst/strings.xml"

    dst="$boxer_root/app/src/main/res/values-$lang"
    mkdir -p "$dst"
    cp "$src/strings-app-main.xml" "$dst/strings.xml"

    dst="$boxer_root/core/presentation/ui/src/main/res/values-$lang"
    mkdir -p "$dst"
    cp "$src/strings-core-presentation-ui.xml" "$dst/strings.xml"

    dst="$boxer_root/core/presentation/designsystem/src/main/res/values-$lang"
    mkdir -p "$dst"
    cp "$src/strings-core-presentation-designsystem.xml" "$dst/strings.xml"

    dst="$boxer_root/qg/presentation/src/main/res/values-$lang"
    mkdir -p "$dst"
    cp "$src/strings-qg-presentation.xml" "$dst/strings.xml"
done
