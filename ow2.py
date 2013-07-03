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

        printB("applicationDidFinishLaunching",app,  add=['mainWindow','currentSystemPresentationOptions'],
                                    subtract=['applicationIconImage', 'helpMenu', 'gestureEventMask', 'mainMenu', 'menu',
                                                'servicesMenu', 'servicesProvider'])
        

         
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

    
        
        QCLayer = getQCCompLayer()
        # QCLayer.setFrame_( win_frame ) # view.frame() )      
        printB("QCLayer", QCLayer)
        # print_setters(QCLayer)
        
        if True:
            # rootLayer = CALayer.layer()
            rootLayer = QCLayer
            view.setLayer_(rootLayer)
            view.setWantsLayer_( objc.YES )
        else:
            view.setWantsLayer_( objc.YES )
            rootLayer = view.layer()


        printB("View",  (view,  s2 )   ) # frame = bounds for origin (0,0)?
        print_setters(view)

        printB("rootLayer", rootLayer)
        
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
        
        # applicationWillBecomeActive seems a good place to "refresh", ie, this is a "new look" at the screen
        
        # workspace = NSWorkspace.sharedWorkspace()
        # activeApps = workspace.runningApplications()
        # printB("runningApplications",  activeApps)
        

    def applicationWillResignActive_(self, aNotification):
        """ Sent by the default notification center immediately before the application is deactivated."""
        printB("applicationWillResignActive",  aNotification.object(), only=['isActive', 'mainWindow'])
        
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
        
        # need to release the lock here as when the
        # application terminates it does not run the rest the
        # original main, only the code that has crossed the
        # pyobc bridge. [https://github.com/gurgeh/selfspy/blob/master/selfspy/sniff_cocoa.py]
            # if cfg.LOCK.is_locked():
            #     cfg.LOCK.release()
        print "\n    Exiting ..."
        
        
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

# from Foundation import NSMakePoint, NSPointInRect, NSCursor, NSMakeRect, NSEqualPoints
# from AppKit import NSView
# 
# # General Event Information
# general_event_info = [ 'context'          ,               
#                         'locationInWindow'            ,    
#                         'modifierFlags'                 ,  
#                         'timestamp'                       ,
#                         'type'                            ,
#                         'window'                          ,
#                         'CGEvent',
#                         'windowNumber'                    
#                         ]
# mouse_event_info =   [
#             'pressedMouseButtons',
#             'doubleClickInterval',
#             'mouseLocation',
#             'buttonNumber',
#             'clickCount',
#             'pressure'  
#             ]
#             
# key_event_info = [
#     'modifierFlags',
#     'keyRepeatDelay',
#     'keyRepeatInterval',
#     'characters',
#     'charactersIgnoringModifiers',
#     'isARepeat',
#     'keyCode'
# ]
# 
# class OpenView(NSView):
#     """."""
#     _locationDefault = NSMakePoint(0.0, 0.0)
#     _itemColorDefault = NSColor.redColor()
#     _backgroundColorDefault = NSColor.whiteColor()
# 
#     # def awakeFromNib(self):       # no nib!
# 
#     def initWithFrame_(self, frame):
#         printB("initWithFrame (frame)",  frame )
#         
#         self.dragging = None
#         
#         result = super(OpenView, self).initWithFrame_(frame)
#         if result is not None:
#             result._location = self._locationDefault
#             result._itemColor = self._itemColorDefault
#             result._backgroundColor = self._backgroundColorDefault
#             
# 
#         printB("initWithFrame (super)",  super(OpenView, self) )
#         printB("initWithFrame (view)",  self )        
#             
#         return result
# 
#     def drawRect_(self, rect):
#         """."""
#         NSColor.whiteColor().set()
#         NSBezierPath.fillRect_(rect)
#         self.itemColor().set()
#         NSBezierPath.fillRect_(self.calculatedItemBounds())
# 
#     def isOpaque(self):
#         """."""
#         return (self.backgroundColor().alphaComponent() >= 1.0)
# 
#     def offsetLocationByX_andY_(self, x, y):
#         """."""
#         self.setNeedsDisplayInRect_(self.calculatedItemBounds())
#         if self.isFlipped():
#             invertDeltaY = -1
#         else:
#             invertDeltaY = 1
#         self.location().x = self.location().x + x
#         self.location().y = self.location().y + y * invertDeltaY
#         self.setNeedsDisplayInRect_(self.calculatedItemBounds())
# 
#     def mouseDown_(self, event):
# 
#         printB("mouseDown",  event  ,only=mouse_event_info+general_event_info)
# 
#         clickLocation = self.convertPoint_fromView_(event.locationInWindow(),
#                                                     None)
#         itemHit = self.isPointInItem_(clickLocation)
#         if itemHit:
#             self.dragging = True
#             self.lastDragLocation = clickLocation
#             NSCursor.closedHandCursor().push()
# 
# 
#     def mouseDragged_(self, event):
#         """."""
#         
#         x = [  'eventNumber',
#                 'deltaX',
#                 'deltaY' 
#                 ]
# 
#         printB("mouseDragged",  event, only = mouse_event_info+general_event_info+x)
#         if self.dragging:
#             newDragLocation = self.convertPoint_fromView_(
#                 event.locationInWindow(),
#                 None
#             )
#             self.offsetLocationByX_andY_(
#                 newDragLocation.x - self.lastDragLocation.x,
#                 newDragLocation.y - self.lastDragLocation.y
#             )
#             self.lastDragLocation = newDragLocation
#             self.autoscroll_(event)
# 
#     def mouseUp_(self, event):
#         """."""
#         self.dragging = False
#         # NSCursor has both an instance and a class method w/ the name 'pop'
#         NSCursor.pyobjc_classMethods.pop()
#         self.window().invalidateCursorRectsForView_(self)
# 
#     def acceptsFirstResponder(self):
#         """."""
#         return True
# 
#     @objc.IBAction      # haha only kidding!
#     def setItemPropertiesToDefault_(self, sender):
#         """."""
#         self.setLocation_(self._locationDefault)
#         self.setItemColor_(self._itemColorDefault)
#         self.setBackgroundColor_(self._backgroundColorDefault)
# 
#     def keyDown_(self, event):
#         print "keydown, event is %r" % event
#         printB("keyDown",  event, only = general_event_info+key_event_info)
# 
#         handled = False
#         characters = event.charactersIgnoringModifiers()
#         
#         if characters.isEqual_('r'):
#             handled = True
#             self.setItemPropertiesToDefault_(self)
#         if handled is False:
#             q = super(OpenView, self).keyDown_(event)  # beeps if not handled/forwarded to super (who doesn't know what to do?)
#             print "keydown: q is", q
#             
#     def setLocation_(self, point):
#         """."""
#         if not NSEqualPoints(point, self.location()):
#             self.setNeedsDisplayInRect_(self.calculatedItemBounds())
#             self._location = point
#             self.setNeedsDisplayInRect_(self.calculatedItemBounds())
#             self.window().invalidateCursorRectsForView_(self)
# 
#     def location(self):
#         """."""
#         return self._location
# 
#     def setBackgroundColor_(self, aColor):
#         """."""
#         if not self.backgroundColor().isEqual_(aColor):
#             self._backgroundColor = aColor
#             self.setNeedsDisplayInRect_(self.calculatedItemBounds())
# 
#     def backgroundColor(self):
#         """."""
#         return self._backgroundColor
# 
#     def setItemColor_(self, aColor):
#         """."""
#         if not self.itemColor().isEqual_(aColor):
#             self._itemColor = aColor
#             self.setNeedsDisplayInRect_(self.calculatedItemBounds())
# 
#     def itemColor(self):
#         """."""
#         return self._itemColor
# 
#     def calculatedItemBounds(self):
#         """."""
#         return NSMakeRect(self.location().x, self.location().y,
#                           60.0, 20.0)
# 
#     def isPointInItem_(self, testPoint):
#         """."""
#         itemHit = NSPointInRect(testPoint, self.calculatedItemBounds())
#         if itemHit:
#             pass
#         return itemHit

    

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

from printB import printB, print_setters
    
def main():

    app = NSApplication.sharedApplication()
    printB("App", app,  add=['mainWindow','currentSystemPresentationOptions'],
                                subtract=['applicationIconImage', 'helpMenu', 'gestureEventMask', 'mainMenu', 'menu',
                                            'servicesMenu', 'servicesProvider'])

    # oh give me a place in the dock, and allow activation…    
    app.setActivationPolicy_( NSApplicationActivationPolicyRegular    ) 
    
    # app.activateIgnoringOtherApps_(objc.YES)


    print_setters(app, only=['activationPolicy','isActive', 'mainWindow', 'canEnterFullScreenMode','windows',
                                'currentSystemPresentationOptions'])


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
