import json

inname = 'P4.300'
outname = 'P4.json'
anns = []

f = open(inname)
linelist = list(f)
i = 0
while i < len(linelist):
  if linelist[i].find('[Zone:') != -1:
    i += 2
    x = linelist[i]
    idx = x[10:len(x)-1]
    
    i += 1
    x = linelist[i]
    l = int(x[16:len(x)-1])

    i += 1
    x = linelist[i]
    r = int(x[17:len(x)-1])

    i += 1
    x = linelist[i]
    t = int(x[15:len(x)-1])

    i += 1
    x = linelist[i]
    b = int(x[18:len(x)-1])

    anns.append({"class": "article",
                   "height": b-t,
                   "id": idx,
                   "type": "rect",
                   "width": r-l,
                   "x": l,
                   "y": t})
  i += 1

seg = [{
        "annotations": anns,
      }]

with open(outname,'w') as f:
   json.dump(seg, f, indent=4)

