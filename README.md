# Minimal file browser

MFB (minimal file browser) is a curses python3 app to quickly
navigate through the filesystem. Use the up and down keys to
select entries, ENTER to open a directory or file, or ESC or
CTRL+C to quit. Any other key will be handled as text input to
filter the result list!

Use the bash wrapper (`source path/to/mfb/mfb.sh` in your `.bashrc`)
to use the `mfb` function. It will also enable natigation to the last
current directory in you shell upon CTRL+C. Pressing ESC will exit MFB
without changing your working directory. 
