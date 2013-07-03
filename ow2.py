#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by donb on 2013-07-02.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

import sys
import os

import objc
from Foundation import *
from AppKit import *
from Quartz import   QCComposition , QCCompositionLayer
from Quartz import CGImageSourceCreateWithURL, CGImageSourceCreateImageAtIndex,  \
                            CGColorCreateGenericRGB, CGColorCreateGenericGray, NSShadow

# from Quartz import CGImageSourceCreateWithURL, CGImageSourceCreateImageAtIndex, QCCompositionLayer, QCComposition, \
#                             CGColorCreateGenericRGB, CGColorCreateGenericGray, NSShadow

from PyObjCTools import AppHelper

print  "objc.__version__ is", objc.__version__

class AppDelegate (NSObject):

    # def applicationWillFinishLaunching_(self, aNotification):
    #     app = aNotification.object()
    #     printB("applicationWillFinishLaunching", app)
    # 
    #     # win = NSApp.windows()[0]


    def applicationDidFinishLaunching_(self, aNotification):
        printB("applicationDidFinishLaunching",  aNotification.object())
        # 
        # print "Hello, World!"
        
        win = NSApp.windows()[0]
        
        # The new window creates a view to be its default content view. You can replace it with your own object by using the setContentView: method.

        view =  win.contentView()

        wf = view.bounds()
        x, y = wf.origin
        width, height = wf.size
        s2 = "origin=(x=%r y=%r) size=(width=%r height=%r)" % (x,y,width,height)

    
        
        QCLayer = getQCCompLayer()
        # QCLayer.setFrame_( win_frame ) # view.frame() )      
        printB("QCLayer", QCLayer)
        
        if True:
            # rootLayer = CALayer.layer()
            rootLayer = QCLayer
            view.setLayer_(rootLayer)
            view.setWantsLayer_( objc.YES )                                      #     [self setWantsLayer: YES];
        else:
            view.setWantsLayer_( objc.YES )                                      #     [self setWantsLayer: YES];
            rootLayer = view.layer()


        printB("View",  (view,  s2 )   ) # frame = bounds for origin (0,0)?
        print_setters(view)

        printB("rootLayer", rootLayer)
        
        # rootLayer.setNeedsDisplay()

        # 
        #   serious magic here: frame is not (precisely) equal to current window frame.  
        #     difference causes redraw here?  can't just say win.frame()
        #       and is there no other way to say to redraw?
        #
        
        #  this magic is for the root layer and for a QCComposition only ?!@?

        # print "win.frame() is", win.frame()
        # frame = ((100.0, 350.0), (871.0, 490.0))        
        # print "xx", win.frame() == frame ==> False
        # frame = win.frame() # ((100.0, 350.0), (871.0, 490.0))        

        win.makeKeyAndOrderFront_(objc.NULL)

        # global win_frame
        # print "win.frame() is:", 

        wf = win.frame()
        x, y = wf.origin
        width, height = wf.size
        magic_delta = 0.2   # must be > 0.1 !?!?!
        win.setFrame_display_(  (  (  x , y ) , ( width, height + magic_delta ) ) , objc.YES )

        # view = win.contentView() 
        # view.displayIfNeeded()
        # view.display()
        
        #
        #   end serious magic
        #
        
        layerDict = {
            'origin' : (420,120),
            'size'  :  (120,120),
            'zPosition'  :  12,
            'path'  :  "/Users/donb/projects/openworld/gray button 96px.psd",
            'cornerRadius'  :  16,
            'borderWidth'  :  1.0,
        }
        testLayer = createLayer(**layerDict)
        rootLayer.addSublayer_(testLayer)

        
        print_setters(testLayer)
        
        # lake_picture_path = "/Library/Desktop Pictures/Lake.jpg"    
        # theLakeImage = getImage(lake_picture_path)

        layerDict['origin']=(200,300)
        layerDict['path']="/Library/Desktop Pictures/Lake.jpg"
        layerDict['size']=(300,300)

        testLayer2 = createLayer( **layerDict)
        rootLayer.addSublayer_(testLayer2)

        # origin=(420+200,120+200)
        # size = (300,300)
        # testLayer.setFrame_(  ( origin , size )  )      
        
        
    def applicationWillBecomeActive_(self, aNotification):
        printB("applicationWillBecomeActive",  aNotification.object())

    def applicationWillResignActive_(self, aNotification):
        """ Sent by the default notification center immediately before the application is deactivated."""
        printB("applicationWillResignActive",  aNotification.object())
        
        

    def applicationWillTerminate_(self, aNotification):
        printB("applicationWillTerminate",  aNotification.object())
        
    def applicationShouldTerminateAfterLastWindowClosed_(self, theApplication):
        printB("applicationShouldTerminateAfterLastWindowClosed is called.  returns YES",  theApplication)
        # print "applicationShouldTerminateAfterLastWindowClosed  theApplication is %r" % ( theApplication )
        return objc.YES
        
class WinDelegate (NSObject):
    
    def windowDidBecomeKey_(self, aNotification ):
        """ Informs the delegate that the window has become the key window."""    
        win = aNotification.object()
        view =  win.contentView()
        wf = view.bounds()
        x, y = wf.origin
        width, height = wf.size
        s2 = "\n    %s\n    origin=(x=%r y=%r) size=(width=%r height=%r)" % ("view.bounds:",x,y,width,height)

        printB("windowDidBecomeKey",   s2   )
        

    def windowDidBecomeMain_(self, aNotification ):
        """ Informs the delegate that the window has become the main window."""    
        printB("windowDidBecomeMain",  aNotification.object())
    
    def windowWillEnterFullScreen_(self, aNotification):
        """The window just entered full-screen mode."""
        printB("windowWillEnterFullScreen",  aNotification.object())

    def windowWillExitFullScreen_(self, aNotification):
        """The window just entered full-screen mode."""
        printB("windowWillExitFullScreen",  aNotification.object())

    # def windowDidExitFullScreen_(self, aNotification):
    #     """The window just entered full-screen mode."""
    #     printB("windowDidExitFullScreen",  aNotification.object())

    # def windowDidEnterFullScreen_(self, aNotification):
    #     """The window just entered full-screen mode."""
    #     printB("windowDidEnterFullScreen",  aNotification.object())

def print_setters(obj):
    setters = [k[3:-1].lower() for (k, v) in obj.__class__.__dict__.items() if  k[0:3] == 'set']
    getter_candidates =  sorted([k for (k, v) in obj.__class__.__dict__.items() if k[-1]!='_' and k[0:3] != 'set'])
    for k in getter_candidates:
        if   k.lower() in setters and  hasattr(obj, k) :
                print "%-32s : %r"  % (k, getattr(obj, k)())


def printB(a,b):
    s4 = "    "
    s3 = "   "
    print "\n--------------\n\n"+s4+a+"\n\n"+s3+repr( b) # , type(b)

def getImage(path):

    url = NSURL.fileURLWithPath_(path)
    imagesrc = CGImageSourceCreateWithURL(url, None)        
    return CGImageSourceCreateImageAtIndex(imagesrc, 0, None);

textBkgndColor = CGColorCreateGenericRGB(0.8, 0.8, 0.5, 0.8);  # light gray
borderColor = CGColorCreateGenericGray(.4, 0.75)
    
def createLayer(    origin=(420,120),
                    size = (180,180),
                    backgroundColor=textBkgndColor,
                    zPosition = 12,
                    path = None,
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
    
    if path is not None:
        grey_button_image = getImage(path)
        testLayer.setContents_( grey_button_image )
    
    testLayer.setCornerRadius_(cornerRadius)      
    
    testLayer.setMasksToBounds_( objc.YES )     # YES, it really does clip everything!
    testLayer.setBorderWidth_(borderWidth)
    testLayer.setBorderColor_( borderColor )           

    # o will or o won't you ever work you shadow you shadow you
    # testLayer.setShadowColor_(NSColor.redColor())
    # testLayer.setShadowOpacity_( 1.0 )
    # testLayer.setShadowRadius_(4.0)
    # testLayer.setShadowOffset_((5.0, 5.0))
    
    return testLayer
    
def getQCCompLayer(): # (s):
    
    # cpath = "/Users/donb/Library/Compositions/gradient_2.qtz"
    cpath = "/Users/donb/Library/Compositions/gradient3_light.qtz"
    # cpath = "/Users/donb/Library/Compositions/v12 grey background.qtz"

    # exampleQCCompositionLayer = QCCompositionLayer.compositionLayerWithFile_(cpath)
    
    theQCComposition = QCComposition.compositionWithFile_(cpath)

    printB("QCComposition", theQCComposition)
    

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
    
def main():
    app = NSApplication.sharedApplication()
    printB("App", NSApp())

    print "app.mainWindow() is:", app.mainWindow()
    # print sorted([k for (k, v) in app.__class__.__dict__.items()])


    delegate = AppDelegate.alloc().init()
    NSApp().setDelegate_(delegate)
    # printB("AppDelegate", delegate)  # not really a thing like app or window?

    win = NSWindow.alloc()

    # global win_frame
    # win_frame = ((100.0, 350.0), (871.0, 490.0))        
    win_frame = ((100.0, 350.0), (1000.0, 639.0))        
    #    '\n    view.bounds:\n    origin=(x=0.0 y=0.0) size=(width=1150.0 height=531.0)'

    
    deferCreation = objc.YES
    # deferCreation = objc.NO
    win.initWithContentRect_styleMask_backing_defer_ (
                        win_frame, 
                        NSTitledWindowMask  |  NSClosableWindowMask | 
                          NSMiniaturizableWindowMask |    NSResizableWindowMask, # |  NSTexturedBackgroundWindowMask,
                        NSBackingStoreBuffered, 
                        deferCreation 
                    )   

    # deferCreation
    # Specifies whether the window server creates a window device for the window immediately. 
    # When YES, the window server defers creating the window device until the window is moved onscreen. All display messages sent to the window or its views are postponed until the window is created, just before it’s moved onscreen.

    win.setTitle_ ('OpenWorld')
    win.setLevel_ (NSNormalWindowLevel) # 3)                   # floating window
    win.setCollectionBehavior_(1 << 7) # NSWindowCollectionBehaviorFullScreenPrimary



    wf = win.frame()
    x, y = wf.origin
    width, height = wf.size
    s = "origin=(x=%r y=%r) size=(width=%r height=%r)" % (x,y,width,height)

    printB("Win", (win, s))
    win.setViewsNeedDisplay_(objc.NO)
    print_setters(win)

    win_delegate = WinDelegate.alloc().init()
    win.setDelegate_(win_delegate)
    printB("WinDelegate", win_delegate)  # like AppDelegate


    AppHelper.runEventLoop()


if __name__ == '__main__':
    main()



    
        # win.displayIfNeeded()
        # view.setNeedsDisplay_( objc.YES )  
        # win.setFrame_display_( frame , objc.YES )
