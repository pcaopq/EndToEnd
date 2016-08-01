import sys
fnamein, fnameout = sys.argv[1:3]
with open(fnamein) as f:
    polys = [l.split('|') for l in f.read().split('\n') if l]
    labpolys = [(p[0],eval('[%s]'%(','.join(p[1:])))) for p in polys]

sh = 6351/768.0
sw = 3960/480.0

json = {'annotations': [
    {'id':pi,'height':(b[1][0]-b[0][0])*sh,'width':(b[1][1]-b[0][1])*sw,'y':(b[0][0])*sh,'x':b[0][1]*sw, 'type':'rect', 'class':lab}
    for pi, (lab,pol) in enumerate(labpolys) for b in pol]}

with open(fnameout,'w') as f:
    f.write(str(json).replace("'",'"').replace(',',',\n\t\t'))
