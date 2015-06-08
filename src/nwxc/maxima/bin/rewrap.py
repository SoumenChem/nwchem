#!/usr/bin/python
#
# This is a little program to rewrap comments that Maxima has generated for
# the NWXC library.
#
# Maxima will generate LaTeX comments (which are supposed to be parsed by
# Doxygen). The LaTeX generator does not pay attention to how long
# lines get to be. However, some picky compilers insist on a maximum line length
# of 132 characters (apparently the current Fortran standard) and refuse to
# compile code that does not adhere to that (even if it just involves comment
# lines). So this script was created to rewrap comment lines to fit within the
# good old 72 character restriction (you never know if someone else is going
# to come up with an even "better" compiler).
#
# This script takes comment lines and if they are longer than 72 characters
# we look for a sensible breaking point, i.e. operators like "+", "-", "/",
# or keywords like "\left" or "\over" or separators like ", " or "\,".
# The first part of the line is written as a comment line and the rest
# goes through the splitting procedure again until the whole line has been
# written out.
#
import sys
from string import rfind

def rewrap_line(longline):
  # note: longline has a newline character at the end which is counted by 
  #       len as well but is not included in the 72 characters that are allowed
  #       in Fortran
  while len(longline)-1 > 72:
    i = -1
    # wrap before * / ( ) + or -
    i = max(i,rfind(longline,"+",0,71))
    i = max(i,rfind(longline,"-",0,71))
    i = max(i,rfind(longline,"/",0,71))
    i = max(i,rfind(longline,"\,",0,70))
    i = max(i,rfind(longline,", ",0,70))
    i = max(i,rfind(longline,"\left",0,67))
    i = max(i,rfind(longline,"\right",0,66))
    if i == -1:
      sys.stderr.write("No sensible break point found in:\n")
      sys.stderr.write(longline)
      exit(1)
    tmpline = longline[:i]+"\n"
    sys.stdout.write(tmpline)
    tmpline  = "C>    " + longline[i:]
    longline = tmpline
  sys.stdout.write(longline)

longline = ""
line = sys.stdin.readline()
while line:
  if line[:2] == "C>":
    # comment line: rewrap it
    longline = line
    rewrap_line(longline)
  else:
    # code line: just write it out as is
    longline = line
    sys.stdout.write(longline)
  line = sys.stdin.readline()

if line[:2] == "C>":
  longline = line
  rewrap_line(longline)
else:
  longline = line
  sys.stdout.write(longline)
