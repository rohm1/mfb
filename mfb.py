import curses
import getopt
import os
import sys

def get_lines(search, ls_options):
    return os.popen("ls " + ls_options + " | tail --lines=+3 | grep -i \"" + search + "\"").read().strip().split('\n')

def redraw(stdscr, search, path, crtline, ls_options):
    stdscr.clear()
    lines=get_lines(search, ls_options)
    maxlines=len(lines)
    if crtline > maxlines:
        crtline=maxlines
    prompt=(path + "/" + search).replace("//", "/")
    stdscr.addstr(0, 0, prompt)
    linenr=1
    for line in lines:
        # highligh selected line
        if linenr-1 == crtline:
            stdscr.addstr(linenr, 0, line, curses.A_REVERSE)
        else:
            stdscr.addstr(linenr, 0, line)
        # prevent screen overflow (no pagination)
        if linenr >= curses.LINES-2:
            break
        linenr+=1
    stdscr.move(0, len(prompt))
    return crtline

def main(stdscr, ls_options):
    curses.use_default_colors()
    curses.noecho()
    path=os.getcwd()
    search=""
    crtline=0
    while True:
        crtline=redraw(stdscr, search, path, crtline, ls_options)
        c = stdscr.getch()
        if c in (curses.KEY_ENTER, 10, 13):
            selectedname=get_lines(search, ls_options)[crtline]
            selectedname=os.popen("echo " + selectedname + " | awk '{print $9}'").read().strip()
            selected=path + "/" + selectedname
            if os.path.isdir(selected):
                # select "first" entry if navigating in a directory,
                # leave selected line to .. else
                if selectedname != "..":
                    crtline=1
                search=""
                path=os.path.realpath(selected)
                os.chdir(path)
            else:
                os.system("xdg-open " + selected + " 2> /dev/null 1> /dev/null")
        elif c == curses.KEY_BACKSPACE:
            if len(search) > 0:
                search=search[0:len(search)-1]
        elif c == curses.KEY_UP:
            if crtline > 0:
                crtline-=1
        elif c == curses.KEY_DOWN:
            if crtline < len(get_lines(search, ls_options))-1:
                crtline+=1
        elif c == 27: # escape
            break
        else:
            search+=chr(c)
    return path
    
outputfile=""
ls_options="--group-directories-first -hla"
try:
    opts, args = getopt.getopt(sys.argv[1:], "ho:l:")
except:
    print('mfb.py -o <outputfile> -l <ls_options>')
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        print('mfb.py -o <outputfile> -l <ls_options>')
        sys.exit()
    elif opt in ("-o"):
        outputfile = arg
    elif opt in ("-l"):
        ls_options = arg

try:
    os.environ.setdefault('ESCDELAY', '1')        
    curses.wrapper(main, ls_options)
except:
    if outputfile != "":
        f = open(outputfile, "w")
        f.write(os.getcwd())
        f.close()

