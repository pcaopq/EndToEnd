def tif_to_jpg(inname, outname, tifh=15832.0, tifw=25404.0):
    with open(inname) as f:
        text = f.read()
        lines = text.split('\n')
        hgoal, wgoal=480,768
        scales = [wgoal/tifw, hgoal/tifh, wgoal/tifw, hgoal/tifh]
        hvwhs = [[float(i)*scale for i,scale in zip(l.split(' '),scales)] for l in lines if l]
        coors = [(vert, hor, vert+h,hor+w) for hor,vert,w,h in hvwhs]
    with open(outname,'w') as f:
        f.write('\n'.join('text|[[%.2f, %.2f], [%.2f, %.2f]]' % c for c in coors))
