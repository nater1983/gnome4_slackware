#!/bin/bash
cd $(dirname $0) ; CWD=$(pwd)
# gfs team. 1993-2023 30 years of glory, building and re buidling... the Universe. 
# This our way... because...
# LONG LIVE SLACKWARE

OUTPUT_FILE="LINKS.TXT"

> "$OUTPUT_FILE"

date +"%H:%M:%S %d-%m-%y" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

process_build_script() {
    local build_script="$1"
    
    urls=$(awk '/wget\s+-c\s+http[s]?:\/\/[^\s]+/{print $NF}' "$build_script")
    if [ -n "$urls" ]; then
        echo "$urls" >> "$OUTPUT_FILE"
    fi

    echo "" >> "$OUTPUT_FILE" 
}

process_directory() {
    local directory="$1"
    local indent="$2"
    
    echo "${indent} $directory" >> "$OUTPUT_FILE"
    
    for slackbuild_file in "$directory"/*.SlackBuild; do
        if [[ -f $slackbuild_file ]]; then
            process_build_script "$slackbuild_file"
        fi
    done

   for subdir in "$directory"/*; do
        if [[ -d $subdir ]]; then
            process_directory "$subdir" "$indent  "
        fi
    done
}

process_directory "../" ""

cd "$CWD" || exit 1
echo "LINKS.TXT file created successfully."

cat LINKS.TXT | grep https://download.gnome.org >> GNOMELINKS.TXT
wait
sed -i 's/tar.xz/sha256sum/g' GNOMELINKS.TXT
wait

mkdir -p SUMS 
wget -i GNOMELINKS.TXT -P SUMS/ -q --show-progress
sed -i '/news/d' SUMS/*.sha256sum
wait
sed -i '/changes/d' SUMS/*.sha256sum
wait
sed -i 's/\s\+/\n/g' SUMS/*.sha256sum
wait
sed -i '$d' SUMS/*.sha256sum

