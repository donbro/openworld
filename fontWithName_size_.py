#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by donb on 2013-07-01.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

import sys
import os

import objc
from Foundation import NSDictionary, NSAttributedString
from AppKit import NSFont, CATextLayer, NSFontAttributeName

def main():


    # "Skia-Regular 14.00 pt. P [] (0x7ff98cb0b410) fobj=0x7ff98cb0ad90, spc=3.50"


    font           = NSFont.fontWithName_size_("HelveticaNeue-Medium",14.0)
    font           = NSFont.fontWithName_size_("Avenir Next LT Pro Ultra Light Italic",14.0)
    print "font is", font
    print "font.displayName() is", font.displayName()
    
    # attributes = NSDictionary.dictionaryWithObjectsAndKeys_(font, NSFontAttributeName, None )
    # print "attributes is", attributes


 
    s = "CGColorCreateGenericRGB(0.8, 0.8, 0.8, 0.4)"
    
    # print dir(NSAttributedString)
        
    # s2 = NSAttributedString.alloc().initWithString_attributes_(s, attributes)
    # 
    # print "s2 is", s2

    s3 = NSAttributedString.alloc().initWithString_attributes_(s, { "NSFont":font })

    print "s3 is", s3 # , "s2 == s3", s2 == s3

    print "s3.size() is", s3.size()

    # s3.size() is <NSSize width=293.0 height=21.0>
    
    cat = CATextLayer.alloc().init()
    
    cat.setString_(s3)
    
    # cat.setFont_(font)
    # cat.setFontSize_(font.pointSize() )        # necessary after setFont?
    
    s4 = cat.string()
    
    print "s4 is", s4, "s3 == s4", s3 == s4
    
    print "cat.bounds() is", cat.frame()
    
    

    


if __name__ == '__main__':
	main()

