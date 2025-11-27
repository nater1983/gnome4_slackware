#!/bin/bash
echo Building pika-backup
cd ../pika-backup/order_pika_backup  || exit 1
./build_all.sh
