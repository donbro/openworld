#!/usr/bin/env python
# encoding: utf-8
"""
createLayer.py

Created by donb on 2013-07-03.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""


import objc
from Foundation import NSURL
from AppKit import NSFont   , NSColor , NSAttributedString
from Quartz import (CGColorCreateGenericRGB    , CGColorCreateGenericGray ,CGImageSourceCreateWithURL,
                            CGImageSourceCreateImageAtIndex, QCComposition, QCCompositionLayer)
from Quartz import CALayer, CATextLayer, CIFilter
                            
from printB import printB

def getImage(path):

    url = NSURL.fileURLWithPath_(path)
    imagesrc = CGImageSourceCreateWithURL(url, None)        
    return CGImageSourceCreateImageAtIndex(imagesrc, 0, None);

textBkgndColor = CGColorCreateGenericRGB(0.8, 0.8, 0.5, 0.8);  # light gray
textBkgndColorNone = CGColorCreateGenericRGB(0.8, 0.8, 0.5, 0.0);  # transparent
borderColor = CGColorCreateGenericGray(.4, 0.75)

textColor2      = CGColorCreateGenericRGB(0.4, 0.2, 0.1, 1.0)
    # font           = NSFont.fontWithName_size_("HelveticaNeue-Medium",14.0)
    # font           = NSFont.fontWithName_size_("HelveticaNeue-Medium",36.0)
    # font           = NSFont.fontWithName_size_("Avenir Next LT Pro Ultra Light Italic",36.0)
font_avenir           = NSFont.fontWithName_size_("Avenir Next LT Pro Italic",36.0)
textColor0      = CGColorCreateGenericRGB(0.6, 0.2, 0.3, 1.0)
textHighlight   = CGColorCreateGenericRGB(1.0, 0.8, 1.0, 0.9)
whiteColor = CGColorCreateGenericRGB(0.0, 0.5, 1.0, 1.0)

def createTextLayer(    origin=(420,120),
                    size = (180,180),
                    backgroundColor=textBkgndColorNone,
                    textColor=textColor0,
                    zPosition = 12,
                    text_string = None,
                    cornerRadius = 25.0,
                    borderWidth = 1.0,
                    borderColor=borderColor,
                    font=font_avenir
                    ):
                    
    cat2 = CATextLayer.alloc().init()

    # cat2.setForegroundColor_(textColor)
    # cat2.setBackgroundColor_(NSColor.whiteColor()) # textBkgndColor)
    cat2.setBackgroundColor_( backgroundColor )

    s3 = NSAttributedString.alloc().initWithString_attributes_(text_string, { "NSFont":font,
                    "NSColor" : textColor } ) # default is black is fine
                    
    cat2.setString_(s3)
    size = s3.size()


    cat2.setFrame_(  ( origin , size )  )      
    cat2.setZPosition_(zPosition)
    cat2.setBorderWidth_(borderWidth)
    cat2.setBorderColor_( borderColor )           
    
    # cat2.setMasksToBounds_( objc.NO )  # doesn'tmatter for a TextLayer?
    
    
    return cat2
                    


def createLayer(    origin=(420,120),
                    size = (180,180),
                    backgroundColor=textBkgndColor,
                    zPosition = 12,
                    image_path = None,
                    image=None,
                    cornerRadius = 25.0,
                    borderWidth = 1.0,
                    borderColor=borderColor
                    ):
                    
                    # name , bounds=None
                    

    testLayer = CALayer.alloc().init()

    # if bounds != None:  
    #     l.setBounds_(bounds)

    # origin=(420,120)
    # size = (300,300)
    testLayer.setFrame_(  ( origin , size )  )      
    testLayer.setBackgroundColor_( backgroundColor )
    testLayer.setZPosition_(zPosition)
    
    if image is not None:
        testLayer.setContents_( image )
    elif image_path is not None:
        image = getImage(image_path)
        testLayer.setContents_( image )
    
    testLayer.setCornerRadius_(cornerRadius)      
    
    testLayer.setMasksToBounds_( objc.YES )     # YES, it really does clip everything!
    testLayer.setBorderWidth_(borderWidth)
    testLayer.setBorderColor_( borderColor )           

    # o will or o won't you ever work you shadow you shadow you
    testLayer.setShadowColor_(NSColor.redColor())
    testLayer.setShadowOpacity_( 1.0 )
    testLayer.setShadowRadius_(4.0)
    testLayer.setShadowOffset_((5.0, 5.0))
    
    return testLayer

def getQCCompLayer(): # (s):
    
    # cpath = "/Users/donb/Library/Compositions/gradient_2.qtz"
    cpath = "/Users/donb/Library/Compositions/gradient3_light.qtz"
    # cpath = "/Users/donb/Library/Compositions/v12 grey background.qtz"

    # exampleQCCompositionLayer = QCCompositionLayer.compositionLayerWithFile_(cpath)
    
    theQCComposition = QCComposition.compositionWithFile_(cpath)

    printB("QCComposition", theQCComposition, only=['attributes', 'defaultInputParameters', 
                            'description', 'filePath', 'protocols',  'patch',  'inputKeys', 
                             'identifier', 'outputKeys'])  # 'composition' is a *really* lot of info about the composition!
    

    # print "theQCComposition.attributes() are", theQCComposition.attributes()
    # print "theQCComposition.identifier() are", theQCComposition.identifier()
    # print "theQCComposition.inputKeys() are", theQCComposition.inputKeys()

    # theQCComposition.inputKeys() are (
    #     "_protocolInput_PrimaryColor",
    #     "_protocolInput_SecondaryColor",
    #     direction,
    #     position
    # )
    
    exampleQCCompositionLayer = QCCompositionLayer.compositionLayerWithComposition_(theQCComposition)


    zPosition = 0
    exampleQCCompositionLayer.setZPosition_(zPosition)

    return exampleQCCompositionLayer


if __name__ == '__main__':
        lake_picture_path = "/Library/Desktop Pictures/Lake.jpg"    
        getImage(lake_picture_path)
        getQCCompLayer()