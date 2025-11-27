#!/bin/bash

# gfs team 2023
# LONG LIVE SLACKWARE (1993-2023) 
# 
set -e

if [ "$UID" -ne 0 ];then
  echo "                               "
  echo " please run this script as root"
  echo "                               "
  echo "                               "
  exit 1
fi


D=$(pwd)
OD=order
BD=/tmp/gfs
BL=BUILD_LOGS

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



cd ./BLACKLIST46/"$OD" || exit
./build_all.sh |& tee "$D"/"$BL"/build_blacklist.system.log
log_time_elapsed "$D"/"$BL"/build_blacklist.system.log



cd "$D" || exit
cd ./main_gnome/"$OD"
./build_all.sh |& tee "$D"/"$BL"/build_main_gnome.log
log_time_elapsed "$D"/"$BL"/build_main_gnome.log


cd "$D" || exit
cd ./gnome/"$OD"
./build_all.sh |& tee "$D"/"$BL"/build_gnome.log
log_time_elapsed "$D"/"$BL"/build_gnome.log


#need to add more packages...
cd "$D" || exit
cd ./gnome_soft/"$OD"
./build_all.sh |& tee "$D"/"$BL"/build_gnome_soft.log
log_time_elapsed "$D"/"$BL"/build_gnome_soft.log


cd "$D" || exit
cd ./gnome_builder/"$OD"
./build_all.sh |& tee "$D"/"$BL"/build_gnome_builder.log
log_time_elapsed "$D"/"$BL"/build_gnome_builder.log

# not all extension ready for gnome-45  so far...
cd "$D" || exit
cd ./extensions/"$OD"
./build_all.sh |& tee "$D"/"$BL"/build_extensions.log
log_time_elapsed "$D"/"$BL"/build_extensions.log


cd "$D" || exit 
cd ./backgrounds/"$OD"
./build_all.sh |& tee "$D"/"$BL"/build_backgrounds.log
log_time_elapsed "$D"/"$BL"/build_backgrounds.log


cd "$D" || exit 
cd ./gnome_more/"$OD"
./build_all.sh |& tee "$D"/"$BL"/build_gnome_more.log
log_time_elapsed "$D"/"$BL"/build_gnome_more.log


#######################################################################################
# uncomment these lines to build all extras or                                        #
# you any time you want to build something specific cd to its order_package folder    #
# and ran build_all.sh                                                                #
# this way you will build and install it with all deps in the right build order.      #
#######################################################################################

#cd "$D" || exit
#cd ./extras/"$OD"
#./build_all.sh |& tee "$D"/"$BL"/build_extras.log
#log_time_elapsed "$D"/"$BL"/build_extras.log
# cd "$D" || exit
#find . -type f -name "*.tar.?z*" -exec rm {} \;
#true


######################################################################################
# uncomment to build all games or                                                    #
# you any time you want to build something specific cd to its order_package folder   #
# and ran build_all.sh                                                               #
# this way you will build and install it with all deps in the right build order.     #
######################################################################################

# Not all games ready so far... no time :( #
#cd "$D" || exit
#cd ./games/"$OD"
#./build_all.sh |& tee "$D"/"$BL"/build_games.log
#log_time_elapsed "$D"/"$BL"/build_games.log

# Last step...
cd "$D" || exit
bash configs.bash |& tee "$D"/"$BL"/ran_configs.log
log_time_elapsed "$D"/"$BL"/ran_configs.log

echo ""
log_time_elapsed "To build the Universe..."
