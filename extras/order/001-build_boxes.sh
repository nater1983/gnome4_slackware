#!/bin/bash
echo Building boxes
cd ../boxes/order_boxes  || exit 1
./build_all.sh
