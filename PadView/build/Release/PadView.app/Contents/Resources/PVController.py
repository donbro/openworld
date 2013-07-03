# -*- coding: utf-8 -*-
#
#  PVController.py
#  PadView
#
#  Created by donb on 2010.05.06.
#  Copyright (c) 2010 __MyCompanyName__. All rights reserved.
#

from objc import YES, NO, IBAction, IBOutlet
from Foundation import *
from AppKit import *

    #@interface Controller : NSObject
    #{
    #   IBOutlet View *view;
    #   
    #   CAScrollLayer *bodyLayer;
    #   CATextLayer *headerTextLayer;
    #   CATextLayer *desktopImageCountLayer;
    #   CATransform3D sublayerTransform;
    #   CGImageRef shadowImage;
    
    #   float cellSpacing = 5;
    #   float cellSize = 160;
    
    #   NSDictionary *textStyle;
    #   Catalog *catalog;
    #   
    #   CGSize desktopImageSize;
    #   NSMutableArray *desktopImages;
    #   int totalDesktopImages, selectedDesktopImageIndex;
    #   
    #   CFMutableDictionaryRef layerDictionary; /* desktopImage -> layer*/
    #   
    #   int sortKeys[3];
    #}
    
from PVDatabase import get_top_level_nodes # LoadDatabase, SaveDatabase

class PVController(NSObject):

    thisPVControllersPadView = IBOutlet()   #   thisControllersPadView = objc.IBOutlet()  # IBOutlet View *view;

    def init(self):
    
        #   NSSize size;
        #   CALayer *rootLayer;
        self = super(PVController, self).init()      #   self = [super init];
        
        if self == None: return None
        
        NSLog("PVController: received init.")
        
        #data = ["node001", ["node002", "node003"]] # just to bet us sstated
        #SaveDatabase(data)
        
        self.data = top_level_nodes = get_top_level_nodes()

       
        #self.data =  LoadDatabase()

        NSLog("PVController: read %d top-level nodes." % len(self.data))  # Use %r, not %@, for a Python structure.

        NSLog("PVController: init (before loadNib): thisPVControllersPadView is: %@.", self.thisPVControllersPadView)

        #[NSBundle loadNibNamed:@"View" owner:self];
        
        NSBundle.loadNibNamed_owner_("PadView", self)
        
        #[[view window] setDelegate:self];

        NSLog("PVController: init (after loadNib): thisPVControllersPadView is: %@.", self.thisPVControllersPadView)
        # PVController: init (after loadNib): thisPVControllersPadView is: <PadView: 0x1f40be0>.

            
        return self



#- (IBAction)fullScreenAction:(id)sender
#{
#   if (![view isInFullScreenMode])
#       [view enterFullScreenMode:[[view window] screen] withOptions:nil];
#   else
#       [view exitFullScreenModeWithOptions:nil];
#}

    @IBAction
    def fullScreenAction_(self, sender):
        NSLog("PVController: received (IBAction) fullScreenAction_")
        #NSLog("PVController: fullScreenAction: NSApp.mainWindow()  is %@.", NSApp.mainWindow() )
        #controller = NSApp.mainWindow().delegate()
        #NSLog("PVController: fullScreenAction: NSApp.mainWindow().delegate() is %@.", controller)
