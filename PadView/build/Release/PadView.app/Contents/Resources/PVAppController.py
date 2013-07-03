# -*- coding: utf-8 -*-
#
#  PadViewAppDelegate.py
#  PadView
#
#  Created by donb on 2010.05.03.
#  Copyright __MyCompanyName__ 2010. All rights reserved.
#

import sys
from objc import YES, NO, IBAction, IBOutlet

# Cocoa = Foundation + AppKit
from Foundation import *
from AppKit import *

# The imports (and definitions) in this file are run through the interpreter
#       when this file is imported at a point in main.py.  
# This is before the application is running and thus before PyObjC and Quartz and the NSApplication have all gotten synched
# So, don't import Quartz until after a point where the application is actually running.

# import Quartz 

from PVController import PVController


class PVAppController(NSObject):

    thePBView = objc.IBOutlet()  # won't exist until after awake from NIB.

    def init(self):
        self = super(PVAppController, self).init()
        if self:
            NSLog("PVAppController: received init.")
#            NSLog("PVAppController: init: sys.version is " + "".join(sys.version.split('\n')) )

            #NSLog("PVAppController: init: thePBView is: %@.", self.thePBView ) # init: thePBView is: (null).  won't exist until after awake from NIB.
            
        return self

    # Yes, this app controller comes from the NIB file.
    
    def awakeFromNib(self):

        NSLog("PVAppController: received awakeFromNib.")
        NSLog("PVAppController: awakeFromNib: sending newWindowAction_.")

        self.newWindowAction_(self)


    #- (IBAction)newWindowAction:(id)sender

    @IBAction
    def newWindowAction_(self, sender):
        NSLog("PVAppController: received newWindowAction_")
        NSLog("PVAppController: creating instance of PVController.")

        #   [[Controller alloc] init];
        PVController.alloc().init()

        #controller = NSApp.mainWindow().delegate()
        #NSLog("PVAppController: NSApp.mainWindow().delegate() is %@.", controller)



    def applicationDidFinishLaunching_(self, sender):
        NSLog("PVAppController: Application did finish launching.")
        NSLog("PVAppController: applicationDidFinishLaunching_: thePBView is: %@.", self.thePBView )   #  thePBView is: <PadView: 0x1f3a750>.

#   
#- (IBAction)fullScreenAction:(id)sender
#{
#   Controller *controller;
#   
#   controller = [[NSApp mainWindow] delegate];
#   
#   [controller fullScreenAction:sender];
#}
    @IBAction
    def fullScreenAction_(self, sender):
        NSLog("PVAppController: received IBAction fullScreenAction_")
        NSLog("PVAppController: fullScreenAction: NSApp.mainWindow()  is %@.", NSApp.mainWindow() )
        controller = NSApp.mainWindow().delegate()
        NSLog("PVAppController: fullScreenAction: NSApp.mainWindow().delegate() is %@.", controller)
    



#pragma mark -
#pragma mark NSAPPLICATION DELEGATE:


    def applicationShouldTerminateAfterLastWindowClosed_(self, sender):
        """ This is not called until it is actually the last window closing.  YES means quit the app. """
        NSLog("PVAppController: received applicationShouldTerminateAfterLastWindowClosed_ returning YES")
        return YES;

def PointToString(p):
    return "{ %.0f, %.0f }" % (  p.x,   p.y, )

def RectToString(rect):
    return "(%.0f,%.0f,%.0f,%.0f)" % (  rect.origin.x,   rect.origin.y,   rect.size.width,   rect.size.height )

def RectToString2(rect):
    return "(origin: (x=%.0f, y=%.0f), size: (width=%.0f, height=%.0f)" % (  rect.origin.x,   rect.origin.y,   rect.size.width,   rect.size.height )



#  // this is where the magic happens
#  - (void)layoutSublayersOfLayer:(CALayer *)layer
def layoutSublayersOfLayer ( layer ):

#   NSValue *value;
#   NSSize cellSize;
#   CGSize size;
#   NSSize spacing, margin;

    size = layer.bounds().size
    margin = layer.valueForKey_("margin")
    spacing = layer.valueForKey_("spacing")
 
    NSLog( "layoutSublayersOfLayer layer=%r, size=%r, margin=%r, spacing=%r" % ( layer, size, margin, spacing) ) #  RectToString( superlayer.bounds() )  )


