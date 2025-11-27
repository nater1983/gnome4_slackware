#!/bin/bash

# gfs team 2024
 
set -e

if [ "$UID" -ne 0 ];then
  echo "R "
  echo "O "
  echo "O "
  echo "T "
  exit 1
fi


D=$(pwd)
OD=order
BD=/tmp/gfs
BL=BUILD_LOGS

if [ ! -d "$D/$BL" ]; then
  mkdir -p "$D/$BL"
fi

log_time_elapsed() {
  local log_file="$1"
  if [ -n "$log_file" ]; then
    echo "Time elapsed for $log_file: $SECONDS seconds" >> "$log_file"
  fi
  SECONDS=0
}


SECONDS=0

rm -rf "$BD" || true
find . -type f -name "*.SlackBuild" -exec chmod +x {} \;
find . -type f -name "*.sh" -exec chmod +x {} \;
chmod +x ./*.sh || true
chmod +x ./*.bash || true


blacklist(){
cd ./BLACKLIST47/"$OD" || exit
./build_all.sh |& tee "$D"/"$BL"/build_blacklist.system.log
log_time_elapsed "$D"/"$BL"/build_blacklist.system.log
}

main_gnome(){
cd "$D" || exit
cd ./main_gnome/"$OD"
./build_all.sh |& tee "$D"/"$BL"/build_main_gnome.log
log_time_elapsed "$D"/"$BL"/build_main_gnome.log
}

gnome(){
cd "$D" || exit
cd ./gnome/"$OD"
./build_all.sh |& tee "$D"/"$BL"/build_gnome.log
log_time_elapsed "$D"/"$BL"/build_gnome.log
}

gnome_soft(){
cd "$D" || exit
cd ./gnome_soft/"$OD"
./build_all.sh |& tee "$D"/"$BL"/build_gnome_soft.log
log_time_elapsed "$D"/"$BL"/build_gnome_soft.log
}

builder(){
cd "$D" || exit
cd ./gnome_builder/"$OD"
./build_all.sh |& tee "$D"/"$BL"/build_gnome_builder.log
log_time_elapsed "$D"/"$BL"/build_gnome_builder.log
}

extensions(){
cd "$D" || exit
cd ./extensions/"$OD"
./build_all.sh |& tee "$D"/"$BL"/build_extensions.log
log_time_elapsed "$D"/"$BL"/build_extensions.log
}


backgrounds(){
cd "$D" || exit 
cd ./backgrounds/"$OD"
./build_all.sh |& tee "$D"/"$BL"/build_backgrounds.log
log_time_elapsed "$D"/"$BL"/build_backgrounds.log
}

gnome_more(){
cd "$D" || exit 
cd ./gnome_more/"$OD"
./build_all.sh |& tee "$D"/"$BL"/build_gnome_more.log
log_time_elapsed "$D"/"$BL"/build_gnome_more.log
}


extras(){
cd "$D" || exit
cd ./extras/"$OD"
./build_all.sh |& tee "$D"/"$BL"/build_extras.log
log_time_elapsed "$D"/"$BL"/build_extras.log
}


# cd "$D" || exit
#find . -type f -name "*.tar.?z*" -exec rm {} \;
#true


games(){
cd "$D" || exit
cd ./games/"$OD"
./build_all.sh |& tee "$D"/"$BL"/build_games.log
log_time_elapsed "$D"/"$BL"/build_games.log
}

# Last step...
configs(){
cd "$D" || exit
bash configs.bash |& tee "$D"/"$BL"/ran_configs.log
log_time_elapsed "$D"/"$BL"/ran_configs.log
}

# Comment what you dont want to build. 
blacklist
main_gnome
gnome
gnome_soft
builder
extensions
backgrounds
gnome_more
extras
games
configs

echo ""
log_time_elapsed "To build the Universe..."
