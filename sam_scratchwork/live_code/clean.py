with open('tb.txt') as f:
    text = f.read()
    lines = text.split('\n')
    hgoal, wgoal=480,768
    hsource,wsource=15832.0,25404.0
    scales = [wgoal/wsource,hgoal/hsource,wgoal/wsource,hgoal/hsource]
    hvwhs = [[float(i)*scale for i,scale in zip(l.split(' '),scales)] for l in lines if l]
    coors = [(vert, hor, vert+h,hor+w) for hor,vert,w,h in hvwhs]
with open('..\\Data\\0005.jpg.demo_seg.txt','w') as f:
    f.write('\n'.join('text|[[%.2f, %.2f], [%.2f, %.2f]]' % c for c in coors))
