#!/bin/bash

SOURCE_DIR="/home/aadith/projects"

BACKUP_DIR="/mnt/backups/projects"

TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)

FILENAME="backup-$TIMESTAMP.tar.gz"

DEST_FILE="$BACKUP_DIR/FILENAME"


echo "Starting backup of $SOURCE_DIR..."


mrdir -p "SOURCE_DIR..."

tar -czvf "$DEST_FILE" "SOURCE_DIR"


if [ $? -eq 0]; then 
  echo "Backup succesful!"
  echo "Archive created at: $DEST_FILE"

else
  echo "Backup FAILED! Please check for errors."
  exit 1

fi 


echo "Backup process complete."
exit 0

