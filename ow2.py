#!/Users/donb/projects/VENV/pyobjc25/bin/python
# encoding: utf-8
"""
#!/usr/bin/env python
#!/Users/donb/projects/VENV/pyobjc25/bin/python

untitled.py

Created by donb on 2013-07-02.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

import sys
import os

import objc
from Foundation import NSObject, NSURL

from AppKit import ( NSFont, NSApplication, NSApp,
                        NSApplicationActivationPolicyRegular , NSWindow, NSTitledWindowMask,
                        NSClosableWindowMask, NSMiniaturizableWindowMask, NSResizableWindowMask,
                        NSBackingStoreBuffered, NSNormalWindowLevel, NSColor,
                        NSAttributedString )
                        
from AppKit import ( CALayer, CATextLayer )

from Quartz import   QCComposition , QCCompositionLayer
from Quartz import ( CGImageSourceCreateWithURL, CGImageSourceCreateImageAtIndex, 
                            CGColorCreateGenericRGB, CGColorCreateGenericGray, NSShadow,
                            CIFilter )

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
        app = aNotification.object()

        printB("App", app, only=['acceptsFirstResponder', 'nextResponder']+
                    ['activationPolicy','isActive', 'mainWindow', 'canEnterFullScreenMode','windows',
                                    'currentSystemPresentationOptions', 'delegate', 'presentationOptions'])

        # printB("applicationDidFinishLaunching",app,  add=['mainWindow','currentSystemPresentationOptions'],
        #                             subtract=['applicationIconImage', 'helpMenu', 'gestureEventMask', 'mainMenu', 'menu',
        #                                         'servicesMenu', 'servicesProvider'])
        

         
        win = app.windows()[0]
        
        # The new window creates a view to be its default content view. 
        # You can replace it with your own object by using the setContentView: method.
        
        dragView = OpenView.alloc().init()
        view = dragView
        win.setContentView_(view)

        # view =  win.contentView()

        wf = view.bounds()
        x, y = wf.origin
        width, height = wf.size
        s2 = "origin=(x=%r y=%r) size=(width=%r height=%r)" % (x,y,width,height)

         #    
         # 
         # backingLayer = getQCCompLayer()
         # # backingLayer.setFrame_( win_frame ) # view.frame() )      
         # printB("backingLayer", backingLayer)
         # # print_setters(backingLayer)
         # 
         # if True:
         #     # rootLayer = CALayer.layer()
         #     rootLayer = backingLayer
         #     view.setLayer_(rootLayer)
         #     view.setWantsLayer_( objc.YES )
         # else:
         #     view.setWantsLayer_( objc.YES )
         #     rootLayer = view.layer()
         # 
         # 
         # printB("View",  (view,  s2 )   ) # frame = bounds for origin (0,0)?
         # print_setters(view)
         # 
         # printB("rootLayer", rootLayer)
         
        # rootLayer.setNeedsDisplay()

        # 
        #   serious magic here.  kind of a kickstarter for the Quartz Composer?
        #   here the frame is not (precisely) equal to current window frame.  
        #     difference causes redraw here?  can't just say win.frame()
        #       and is there no other way to say to redraw/start composition?
        #  this magic is for the root layer and for a QCComposition only ?!@?

        # this is needed
        win.makeKeyAndOrderFront_(objc.NULL)

        wf = win.frame()
        x, y = wf.origin
        width, height = wf.size
        magic_delta = 0.2   # must be > 0.1 (!)
        win.setFrame_display_(  (  (  x , y ) , ( width, height + magic_delta ) ) , objc.YES )

        #
        #   end serious magic
        #
        
        layerDict = {
            'origin' : (420,120),
            'size'  :  (120,120),
            'zPosition'  :  12,
            'image_path'  :  "/Users/donb/projects/openworld/gray button 96px.psd",
            'cornerRadius'  :  16,
            'borderWidth'  :  1.0,
        }
        testLayer = createLayer(**layerDict)
        rootLayer.addSublayer_(testLayer)

        
        
        applicationIconImage=app.applicationIconImage()

        layerDict['image']=applicationIconImage
        layerDict['origin']=(100,400)
        layerDict['size']=applicationIconImage.size()
        testLayer3 = createLayer( **layerDict)
        rootLayer.addSublayer_(testLayer3)
        

        printB("testLayer3",  testLayer3  ) # frame = bounds for origin (0,0)?

        
        
        # lake_picture_path = "/Library/Desktop Pictures/Lake.jpg"    
        # theLakeImage = getImage(lake_picture_path)

        layerDict['origin']=(300,300)
        layerDict['image_path']="/Library/Desktop Pictures/Lake.jpg"
        del layerDict['image']        
        layerDict['size']=(300,300)

        testLayer2 = createLayer( **layerDict)
        rootLayer.addSublayer_(testLayer2)


 
        layerDict['origin']=(420,60)
        layerDict['text_string']="full-size and on the 1080p LCD"
        layerDict['zPosition'] = 20
        layerDict['textColor']=NSColor.blackColor()
        
        del layerDict['image_path']
        
        testLayer3 = createTextLayer( **layerDict)
        rootLayer.addSublayer_(testLayer3)



        whiteColor = CGColorCreateGenericRGB(0.0, 0.5, 1.0, 1.0)

        layerDict['textColor']=NSColor.whiteColor()
        layerDict['zPosition'] = 19
        
        testLayer4 = createTextLayer(**layerDict)
        rootLayer.addSublayer_(testLayer4)

        blurFilter = CIFilter.filterWithName_("CIGaussianBlur")
 
        blurFilter.setDefaults()
        # blurFilter.setValue_forKey_( 2.0, "inputRadius" )
        blurFilter.setValue_forKey_( .75, "inputRadius" )
        blurFilter.setName_("blur")
 
        testLayer4.setFilters_( [blurFilter] )

        app.activateIgnoringOtherApps_(objc.YES)

        # r_app = NSRunningApplication.currentApplication()
        # 
        # print "r_app is", r_app
        # 
        # q = r_app.activateWithOptions_(1L)
        # 
        # print "r_app.activateWithOptions_(1L) is", r_app.activateWithOptions_(1L)
        
        
    def applicationWillBecomeActive_(self, aNotification):
        printB("applicationWillBecomeActive",  aNotification.object())
        printB("App", app, only=['acceptsFirstResponder', 'nextResponder']+
                    ['activationPolicy','isActive', 'mainWindow', 'canEnterFullScreenMode','windows',
                                    'currentSystemPresentationOptions', 'delegate', 'presentationOptions'])
        
        # applicationWillBecomeActive seems a good place to "refresh", ie, this is a "new look" at the screen
        
        # workspace = NSWorkspace.sharedWorkspace()
        # activeApps = workspace.runningApplications()
        # printB("runningApplications",  activeApps)
        

    def applicationWillResignActive_(self, aNotification):
        """ Sent by the default notification center immediately before the application is deactivated."""
        printB("applicationWillResignActive",  aNotification.object(), only=['isActive', 'mainWindow'])
        printB("App", app, only=['acceptsFirstResponder', 'nextResponder']+
                    ['activationPolicy','isActive', 'mainWindow', 'canEnterFullScreenMode','windows',
                                    'currentSystemPresentationOptions', 'delegate', 'presentationOptions'])
        
        # activationPolicy                 : 0
        # applicationIconImage             : <NSImage 0x7fe73311b400 Size={128, 128} Reps=(
        # canEnterFullScreenMode           : 0
        # delegate                         : <AppDelegate: 0x7fe733114c90>
        # gestureEventMask                 : 3223060480
        # helpMenu                         : None
        # isActive                         : True
        # mainMenu                         : None
        # menu                             : None
        # presentationOptions              : 0
        # servicesMenu                     : None
        # servicesProvider                 : None
        # windowsMenu                      : None        
        
        
        # in concert with applicationWillBecomeActive, this one might dim or still or quiesce an active display? (ie pause?)
        

    def applicationWillTerminate_(self, aNotification):
        printB("applicationWillTerminate",  aNotification.object())
        printB("App", app, only=['acceptsFirstResponder', 'nextResponder']+
                    ['activationPolicy','isActive', 'mainWindow', 'canEnterFullScreenMode','windows',
                                    'currentSystemPresentationOptions', 'delegate', 'presentationOptions'])
        
        # need to release the lock here as when the
        # application terminates it does not run the rest the
        # original main, only the code that has crossed the
        # pyobc bridge. [https://github.com/gurgeh/selfspy/blob/master/selfspy/sniff_cocoa.py]
            # if cfg.LOCK.is_locked():
            #     cfg.LOCK.release()
        print "\n    Exiting ..."
        
        
    def applicationShouldTerminateAfterLastWindowClosed_(self, theApplication):
        printB("applicationShouldTerminateAfterLastWindowClosed is called.  returns YES",  theApplication)
        printB("App", app, only=['acceptsFirstResponder', 'nextResponder']+
                    ['activationPolicy','isActive', 'mainWindow', 'canEnterFullScreenMode','windows',
                                    'currentSystemPresentationOptions', 'delegate', 'presentationOptions'])
        
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

        printB("windowDidBecomeKey",   win   )
        printB("windowDidBecomeKey",   view.bounds()   )
        

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

from OpenView import OpenView


from printB import printB, print_setters
    
def main():

    app = NSApplication.sharedApplication()
    
    # printB("App", app, only=['acceptsFirstResponder', 'nextResponder'])
    # printB("App", app,  add=['mainWindow','currentSystemPresentationOptions'],
    #                             subtract=['applicationIconImage', 'helpMenu', 'gestureEventMask', 'mainMenu', 'menu',
    #                                         'servicesMenu', 'servicesProvider'])

    printB("App (orig)", app, only=['acceptsFirstResponder', 'nextResponder']+
                ['activationPolicy','isActive', 'mainWindow', 'canEnterFullScreenMode','windows',
                                'currentSystemPresentationOptions', 'delegate', 'presentationOptions'])


    # oh give me a place in the dock, and allow activation…    
    app.setActivationPolicy_( NSApplicationActivationPolicyRegular    ) 
    
    # app.activateIgnoringOtherApps_(objc.YES)


    printB("App", app, only=['acceptsFirstResponder', 'nextResponder']+
                ['activationPolicy','isActive', 'mainWindow', 'canEnterFullScreenMode','windows',
                                'currentSystemPresentationOptions', 'delegate', 'presentationOptions'])


    delegate = AppDelegate.alloc().init()
    NSApp().setDelegate_(delegate)

    #
    #       Win
    #

    win = NSWindow.alloc()

    win_frame = ((100.0, 350.0), (1000.0, 639.0))        
    
    # deferCreation
    
    # Specifies whether the window server creates a window device for the window immediately. 
    # When YES, the window server defers creating the window device until the window is moved onscreen. All display messages sent to the window or its views are postponed until the window is created, just before it’s moved onscreen.

    deferCreation = objc.YES
    # deferCreation = objc.NO

    win.initWithContentRect_styleMask_backing_defer_ (
                        win_frame, 
                            NSTitledWindowMask  |  NSClosableWindowMask | 
                            NSMiniaturizableWindowMask |    NSResizableWindowMask, # |  NSTexturedBackgroundWindowMask,
                        NSBackingStoreBuffered, 
                        deferCreation 
                    )   

    win.setTitle_ ('OpenWorld')
    win.setLevel_ (NSNormalWindowLevel) # 3)                   # floating window
    win.setCollectionBehavior_(1 << 7) # NSWindowCollectionBehaviorFullScreenPrimary

    wf = win.frame()
    x, y = wf.origin
    width, height = wf.size
    s = "origin=(x=%r y=%r) size=(width=%r height=%r)" % (x,y,width,height)

    printB("Win", win, add=['frame'])
    win.setViewsNeedDisplay_(objc.NO)
    # print_setters(win)

    win_delegate = WinDelegate.alloc().init()
    win.setDelegate_(win_delegate)

    printB("WinDelegate", win_delegate)  # like AppDelegate


    AppHelper.runEventLoop()


if __name__ == '__main__':
    main()



    
        # win.displayIfNeeded()
        # view.setNeedsDisplay_( objc.YES )  
        # win.setFrame_display_( frame , objc.YES )
