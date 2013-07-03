#!/usr/bin/env python
# encoding: utf-8

""" openworld.py 
"""

import objc
from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper

print  "objc.__version__ is", objc.__version__

from Quartz import CGImageSourceCreateWithURL, CGImageSourceCreateImageAtIndex, QCCompositionLayer, QCComposition, \
                            CGColorCreateGenericRGB, CGColorCreateGenericGray, NSShadow


"""
    It is possible to build full Cocoa apps without InterfaceBuilder.
    
"""

class AppDelegate (NSObject):

    def applicationWillFinishLaunching_(self, aNotification):
        print "applicationWillFinishLaunching.  name is %r, object is %r" % ( aNotification.name(), aNotification.object())
        # the following seem to be important to having the composition get its initial drawing in
        global win
        
        frame = ((100.0, 350.0), (871.0, 490.0))        
        win.setFrame_display_( frame , objc.YES )

        # Sets a given view as the one that’s made first responder (also called the key view) the first time the window is placed onscreen.
        # 
        view = win.contentView()
        win.setInitialFirstResponder_(view)
        
        
        q = win.initialFirstResponder()
        print "win.initialFirstResponder() is: " , q

        
    def applicationDidFinishLaunching_(self, aNotification):
        print "applicationDidFinishLaunching  name is %r, object is %r" % ( aNotification.name(), aNotification.object())
        
        print "Hello, World!"
        
    def applicationWillTerminate_(self, aNotification):
        print "applicationWillTerminate  name is %r, object is %r" % ( aNotification.name(), aNotification.object())

    # aNotification
    # A notification named NSApplicationWillTerminateNotification. Calling the object method of this notification returns the NSApplication object itself.
    # Discussion
    # Your delegate can use this method to perform any final cleanup before the application terminates.

    def applicationDidUnhide_(self, aNotification):
        print "applicationDidUnhide  name is %r, object is %r" % ( aNotification.name(), aNotification.object())

    def applicationShouldTerminateAfterLastWindowClosed_(self, theApplication):
        print "applicationShouldTerminateAfterLastWindowClosed  theApplication is %r" % ( theApplication )
        return objc.YES
        
    # when last window is closed this happens:
    # applicationShouldTerminateAfterLastWindowClosed  theApplication is <NSApplication: 0x7fa12c30fd70>
    # applicationWillTerminate  name is u'NSApplicationWillTerminateNotification', object is <NSApplication: 0x7fa12c30fd70>
    
        
    def applicationWillBecomeActive_(self, aNotification):
        print "applicationWillBecomeActive  name is %r, object is %r" % ( aNotification.name(), aNotification.object())
        # Returns the currently focused NSView object, or nil if there is none.

        print "NSView.focusView() is", NSView.focusView()

    def applicationWillResignActive_(self, aNotification):
        """ Sent by the default notification center immediately before the application is deactivated."""
        print "applicationWillResignActive  name is %r, object is %r" % ( aNotification.name(), aNotification.object())

        

    def sayHello_(self, sender):
        print "Hello again, World!"
    
        q = NSApp().currentEvent()
        print "NSApp().currentEvent is: " , q

        # app.currentEvent is:  NSEvent: type=LMouseUp loc=(48,32) time=291452.6 flags=0x100 win=0x0 winNum=19512 ctxt=0x0 evNum=4811 click=1 buttonNumber=0 pressure=0



    def ztoggleFullScreen_(self, sender):
        print "toggleFullScreen!(app)"


    def keyDown_( self, event):
        print "keyDown  event (app) is %r" % ( event )

class WinDelegate (NSObject):

    # this handler works but can jsut sent toggle full screen to God/NULL/the infinite/the applicatoin and it will also work

    # def ztoggleFullScreen_(self, sender):
    #     print "toggleFullScreen!(win delegate)"
    #     print "toggleFullScreen  sender is %r" % ( sender )
    #     # toggleFullScreen  sender is <NSButton: 0x7faf1ba3b900>
    # 
    #     global win
    #     win.toggleFullScreen_(objc.nil)


 
    # these happen in this order:
    
    #  Will Enter, Did Enter, Will Exit, Did Exit
    
    # windowWillEnterFullScreen  name is u'NSWindowWillEnterFullScreenNotification', object is <NSWindow: 0x7fa6d7319e00>
    # windowDidResize  name is u'NSWindowDidResizeNotification', object is <NSWindow: 0x7fa6d7319e00>
    # windowDidEnterFullScreen  name is u'NSWindowDidEnterFullScreenNotification', object is <NSWindow: 0x7fa6d7319e00>

    # windowWillExitFullScreen  name is u'NSWindowWillExitFullScreenNotification', object is <NSWindow: 0x7fa6d7319e00>
    # windowDidResize  name is u'NSWindowDidResizeNotification', object is <NSWindow: 0x7fa6d7319e00>
    # windowDidExitFullScreen  name is u'NSWindowDidExitFullScreenNotification', object is <NSWindow: 0x7fa6d7319e00>
        
    
        
    def windowWillEnterFullScreen_(self, aNotification):
        """The window just entered full-screen mode."""
        print "windowWillEnterFullScreen  name is %r, object is %r" % ( aNotification.name(), aNotification.object())

    def windowWillExitFullScreen_(self, aNotification):
        """The window just entered full-screen mode."""
        print "windowWillExitFullScreen  name is %r, object is %r" % ( aNotification.name(), aNotification.object())

    def windowDidExitFullScreen_(self, aNotification):
        """The window just entered full-screen mode."""
        print "windowDidExitFullScreen  name is %r, object is %r" % ( aNotification.name(), aNotification.object())

    def windowDidEnterFullScreen_(self, aNotification):
        """The window just entered full-screen mode."""
        print "windowDidEnterFullScreen  name is %r, object is %r" % ( aNotification.name(), aNotification.object())


    def windowDidResize_(self, aNotification):
        """Informs the delegate that the window has been resized."""
        print "windowDidResize  name is %r, object is %r" % ( aNotification.name(), aNotification.object())
        
        # windowDidResize  name is u'NSWindowDidResizeNotification', object is <NSWindow: 0x7fca963a8b90>

        win = aNotification.object()
        
        # print "aNotification.object() is", aNotification.object(), "win is", win
        
        # z = win.isMainWindow()
        # print "win.isMainWindow is ", z
        # z = win.isKeyWindow()
        # print "win.isKeyWindow is ", z
        
        # win.makeKeyWindow()
    
        # z = win.isMainWindow()
        # print "win.isMainWindow is ", z
        # z = win.isKeyWindow()
        # print "win.isKeyWindow is ", z

        z = win.frame()
        print "win.frame is ", z


        view = win.contentView()
                
        # 
        #   rootLayer
        # 
 
        global exampleQCCompositionLayer
        

        rootLayer =         view.layer()



        rootLayer.setBounds_(  view.bounds() )
        # rootLayer.setBounds_(  (view.bounds().origin, (view.bounds().size.width-100.0, view.bounds().size.height - 100.0 ))  ) # ( (100, 100)  , (500, 500) )  )      
        # view.bounds() is <NSRect origin=<NSPoint x=0.0 y=0.0> size=<NSSize width=871.0 height=490.0>>
        
        print "rootLayer.bounds() is:", rootLayer.bounds()
        # rootLayer.setShadowColor_(NSColor.redColor())
        # rootLayer.setShadowOpacity_( 1.0 )
        # rootLayer.setShadowRadius_(4.0)
        # rootLayer.setShadowOffset_((5.0, 5.0))
        
        # print "view.shadow() is:", view.shadow()


        shadow = NSShadow.alloc().init()
        shadowColor = NSColor.colorWithCalibratedWhite_alpha_(1.0 ,1.0  )
        shadow.setShadowColor_( shadowColor ) #  NSColor.redColor() )
        shadow.setShadowOffset_( (10.0, 10.0) )
        shadow.setShadowBlurRadius_(10.0) 
        
        view.setShadow_(shadow)
        print "view.shadow() is:", view.shadow()

        rootLayer.setMasksToBounds_( objc.YES )     # YES, it really does clip everything!
        
        rootLayer.setCornerRadius_(  20.0  )

        global cat, cat2, testLayer, sublayer

        textBkgndColor = CGColorCreateGenericRGB(0.8, 0.7, 0.1, 0.5);  # yellowish
        
        rootLayer.setBackgroundColor_( textBkgndColor )
        
        rootLayer.addSublayer_(cat)
        rootLayer.addSublayer_(cat2)
        rootLayer.addSublayer_(testLayer)
        rootLayer.addSublayer_(sublayer)

        print "rootLayer.sublayers() is", rootLayer.sublayers()
        print "rootLayer.contents() is", rootLayer.contents()
        

    # # windowDidUpdate happens a lot!
    # def windowDidUpdate_(self, aNotification ):
    #     print "windowDidUpdate  name is %r, object is %r" % ( aNotification.name(), aNotification.object())

    def windowDidBecomeKey_(self, aNotification ):
        """ Informs the delegate that the window has become the key window."""    
        print "windowDidBecomeKey  name is %r, object is %r" % ( aNotification.name(), aNotification.object())

    def windowDidBecomeMain_(self, aNotification ):
        """ Informs the delegate that the window has become the main window."""    
        print "windowDidBecomeMain_  name is %r, object is %r" % ( aNotification.name(), aNotification.object())

    # You can retrieve the window object in question by sending object to notification (ie, aNotification.object() )



    # this (and the other delegate callbacks) are called by ("receive a notification sent from")
    #           the NSNotificationCenter, when, in this case,  the window receives (executes)  [ NSWindow becomeKeyWindow ]
    
    # 7   Foundation                          0x00007fff96417fc3 -[NSNotificationCenter postNotificationName:object:userInfo:] + 65
    # 8   AppKit                              0x00007fff94373886 -[NSWindow becomeKeyWindow] + 1345
    
    # becomeKeyWindow is a method on Window that could be overriden/subclassed but is more easily "hooked" via the delegate
    #       which just conveniently forwards the call via the notification center.
    
    # becomeKeyWindow is "Invoked automatically to inform the window that it has become the key window; never invoke this method directly."
    # [https://developer.apple.com/library/mac/#documentation/cocoa/reference/ApplicationKit/Classes/NSWindow_Class/Reference/Reference.html#//apple_ref/doc/c_ref/NSWindow]

    
    def windowWillClose_(self, aNotification ):
        """ Tells the delegate that the window is about to close."""
    
        print "windowWillClose  name is %r, object is %r" % ( aNotification.name(), aNotification.object())


    def windowShouldClose_(self, sender):
        # Tells the delegate that the user has attempted to close a window or the window has received a performClose: message.
        print "windowShouldClose  sender is %r" % ( sender )
        # YES to allow sender to be closed; otherwise, NO.

        return objc.YES
        
        # windowShouldClose  sender is <NSWindow: 0x7fd8b4b1e8c0>
        # applicationShouldTerminateAfterLastWindowClosed  theApplication is <NSApplication: 0x7fd8b4b081c0>
        # applicationWillTerminate  name is u'NSApplicationWillTerminateNotification', object is <NSApplication: 0x7fd8b4b081c0>
        
    def keyDown_( self, event):
        print "keyDown  event is %r" % ( event )



    # // -------------------------------------------------------------------------------
    # //  window:willUseFullScreenContentSize:proposedSize
    # //
    # //  A window's delegate can optionally override this method, to specify a different
    # //  full screen size for the window. This delegate method override's the window's full
    # //  screen content size to include a border space around it.
    # // -------------------------------------------------------------------------------
    # def window_willUseFullScreenContentSize_(self, window, proposedSize):
    #     
    #     print "willUseFullScreenContentSize"
    #     print "willUseFullScreenContentSize  window is %r,  proposedSize is %r" % ( window, proposedSize )
    # 
    # 
    #     # leave a border space around our full screen window
    # 
    #     return NSMakeSize(proposedSize.width - 180, proposedSize.height - 100)



def main():
    
    #
    #       app
    #
    
    
    # The sharedApplication class method initializes the display environment and 
    # connects your program to the window server and the display server. 
    
    app = NSApplication.sharedApplication()

    # sharedApplication only performs the initialization once; 
    # if you invoke it more than once, it simply returns the NSApplication object it created previously.

    # sharedApplication also initializes the global variable NSApp, 
    # which you use to retrieve the NSApplication instance. 
    
    print "NSApp is:", NSApp(), "local app is:", app
    assert( NSApp() == app )
    
    # The NSApplication object maintains a list of all the NSWindow objects 
    # the application uses, so it can retrieve any of the application’s NSView objects. 


    # we must keep a reference to the delegate object ourselves,
    # NSApp.setDelegate_() doesn't retain it. A local variable is
    # enough here.
    
    delegate = AppDelegate.alloc().init()
    NSApp().setDelegate_(delegate)

    # app.windows: 0 ()

    # NSApplication performs the important task of receiving events from
    # the window server and distributing them to the proper NSResponder objects.

    # NSApp translates an event into an NSEvent object, then forwards
    # the NSEvent object to the affected NSWindow object.

    # All keyboard and mouse events go directly to the NSWindow object associated with the event.
    # The only exception to this rule is if the Command key is pressed when a key-down event occurs;
    # in this case, every NSWindow object has an opportunity to respond to the event.
    # When an NSWindow object receives an NSEvent object from NSApp,
    # it distributes it to the objects in its view hierarchy.

    
    
    global win
    win = NSWindow.alloc()
    # frame = ((100.0, 500.0), (550.0, 400.0))
    frame = ((100.0, 350.0), (871.0, 490.0))        
    
    win.initWithContentRect_styleMask_backing_defer_ (
                        frame, 
                        NSTitledWindowMask  |  NSClosableWindowMask | 
                          NSMiniaturizableWindowMask | 
                          NSResizableWindowMask, # |  NSTexturedBackgroundWindowMask,
                        NSBackingStoreBuffered, 
                        objc.YES # 0
                    )   #    15,



    win.setTitle_ ('OpenWorld')
    win.setLevel_ (NSNormalWindowLevel) # 3)                   # floating window


    w = app.windows()    
    print "app.windows after alloc() and init are:", len(w), w
    # app.windows (after NSWindow.alloc: 1 (   "<NSWindow: 0x7fec23cd3470>"   )


    # A single NSWindow object corresponds to at most one onscreen window.
    # The two principal functions of a window are to provide an area in which views
    # can be placed and to accept and distribute, to the appropriate views,
    # events the user instigates through actions with the mouse and keyboard.


    # // To specify we want our given window to be the full screen primary one, we can
    # // use the following:
    win.setCollectionBehavior_(1 << 7) # NSWindowCollectionBehaviorFullScreenPrimary
    win.setOpaque_(objc.YES)
    # win.setViewsNeedDisplay_(objc.YES)  # not needed, view knows when it needs display.

    # win.makeKeyWindow()
    # 
    # z = win.isMainWindow()
    # print "win.isMainWindow is ", z
    # z = win.isKeyWindow()
    # print "win.isKeyWindow is ", z

    # // Make the window the first responder to get keystrokes
    x = win.makeFirstResponder_(win)
    print "win.makeFirstResponder_(win) is", x
    
    


    # WinDelegate
    
    win_delegate = WinDelegate.alloc().init()
    win.setDelegate_(win_delegate)

    # NSBackingStoreBuffered
    # The window renders all drawing into a display buffer and then flushes it to the screen.
    # You should use this mode. It supports hardware acceleration, Quartz drawing, and takes advantage of the GPU when possible. It also supports alpha channel drawing, opacity controls, using the compositor.

    # Specifies whether the window server creates a window device for the window immediately. When YES, the window server defers creating the window device until the window is moved onscreen. All display messages sent to the window or its views are postponed until the window is created, just before it’s moved onscreen.
    
    
    #
    #   view
    #
    

    #
    #   The NSView class provides a structure for drawing, printing, and handling events.
    #
    # Cocoa provides a high-level class, NSView, that implements the fundamental view behavior.
    # An NSView instance defines the rectangular location of the view, referred to as its frame rectangle,
    # and takes responsibility for rendering a visual representation of its data within that area.
    # In addition to drawing, a view takes responsibility for handling user events directed towards the view.


  
    view = win.contentView()
    print "win.contentView is ", view
    # win.contentView is  <NSView: 0x7fa53b48b690>
    
    print "view.frame() is", view.frame()
    # view.frame() is <NSRect origin=<NSPoint x=0.0 y=0.0> size=<NSSize width=550.0 height=400.0>>
    
    print "view.bounds() is", view.bounds()
    # view.bounds() is <NSRect origin=<NSPoint x=0.0 y=0.0> size=<NSSize width=550.0 height=400.0>>
    
    print "view.window() is", view.window()
    
    

    # NSView objects (also know, simply, as view objects or views) are arranged within an NSWindow object,
    # in a nested hierarchy of subviews. A view object claims a rectangular region of its enclosing superview,
    # is responsible for all drawing within that region, and is eligible to receive mouse events
    # occurring in it as well. In addition to these major responsibilities, NSView handles dragging of
    # icons and works with the NSScrollView class to support efficient scrolling.
    # 
    # Most of the functionality of NSView either is automatically invoked by the Application Kit,
    # or is available in Interface Builder. Unless you’re implementing a concrete subclass of NSView
    # or working intimately with the content of the view hierarchy at runtime,
    # you don’t need to know much about this class’s interface.
    # See “Commonly Used Methods” for methods you might use regardless.
    # 

    print "view.superview() is", view.superview()
    print "view.superview().bottomCornerRounded() is", view.superview().bottomCornerRounded()
    # view.superview().setBottomCornerRounded_(0)
    # view.superview().bottomCornerRounded() is 1
    
    # print "view.superview().bottomCornerRounded() is", view.superview().bottomCornerRounded()
    # view.superview() is <NSGrayFrame: 0x7fb50bd5db50>


    # # print "view.subviews() is", view.subviews()  # ()
    # print "view.tag() is", view.tag()  # view.tag() is -1
    # 
    # 
    # # Returns the currently focused NSView object, or nil if there is none.
    # 
    # print "NSView.focusView() is", NSView.focusView()


    # For views you create programmatically, call the view’s setWantsLayer: method and pass a value of YES to indicate that the view should use layers.

    # (donb) views are really, really, usually created in inteface builder as subclasses which are instantiated and inserted into place at "NIB-time"



    # default is that views are born not using a layer as its backing store

    print "view.wantsLayer() is", view.wantsLayer()
    print "view.layer() is", view.layer()
    # view.wantsLayer() is False
    # view.layer() is None


    # The order that setWantsLayer: and setLayer: are called is important,
    # it makes the distinction between a layer-backed view and a layer-hosting view.
    
    # 
    #   A layer-backed view
    #
    # A layer-backed view is a view that is backed by a Core Animation layer.
    # Any drawing done by the view is cached in the backing layer.
    # You configure a layer-backed view by invoking setWantsLayer: with a value of YES.
    # The view class automatically creates a backing layer for you (using makeBackingLayer if overridden),
    # and you must use the view class’s drawing mechanisms.
    # When using layer-backed views you should never interact directly with the layer.
    # Instead you must use the standard view programming practices.
    
    #
    #   A layer-hosting view 
    #
    # A layer-hosting view is a view that contains a Core Animation layer
    # that you intend to manipulate directly. You create a layer-hosting view by instantiating a
    # Core Animation layer class and supplying that layer to the view’s setLayer: method.
    # After doing so, you then invoke setWantsLayer: with a value of YES.
    # This method order is crucial. When using a layer-hosting view you should not rely on the view for drawing,
    # nor should you add subviews to the layer-hosting view.
    # The root layer (the layer set using setLayer:) should be treated as the root layer of the layer tree
    # and you should only use Core Animation drawing and animation methods.
    # You still use the view for handling mouse and keyboard events,
    # but any resulting drawing must be handled by Core Animation.
    # 
    
    #
    # setWantsLayer:
    #
    # Specifies whether the receiver and its subviews use a Core Animation layer as a backing store.
    # 
    # - (void)setWantsLayer:(BOOL)flag
    # Parameters
    # 
    # YES if the receiver and its subviews should use a Core Animation layer as its backing store, otherwise NO.
    #  


    # To create a layer-hosting view, create your layer object and associate it with the view before displaying the view onscreen, as shown in Listing 2-2. In addition to setting the layer object, you must still call the setWantsLayer: method to let the view know that it should use layers.
    # 
    # Listing 2-2  Creating a layer-hosting view
    # // Create myView...
    #  
    # [myView setWantsLayer:YES];
    # CATiledLayer* rootLayer = [CATiledLayer layer];
    # [myView setLayer:rootLayer];
    #  
    
    
    # // Create a QCComposition Layer with the path to that composition
    # // A QCCompositionLayer is a CAOpenGLLayer with the asynchronous property set to YES
    # // therefore it does not need to be invalidated to display (it will automatically be invalidated).


    # cpath = "/Users/donb/Library/Compositions/gradient_2.qtz"
    cpath = "/Users/donb/Library/Compositions/gradient3_light.qtz"
    # cpath = "/Users/donb/Library/Compositions/v12 grey background.qtz"

    
    
    

    # exampleQCCompositionLayer = QCCompositionLayer.compositionLayerWithFile_(cpath)
    
    theQCComposition = QCComposition.compositionWithFile_(cpath)
    
    print "theQCComposition is", theQCComposition
    # print "theQCComposition.attributes() are", theQCComposition.attributes()
    print "theQCComposition.identifier() are", theQCComposition.identifier()
    print "theQCComposition.inputKeys() are", theQCComposition.inputKeys()



    # theQCComposition.inputKeys() are (
    #     "_protocolInput_PrimaryColor",
    #     "_protocolInput_SecondaryColor",
    #     direction,
    #     position
    # )
    
    
    
    global exampleQCCompositionLayer
    exampleQCCompositionLayer = QCCompositionLayer.compositionLayerWithComposition_(theQCComposition)

    zPosition = 0
    exampleQCCompositionLayer.setZPosition_(zPosition)



    # composition layer has composition renderer protocol

    # x = exampleQCCompositionLayer.valueForInputKey_("_protocolInput_PrimaryColor")    
    # print '"_protocolInput_PrimaryColor" is:', x
    # 
    # x = exampleQCCompositionLayer.valueForInputKey_("position")    
    # print '"position" is:', x
    # # "position" is: 0.5
    # 
    # # exampleQCCompositionLayer.setValue_forInputKey_(0.75, "position")        # setValue:forInputKey

    origin=(0+50,0+50)
    size = (871.0-100, 490.0-100)
    exampleQCCompositionLayer.setBounds_(  ( origin , size )  )      
    exampleQCCompositionLayer.setFrame_(  ( origin , size )  )      

    x = exampleQCCompositionLayer.propertyListFromInputValues()
    print '"propertyListFromInputValues" are:', x

    x = exampleQCCompositionLayer.bounds()
    print '"exampleQCCompositionLayer.bounds" are:', x

    x = exampleQCCompositionLayer.frame()
    print '"exampleQCCompositionLayer.frame" are:', x
    
    # "propertyListFromInputValues" are: {
    #     "_protocolInput_PrimaryColor" =     {
    #         alpha = 1;
    #         blue = "0.5417715310113248";
    #         green = "0.6321745184063987";
    #         red = "0.7371773097826086";
    #     };
    #     "_protocolInput_SecondaryColor" =     {
    #         alpha = 1;
    #         blue = "0.1003563550287777";
    #         green = "0.1213909646739131";
    #         red = "0.1123059824201185";
    #     };
    #     direction = 0;
    #     position = "0.5";
    # }

    # rootLayer = exampleQCCompositionLayer
    # rootLayer = CATextLayer.alloc().init()

    
    # exampleQCCompositionLayer.setFrame_(NSRectToCGRect( view.frame() ) )
    global cat, cat2, testLayer, sublayer
    
    
    textBkgndColor = CGColorCreateGenericRGB(0.8, 0.8, 0.8, 0.0);  # light gray

    testLayer = CALayer.alloc().init()
    origin=(420,120)
    size = (300,300)
    testLayer.setFrame_(  ( origin , size )  )      
    testLayer.setBackgroundColor_( textBkgndColor )
    zPosition = 12
    testLayer.setZPosition_(zPosition)

    path = "/Library/Desktop Pictures/Lake.jpg"    
    url = NSURL.fileURLWithPath_(path)
    imagesrc = CGImageSourceCreateWithURL(url, None)        
    theLakeImage = CGImageSourceCreateImageAtIndex(imagesrc, 0, None);
    testLayer.setContents_( theLakeImage )


    testLayer.setShadowColor_(NSColor.redColor())
    testLayer.setShadowOpacity_( 1.0 )
    testLayer.setShadowRadius_(4.0)
    testLayer.setShadowOffset_((5.0, 5.0))
    testLayer.setMasksToBounds_( objc.NO )
    testLayer.setCornerRadius_(  13.0  )
    
    print [(a, getattr(testLayer,a)()) for a in ['shadowColor', 'shadowOffset', 'shadowOpacity', 'shadowPath', 'shadowRadius'] ]

    # view = [[AnimatedView alloc] initWithFrame:NSMakeRect(0, 0, 100, 100)];
    # [view setWantsLayer:YES];
    # [view setLayer:[QCCompositionLayer compositionLayerWithComposition:composition]];
    # [window setContentView:view];
    # [view release];
    # 
    # /* Show window */
    # [window makeKeyAndOrderFront:nil];

    # rootLayer = CATiledLayer.layer()
    # view.layer() is <CATiledLayer: 0x7fe095008030>




    
    cat = CATextLayer.alloc().init()
    cat.setString_("Hello Wonko!")
    textColor0      = CGColorCreateGenericRGB(0.1, 0.2, 0.3, 1.0)
    cat.setForegroundColor_(textColor0)
    cat.setBackgroundColor_(textBkgndColor)
    zPosition = 12
    cat.setZPosition_(zPosition)
    origin=(120,120)
    size = (300,100)
    cat.setFrame_(  ( origin , size )  )      

    print "cat.position() is", cat.position()


    #########
    # font           = NSFont.fontWithName_size_("HelveticaNeue-Medium",14.0)
    # font           = NSFont.fontWithName_size_("HelveticaNeue-Medium",36.0)
    # font           = NSFont.fontWithName_size_("Avenir Next LT Pro Ultra Light Italic",36.0)
    font           = NSFont.fontWithName_size_("Avenir Next LT Pro Italic",36.0)
    
    print "font is", font
    print "font.displayName() is", font.displayName()
    
    # attributes = NSDictionary.dictionaryWithObjectsAndKeys_(font, NSFontAttributeName, None )
    # print "attributes is", attributes


 
    s = "full-size and on the 1080p LCD"
    textColor2      = CGColorCreateGenericRGB(0.4, 0.2, 0.1, 1.0)
    textColor_h      = NSColor.whiteColor() # CGColorCreateGenericRGB(0.0, 0.0, 0.0, 1.0)
    
    shadow = NSShadow.alloc().init()
    # shadow.setShadowColor_(NSColor.whiteColor())


    shadowColor = NSColor.colorWithCalibratedWhite_alpha_(0.0 , 0.25  )

    shadow.setShadowColor_( shadowColor ) #  NSColor.redColor() )
    shadow.setShadowOffset_( (10.0, 10.0) )
    shadow.setShadowBlurRadius_(10.0) 


    # [shadow setShadowOffset:CGSizeMake (1.0, 1.0)];
    # [shadow setShadowBlurRadius:1];
    
    print "shadow is", shadow
    # shadow is NSShadow {1, 1} blur = 1 color = {NSCalibratedWhiteColorSpace 1 1}
    
    # shadow set on CALayer, view, etc
    # NSShadow *shadow = [[[NSShadow alloc] init] autorelease];
    # [shadow setShadowBlurRadius:3.0];
    # [shadow setShadowOffset:NSMakeSize(0.0, 5.0)];
    # [shadow setShadowColor:[NSColor colorWithCalibratedWhite:0.0 alpha:0.6]];
    # [shadow set];
    # // continue with your drawing...
    
    # shadow specified as an attribute of a string

    # @Jonathan: that was what I was about to post as an answer indeed. setShadow: simply copies the shadow's properties to the Core Animation layer, so the view must be backed by a CALayer. This is also noticeable when you want to apply a shadow to a view using Interface Builder. – Joost Jan 24 '11 at 21:21
    # Ayup. Have had my head in iOS for a while, so it briefly slipped my mind that on the Mac, views are not layer-backed by default. :) – Jonathan Grynspan Jan 24 '11 at 21:32
    # [http://stackoverflow.com/questions/4704047/adding-a-shadow-to-a-nsimageview]


    paragraphStyle = NSMutableParagraphStyle.alloc().init()
    paragraphStyle.setAlignment_(1) # NSTextAlignmentCenter
    
    # s3 = NSAttributedString.alloc().initWithString_attributes_(s, { "NSFont":font , NSForegroundColorAttributeName: textColor2} )
    s3 = NSAttributedString.alloc().initWithString_attributes_(s, { "NSFont":font ,
                                                            NSShadowAttributeName : shadow ,
                                                                        NSParagraphStyleAttributeName:paragraphStyle } ) # default is black is fine
    s3_h = NSAttributedString.alloc().initWithString_attributes_(s, { "NSFont":font , NSForegroundColorAttributeName: textColor_h,
                                            NSShadowAttributeName : shadow ,
                                                                NSParagraphStyleAttributeName:paragraphStyle } )

    # print "s3.size() is", s3.size()    # s3.size() is <NSSize width=293.0 height=21.0>

    # cat2.setString_("Hello Rounder-Upers!")
    # textColor      = CGColorCreateGenericRGB(0.4, 0.2, 0.1, 1.0)
    # cat2.setForegroundColor_(textColor)
    # cat2.setBackgroundColor_(textBkgndColor)
    # # cat2.setPosition_( (140,40)  )

    cat2 = CATextLayer.alloc().init()

    textColor      =  CGColorCreateGenericRGB(1.0, 1.0, 1.0, 1.0)
    
    cat2.setForegroundColor_(textColor0)
    cat2.setBackgroundColor_(NSColor.whiteColor()) # textBkgndColor)
    # # cat2.setPosition_( (140,40)  )

    # print dir(cat2)
    # sys.exit()

    x = cat2.foregroundColor()
    print "cat2.foregroundColor() is",x

    x = cat2.backgroundColor()
    print "cat2.backgroundColor() is",x

    
    cat2.setString_(s3)

    # s4 = cat2.string()
    # print "size is", s4.size()  # size is <NSSize width=730.4039999999998 height=37.0>
    # print "s4 is", s4, "s3 == s4", s3 == s4

    origin=(20,20)

    size = s3.size()
    
    cat2.setFrame_(  ( origin , size )  )      
    zPosition = 3
    cat2.setZPosition_(zPosition)
    
    print "cat2.frame() is", cat2.frame()

    # textColor_h      = CGColorCreateGenericRGB(1.0, 1.0, 1.0, 0)
    # textColor_h      =  CGColorCreateGenericRGB(1.0, 0.0, 0.0, 1)
    textColor_h      = CGColorCreateGenericGray(1.0, 1.0)                # dark charcoal, almost black
    
    cat_h2 = CATextLayer.alloc().init()
    cat_h2.setString_(s3_h)
    cat_h2.setForegroundColor_(textColor_h)
    cat_h2.setBackgroundColor_(textBkgndColor)

    x = cat_h2.foregroundColor()
    print "cat_h2.foregroundColor() is",x

    origin_h2=(origin[0]+0,origin[1]-0.5) # relative to super_layer?
    cat_h2.setFrame_(  ( origin_h2 , size )  )      

    print "cat_h2.frame() is", cat_h2.frame()




    zPosition = 3
    cat_h2.setZPosition_(zPosition-2)


    ##########
    

    # rootLayer = cat2
    
    # rootLayer = CALayer.layer()                                     # [[CALayer layer] retain]
    
    # rootLayer.setBounds_( view.bounds() )                           # NSRectToCGRect(self.bounds)

    exampleQCCompositionLayer.setFrame_( view.frame() )      


    # rootLayer = exampleQCCompositionLayer
    

    cat.setMasksToBounds_( objc.NO )
    cat2.setMasksToBounds_( objc.NO )

    cat2.setShadowColor_(NSColor.redColor())
    cat2.setShadowOpacity_( 1.0 )
     
    # print [(a, getattr(testLayer,a)()) for a in ['shadowColor', 'shadowOffset', 'shadowOpacity', 'shadowPath', 'shadowRadius'] ]
    #sys.exit()

    # cat2.addSublayer_(cat_h2)           # if a text widget is sub to another text widget is it clipped to that widget?
    # rootLayer.addSublayer_(cat_h2)
    # cat_h2.setForegroundColor_(textColor_h)
    
    

    # 
    # origin=(0+50,0+50)
    # size = (871.0-100, 490.0-100)
    # exampleQCCompositionLayer.setBounds_(  ( origin , size )  )      
    
    # rootLayer.addSublayer_(exampleQCCompositionLayer)
        



    print "view.wantsLayer() is", view.wantsLayer()
    print "view.layer() is", view.layer()
    # view.wantsLayer() is True
    # view.layer() is <QCCompositionLayer: 0x7f9d24400030>



    sublayer = CALayer.layer()                                     # [[CALayer layer] retain]


    sublayer.setContents_( theLakeImage )

    # sublayer = [CALayer layer];
    sublayer.setBackgroundColor_( NSColor.blueColor() )
        # sublayer.backgroundColor = [UIColor blueColor].CGColor;

    sublayer.setShadowOffset_((5.0, 5.0))

    sublayer.setShadowRadius_(4.0)

    sublayer.setShadowColor_(NSColor.blackColor())
    
    sublayer.setShadowOpacity_( 0.8 )

    origin=(220,420)
    size = (300,100)
    sublayer.setFrame_(  ( origin , size )  )      
    

    if True:
        # rootLayer = CALayer.layer()
        rootLayer = exampleQCCompositionLayer
        view.setLayer_(rootLayer)
        view.setWantsLayer_( objc.YES )                                      #     [self setWantsLayer: YES];
    else:
        view.setWantsLayer_( objc.YES )                                      #     [self setWantsLayer: YES];
        rootLayer = view.layer()

    # sublayer.shadowOffset = CGSizeMake(0, 3);
    # sublayer.shadowRadius = 5.0;
    # sublayer.shadowColor = [UIColor blackColor].CGColor;
    # sublayer.shadowOpacity = 0.8;
    # sublayer.frame = CGRectMake(30, 30, 128, 192);
    # [self.view.layer addSublayer:sublayer];
    
    # # theLakeImage is <CGImage 0x7fc3cd0d1910>

    # Because a layer is just a container for managing a bitmap image, you can
    # assign an image directly to the layer’s contents property.
    
    # Assigning an image to the layer is easy and lets you specify the
    # exact image you want to display onscreen.
    # The layer uses the image object you provide directly and
    # does not attempt to create its own copy of that image.
    # This behavior can save memory in cases where your app uses the same image in multiple places.
    
    # print "rootLayer.contents() is", rootLayer.contents()
    # rootLayer.contents() is None


    
    # l.setBackgroundColor_(theCGColor)  # self.viewBkgndColor)     
    
    # still handles buttons ok.  


    # hel = NSButton.alloc().initWithFrame_ (((10.0, 10.0), (80.0, 80.0)))
    # win.contentView().addSubview_ (hel)
    # hel.setBezelStyle_( 4 )
    # hel.setTitle_( 'Hello!' )
    # hel.setTarget_( app.delegate() )
    # hel.setAction_( "sayHello:" )
    # 
    # beep = NSSound.alloc()
    # beep.initWithContentsOfFile_byReference_( '/System/Library/Sounds/Tink.Aiff', 1 )
    # hel.setSound_( beep )
    # 

    # bye = NSButton.alloc().initWithFrame_ (((100.0, 10.0), (80.0, 80.0)))
    # win.contentView().addSubview_ (bye)
    # bye.setBezelStyle_( 4 )
    # bye.setTarget_ (app)
    # bye.setAction_ ('stop:')
    # bye.setEnabled_ ( 1 )
    # bye.setTitle_( 'Goodbye!' )



    # 
    # adios = NSSound.alloc()
    # adios.initWithContentsOfFile_byReference_(  '/System/Library/Sounds/Basso.aiff', 1 )
    # bye.setSound_( adios )
    # 
    # 
    # 
    # tog = NSButton.alloc().initWithFrame_ (((190.0, 10.0), (80.0, 80.0)))
    # win.contentView().addSubview_ (tog)
    # tog.setBezelStyle_( 4 )
    # tog.setTarget_ ( objc.nil )
    # # tog.setAction_ ('ztoggleFullScreen:')
    # tog.setAction_ ('toggleFullScreen:')
    # tog.setEnabled_ ( 1 )
    # tog.setTitle_( 'toggleFullScreen:' )

    # If an application supports fullscreen, it should add a menu item to the View menu with toggleFullScreen: as the action, and nil as the target.

 
 
    w = app.windows()    
    print "app.windows (before display() are:", len(w), w

    # win.display()
    # win.orderFrontRegardless()          ## but this one does
    
    win.makeKeyAndOrderFront_(objc.NULL)
    # z = win.isMainWindow()
    # print "win.isMainWindow is ", z
    # win.makeKeyWindow()
    # z = win.isKeyWindow()
    # print "win.isKeyWindow is ", z

    w = app.windows()    
    print "app.windows are:", len(w), w
    
    q = app.currentEvent()
    print "app.currentEvent is: " , q

    AppHelper.runEventLoop()


if __name__ == '__main__' : main()


# Based on the original PyObjC interface example "Hello World" by Steve Majewski. 

#   ("ObjC becomes Python")

### NOTE:  This is no longer the recommended way to build applications
### using the pyobjc bridge under with OS X.  In particular, applications
### work much better if they are constructed in a proper app wrapper.
