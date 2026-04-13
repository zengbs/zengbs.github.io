for file in *\ *; do
    [ -e "$file" ] || continue
    mv -v "$file" "${file// /_}"
done
