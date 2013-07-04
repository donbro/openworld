#!/Users/donb/projects/VENV/pyobjc25/bin/python
# encoding: utf-8
"""
OpenView.py

Created by donb on 2013-07-03.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

import objc

from AppKit import NSColor, NSCursor
from Foundation import NSMakePoint, NSPointInRect, NSMakeRect, NSEqualPoints
from AppKit import NSView, CALayer

from printB import printB, print_setters
from createLayer import getQCCompLayer

# General Event Information

general_event_info = [ 'context'          ,               
                        'locationInWindow'            ,    
                        'modifierFlags'                 ,  
                        'timestamp'                       ,
                        'type'                            ,
                        'window'                          ,
                        'CGEvent',
                        'windowNumber'                    
                        ]
mouse_event_info =   [
            'pressedMouseButtons',
            'doubleClickInterval',
            'mouseLocation',
            'buttonNumber',
            'clickCount',
            'pressure'  
            ]
            
key_event_info = [
    'modifierFlags',
    'keyRepeatDelay',
    'keyRepeatInterval',
    'characters',
    'charactersIgnoringModifiers',
    'isARepeat',
    'keyCode'
]

# // The MyOverLayer class is used so that our overlay layer with the drag handles is not included in hit testing. 
# Otherwise, hit testing would always return the overlay layer since it is the top layer and fills the entire view. 
# It is implemented it in this file because it is a private helper class of LTView.
# @interface MyOverLayer : CALayer
# @end
# 

class MyOverLayer(CALayer):         # @implementation MyOverLayer

    def containsPoint_(self, p):
        return objc.NO    # just NO, always NO, not here , this layer never contains any points


class OpenView(NSView):
    """."""
    _locationDefault = NSMakePoint(0.0, 0.0)
    _itemColorDefault = NSColor.redColor()
    _backgroundColorDefault = NSColor.whiteColor()

    # def awakeFromNib(self):       # no nib!
    
    # def __init__(self):
    #     CALayer *overlayLayer;
        
    def initialize_(self, b):
        printB("OpenView received initialize",  self )
        # is this ever called in our PyObjC world?
        
    # [self exposeBinding:kLTViewSlides];
    # [self exposeBinding:kLTViewSelectionIndexes];

    

    def initWithFrame_(self, frame):

        printB("initWithFrame (frame)",  frame )
        self.dragging = None
        
        result = super(OpenView, self).initWithFrame_(frame)

        print "result is", result
        if result is None:
            return result

        self._location = self._locationDefault
        self._itemColor = self._itemColorDefault
        # self._backgroundColor = self._backgroundColorDefault

        # self.setLocation_(self._locationDefault)
        # self.setItemColor_(self._itemColorDefault)
        # self.setBackgroundColor_(self._backgroundColorDefault)

        # // setup the CALayer for the overall full-screen view

        #
        #   backing layer
        #
        
        backingLayer = getQCCompLayer()
        # backingLayer.setFrame_( win_frame ) # view.frame() )      
        # backingLayer.frame = NSRectToCGRect(frame);
        # backingLayer.bounds = CGRectMake(0, 0, frame.size.width, frame.size.height);
        # backingLayer.backgroundColor = CGColorCreateGenericRGB(1, 1, 1, 1.0);
        # backingLayer.opaque = YES;

        printB("QCLayer", backingLayer)
        # print_setters(backingLayer)
    
        if True:
            # rootLayer = CALayer.layer()
            self.setLayer_(backingLayer)
            self.setWantsLayer_( objc.YES )
            rootLayer = backingLayer            
        else:
            self.setWantsLayer_( objc.YES )
            rootLayer = self.layer()

        # printB("initWithFrame (super)",  super(OpenView, self) )
        # printB("initWithFrame (view)",  self )        


        printB("View",  self ) # frame = bounds for origin (0,0)?
        print_setters(self)

        printB("rootLayer", rootLayer)


        #
        #   overlay Layer
        #
        #  The overlay layer is used to draw any drag handles, so that they are always on top of all slides. 
        #  We must take care to make sure this layer is always the last one.
        #
        
        overlayLayer = MyOverLayer.layer() # (_LTOverlayLayer was MyOverLayer)
        overlayLayer.setFrame_( backingLayer.frame() ) # view.frame() )      
        overlayLayer.setOpaque_( objc.NO )

        # We want to be the delegate so we can do the drag handle drawing        
        overlayLayer.setDelegate_(self)
        # overlayLayer.backgroundColor = CGColorCreateGenericRGB(0, 0, 0, 0.0);
        # overlayLayer.autoresizingMask = kCALayerWidthSizable | kCALayerHeightSizable;



        backingLayer.addSublayer_(overlayLayer)

        # // init ivars
        # _slides = [[NSMutableArray array] retain];
        # self.selectionIndexes = [NSIndexSet indexSet];

        # // init the input trackers
        # [self _initTrackers];

        # // register for dragging
        # [self registerForDraggedTypes:[NSArray arrayWithObject:(NSString *)kUTTypeFileURL]];

        # // we want touch events
        self.setAcceptsTouchEvents_(objc.YES)
     
    
        return result

    def drawRect_(self, rect):
        """."""
        NSColor.whiteColor().set()
        NSBezierPath.fillRect_(rect)
        self.itemColor().set()
        NSBezierPath.fillRect_(self.calculatedItemBounds())

    def isOpaque(self):
        """."""
        # return (self.backgroundColor().alphaComponent() >= 1.0)

    def offsetLocationByX_andY_(self, x, y):
        """."""
        self.setNeedsDisplayInRect_(self.calculatedItemBounds())
        if self.isFlipped():
            invertDeltaY = -1
        else:
            invertDeltaY = 1
        self.location().x = self.location().x + x
        self.location().y = self.location().y + y * invertDeltaY
        self.setNeedsDisplayInRect_(self.calculatedItemBounds())

    def mouseDown_(self, event):

        printB("mouseDown",  event  ,only=mouse_event_info+general_event_info)

        clickLocation = self.convertPoint_fromView_(event.locationInWindow(),
                                                    None)
        itemHit = self.isPointInItem_(clickLocation)
        if itemHit:
            self.dragging = True
            self.lastDragLocation = clickLocation
            NSCursor.closedHandCursor().push()


    def mouseDragged_(self, event):
        """."""
        
        x = [  'eventNumber',
                'deltaX',
                'deltaY' 
                ]

        printB("mouseDragged",  event, only = mouse_event_info+general_event_info+x)
        if self.dragging:
            newDragLocation = self.convertPoint_fromView_(
                event.locationInWindow(),
                None
            )
            self.offsetLocationByX_andY_(
                newDragLocation.x - self.lastDragLocation.x,
                newDragLocation.y - self.lastDragLocation.y
            )
            self.lastDragLocation = newDragLocation
            self.autoscroll_(event)

    def mouseUp_(self, event):
        """."""
        self.dragging = False
        # NSCursor has both an instance and a class method w/ the name 'pop'
        NSCursor.pyobjc_classMethods.pop()
        self.window().invalidateCursorRectsForView_(self)

    def acceptsFirstResponder(self):
        """."""
        return True

    @objc.IBAction      # haha only kidding!
    def setItemPropertiesToDefault_(self, sender):
        """."""
        self.setLocation_(self._locationDefault)
        self.setItemColor_(self._itemColorDefault)
        self.setBackgroundColor_(self._backgroundColorDefault)

    def keyDown_(self, event):
        print "keydown, event is %r" % event
        printB("keyDown",  event, only = general_event_info+key_event_info)

        handled = False
        characters = event.charactersIgnoringModifiers()
        
        if characters.isEqual_('r'):
            handled = True
            self.setItemPropertiesToDefault_(self)
        if handled is False:
            q = super(OpenView, self).keyDown_(event)  # beeps if not handled/forwarded to super (who doesn't know what to do?)
            print "keydown: q is", q
            
    def setLocation_(self, point):
        """."""
        if not NSEqualPoints(point, self.location()):
            self.setNeedsDisplayInRect_(self.calculatedItemBounds())
            self._location = point
            self.setNeedsDisplayInRect_(self.calculatedItemBounds())
            self.window().invalidateCursorRectsForView_(self)

    def location(self):
        """."""
        return self._location

    def setBackgroundColor_(self, aColor):
        """."""
        if not self.backgroundColor().isEqual_(aColor):
            self._backgroundColor = aColor
            self.setNeedsDisplayInRect_(self.calculatedItemBounds())

    def backgroundColor(self):
        """."""
        # return self._backgroundColor

    def setItemColor_(self, aColor):
        """."""
        if not self.itemColor().isEqual_(aColor):
            self._itemColor = aColor
            self.setNeedsDisplayInRect_(self.calculatedItemBounds())

    def itemColor(self):
        """."""
        return self._itemColor

    def calculatedItemBounds(self):
        """."""
        return NSMakeRect(self.location().x, self.location().y,
                          60.0, 20.0)

    def isPointInItem_(self, testPoint):
        """."""
        itemHit = NSPointInRect(testPoint, self.calculatedItemBounds())
        if itemHit:
            pass
        return itemHit



if __name__ == '__main__':
    pass
