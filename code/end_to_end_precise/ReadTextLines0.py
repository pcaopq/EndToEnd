import pcsxml
import tinyxml2
from memory_profiler import profile
from PIL import Image as PILI

def size_of_image(imname):
    im=PILI.open(imname )
    return im.size[::-1] #[height,width]

def scale(coor, factor):
    vpos,hpos,height,width = coor
    hs,ws = factor
    return (vpos*hs,hpos*ws,height*hs,width*ws)

# fp = open('readxml2.log', 'w+')
# @profile(stream = fp)
def readxml(xmlname, imagename, scrapedname):
    xmldoc = tinyxml2.XMLDocument()
    xmldoc.LoadFile(xmlname)
    page = xmldoc.FirstChildElement("alto").FirstChildElement("Layout").FirstChildElement("Page")
    textblks = page.FirstChildElement("PrintSpace").FirstChildElement("TextBlock")    
    h = tinyxml2.new_intp()
    w = tinyxml2.new_intp()
    page.QueryIntAttribute("HEIGHT", h)
    page.QueryIntAttribute("WIDTH", w)
    (hj, wj) = size_of_image(imagename)
    factor = float(hj)/tinyxml2.intp_value(h), float(wj)/tinyxml2.intp_value(w)
    tinyxml2.delete_intp(h)
    tinyxml2.delete_intp(w)    

    with open(scrapedname, 'w') as f:
        while(textblks != None):
            f.write('*'*70+'\n')
            # if textblock.getElementsByTagName('TextLine'):
            textlines = textblks.FirstChildElement("TextLine")
            while(textlines != None):
                strings = textlines.FirstChildElement("String")
                while(strings != None):
                    hpos = strings.IntAttribute("HPOS")
                    vpos = strings.IntAttribute("VPOS")
                    width = strings.IntAttribute("WIDTH")
                    height = strings.IntAttribute("HEIGHT")
                    content = strings.Attribute("CONTENT")
                    coor = (vpos, hpos, height, width)
                    coor = scale(coor, factor)
                    f.write("%s %f %f %f %f\n" % ((content,)+coor))
                    strings = strings.NextSiblingElement("String")

                spaces = textlines.FirstChildElement("SP")
                while(spaces != None):
                    # hpos = spaces.IntAttribute("HPOS")
                    # vpos = spaces.IntAttribute("VPOS")
                    # width = spaces.IntAttribute("WIDTH")
                    f.write("%s %s %s\n" % (vpos*factor[0], hpos*factor[1], width*factor[1]))
                    spaces = spaces.NextSiblingElement("SP")
                    
                textlines = textlines.NextSiblingElement("TextLine")
            textblks = textblks.NextSiblingElement("TextBlock")
    f.close() 
            # if textblock.getAttribute('HPOS'):
            # 	f.write("%f %f %f %f\n" % (float(textblock.getAttribute('HPOS')), float(textblock.getAttribute('VPOS')), float(textblock.getAttribute('WIDTH')), float(textblock.getAttribute('HEIGHT'))))

#import sys
#readxml(sys.argv[1]) #e.g. 0005.xml
