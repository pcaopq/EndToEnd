from xml.dom import minidom
import processXML
from PIL import Image as PILI
from memory_profiler import profile

def size_of_image(imname):
    im=PILI.open(imname )
    return im.size[::-1] #[height,width]

def get_scalefactors(xmlname, imagename):
    pxml = processXML.ProcessXML(xmlname)
    (h,w) = pxml.getTIFdimensions(); 
    h,w=float(h),float(w)
    (hj,wj) = size_of_image(imagename)
    return float(hj)/h, float(wj)/w
def scale(coor, factor):
    vpos,hpos,height,width = coor
    hs,ws = factor
    return (vpos*hs,hpos*ws,height*hs,width*ws)

# fp = open('readxml2.log', 'w+')
# @profile(stream = fp)
def readxml(xmlname, imagename, scrapedname):
    xmldoc = minidom.parse(xmlname)
    alto = xmldoc.getElementsByTagName('alto')[0]
    layout = alto.getElementsByTagName('Layout')[0]
    page = layout.getElementsByTagName('Page')[0]
    printspace = page.getElementsByTagName('PrintSpace')[0]
    textblocks = printspace.getElementsByTagName('TextBlock')

    factor = get_scalefactors(xmlname, imagename)

    with open(scrapedname, 'w') as f:
    	for textblock in textblocks:
            f.write('-'*70+'\n')
            if textblock.getElementsByTagName('TextLine'):
                textlines = textblock.getElementsByTagName('TextLine')
                for textline in textlines:
                    strings = textline.getElementsByTagName('String')
                    sps = textline.getElementsByTagName('SP')
                    for string in strings:
                        L = lambda label:float(string.getAttribute(label))
                        S = lambda label:(string.getAttribute(label))
                        coor = (L('VPOS'), L('HPOS'), L('HEIGHT'),L('WIDTH'))
                        coor = scale(coor, factor)
                        f.write("%s %f %f %f %f\n" % ((S('CONTENT'),)+coor))
                    for sp in sps:
                        L = lambda label:float(string.getAttribute(label))
                        f.write("%s %s %s\n" % (L('VPOS')*factor[0],
                                                L('HPOS')*factor[1],
                                                L('WIDTH')*factor[1]))
            # if textblock.getAttribute('HPOS'):
            # 	f.write("%f %f %f %f\n" % (float(textblock.getAttribute('HPOS')), float(textblock.getAttribute('VPOS')), float(textblock.getAttribute('WIDTH')), float(textblock.getAttribute('HEIGHT'))))

#import sys
#readxml(sys.argv[1]) #e.g. 0005.xml
