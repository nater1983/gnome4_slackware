#!/bin/bash

# Variables
pattern='/sbin/makepkg'
line1='if [ -f "$CWD/slack-required" ]; then cat "$CWD/slack-required" > "$PKG/usr/doc/$PRGNAM-$VERSION/slack-required"; fi'
log_file="changes.log"
backup_dir="./backup"

# Helper function: Log messages
log_message() {
    local message="$1"
    echo "$message"
    echo "$message" >> "$log_file"
}

# Helper function: Check for .SlackBuild files
check_slackbuild_files() {
    local count
    count=$(find ./ -name "*.SlackBuild" | wc -l)
    if [[ "$count" -eq 0 ]]; then
        log_message "No .SlackBuild files found. Exiting."
        exit 1
    fi
}

# Helper function: Create backups
backup_files() {
    mkdir -p "$backup_dir"
    log_message "Creating backups in $backup_dir..."
    find ./ -name "*.SlackBuild" -exec cp {} "$backup_dir" \;
    log_message "Backups completed."
}

# Helper function: Dry run
dry_run() {
    log_message "Performing dry-run to preview changes..."
    find ./ -name "*.SlackBuild" -exec sed "s#$pattern#$line1\n$pattern#g" {} \;
}

# Helper function: Apply changes
apply_changes() {
    log_message "Applying changes..."
    find ./ -name "*.SlackBuild" -exec sed -i "s#$pattern#$line1\n$pattern#g" {} \;
    log_message "Changes applied successfully."
}

# Helper function: Show usage
show_usage() {
    echo "Usage: $0 [--dry-run | --apply | --backup | --help]"
    echo "  --dry-run      Preview the changes (default mode)."
    echo "  --apply        Apply the changes to .SlackBuild files."
    echo "  --backup       Create backups of .SlackBuild files before modification."
    echo "  --help         Display this help message."
}

# Parse command-line arguments
if [[ "$#" -eq 0 ]]; then
    dry_run
    exit 0
fi

case "$1" in
    --dry-run)
        check_slackbuild_files
        dry_run
        ;;
    --apply)
        check_slackbuild_files
        backup_files
        apply_changes
        ;;
    --backup)
        check_slackbuild_files
        backup_files
        ;;
    --help)
        show_usage
        ;;
    *)
        echo "Invalid option: $1"
        show_usage
        exit 1
        ;;
esac
