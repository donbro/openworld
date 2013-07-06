#!/Users/donb/projects/VENV/pyobjc25/bin/python
# encoding: utf-8
"""
OpenView.py

Created by donb on 2013-07-03.
Copyright (c) 2013 __MyCompanyName__. All rights reserved.
"""

import objc


from Foundation import NSMakePoint, NSPointInRect, NSMakeRect, NSEqualPoints
from AppKit import NSColor, NSCursor, NSView, CALayer, NSApp, NSTouchPhaseTouching

from printB import printB, print_setters
from createLayer import getQCCompLayer, createLayer, createTextLayer

from Quartz import CGColorCreateGenericRGB, CIFilter, CGColorCreateGenericGray

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
        
    # also some layer subclass experimentatoin because this is the only layer subclsss I have a the moment
    
    
    def layoutSublayersOfLayer_(self, layer):
        printB("OpenView layoutSublayersOfLayer",  layer )
    


class OpenView(NSView):   # my OpenView was LTView in LightTable
    """."""
    _locationDefault = NSMakePoint(0.0, 0.0)
    _itemColorDefault = NSColor.redColor()
    _backgroundColorDefault = NSColor.whiteColor()

    # def awakeFromNib(self):       # no nib!
    
    # def __init__(self):
    #     CALayer *overlayLayer;
        
    def initialize_(self, b):
        printB("OpenView received initialize!",  self )
        # is this ever called in our PyObjC world?
        
    # [self exposeBinding:kLTViewSlides];
    # [self exposeBinding:kLTViewSelectionIndexes];

    

    def initWithFrame_(self, frame):

        print "initWithFrame",  frame

        self._location = self._locationDefault
        self._itemColor = self._itemColorDefault
        self._backgroundColor = self._backgroundColorDefault

        
        self.dragging = None
        
        result = super(OpenView, self).initWithFrame_(frame)

        # self.setBounds_( (0,0) , self.window().frame.size )

        printB("initWithFrame",  self ,all_names=True)
        printB("view.initWithFrame", self, add=['frame','bounds'])

        print "result of super(OpenView, self).initWithFrame_(frame) is", result
        if result is None:
            return result

        # // setup the CALayer for the overall full-screen view

        #
        #   backing layer
        #
        
        backingLayer = getQCCompLayer()
        frame = self.frame()
        backingLayer.setBounds_( ((0, 0), (frame.size.width, frame.size.height)) )
        
        # backingLayer.setFrame_(  view.frame() )      
        # backingLayer.frame = NSRectToCGRect(frame);
        # backingLayer.backgroundColor = CGColorCreateGenericRGB(1, 1, 1, 1.0);
        backingLayer.setOpaque_(objc.YES)

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
        print_setters(self, add=['bounds', 'frame'])

        printB("rootLayer", rootLayer, add=['bounds'])


        #
        #   overlay Layer
        #
        #  The overlay layer is used to draw any drag handles, so that they are always on top of all slides. 
        #  We must take care to make sure this layer is always the last one.
        #
        
        overlayLayer = MyOverLayer.layer() # (_LTOverlayLayer was MyOverLayer)
        overlayLayer.setFrame_( backingLayer.frame() ) # view.frame() )      
        overlayLayer.setOpaque_( objc.NO )

        borderWidth = 4.0
        overlayLayer.setBorderWidth_(borderWidth)
        # borderColor = CGColorCreateGenericGray(.4, 0.75)
        borderColor = CGColorCreateGenericRGB(1, 0.5, 0.2, 0.8);
        overlayLayer.setBorderColor_( borderColor )         
        
        zPosition = 20
        
        overlayLayer.setZPosition_(zPosition)

        #   zPosition
        #
        # Increasing zPosition moves the layer towards the front
        # Decreasing it moves it away and towards the back
        #

        # We want to be the delegate so we can do the drag handle drawing        
        overlayLayer.setDelegate_(self)
        # overlayLayer.backgroundColor = CGColorCreateGenericRGB(0, 0, 0, 0.0);
        # overlayLayer.autoresizingMask = kCALayerWidthSizable | kCALayerHeightSizable;

        printB("overlayLayer", overlayLayer, all_names=True)
        printB("overlayLayer", overlayLayer, only = ['borderColor', 'borderWidth', 'bounds'] )

        backingLayer.addSublayer_(overlayLayer)

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

        layerDict = {
            'origin' : (420,120),
            'size'  :  (120,120),
            'zPosition'  :  12,
            'image_path'  :  "/Users/donb/projects/openworld/gray button 96px.psd",
            'cornerRadius'  :  16,
            'borderWidth'  :  1.0,
        }
        # 
        # testLayer = createLayer(**layerDict)
        # rootLayer.addSublayer_(testLayer)
        # 
        
        app = NSApp()
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

    def touchesBeganWithEvent_(self, event):
        """Informs the receiver that new set of touches has been recognized."""
        printB("touchesBeganWithEvent_",  event  ,only=general_event_info)
        # touchesMatchingPhase:inView:
        touches = event.touchesMatchingPhase_inView_( NSTouchPhaseTouching ,self)
        
        print "touches is", len(touches), touches

        
    # [_inputTrackers makeObjectsPerformSelector:_cmd withObject:event];


    # NSSet *touches = [event touchesMatchingPhase:NSTouchPhaseTouching inView:self.view];
    # 
    # if (touches.count == 2) {
    #     self.initialPoint = [self.view convertPointFromBase:[event locationInWindow]];
    #     NSArray *array = [touches allObjects];
    #     _initialTouches[0] = [[array objectAtIndex:0] retain];
    #     _initialTouches[1] = [[array objectAtIndex:1] retain];
    #     
    #     _currentTouches[0] = [_initialTouches[0] retain];
    #     _currentTouches[1] = [_initialTouches[1] retain];
    # } else if (touches.count > 2) {
    #     // More than 2 touches. Only track 2.
    #     if (self.isTracking) {
    #         [self cancelTracking];
    #     } else {
    #         [self releaseTouches];
    #     }
    # 
    # }

    # *lots* of these.  have to summarize/compute features of all of them.
    # def touchesMovedWithEvent_(self, event):
    #     printB("touchesMovedWithEvent_",  event  ,only=general_event_info)
    # # [_inputTrackers makeObjectsPerformSelector:_cmd withObject:event];


    def touchesEndedWithEvent_(self, event):
        printB("touchesEndedWithEvent_",  event  ,only=general_event_info)
    # [_inputTrackers makeObjectsPerformSelector:_cmd withObject:event];


    def touchesCancelledWithEvent_(self, event):
        printB("touchesCancelledWithEvent_",  event  ,only=general_event_info)
    # [_inputTrackers makeObjectsPerformSelector:_cmd withObject:event];


    def rotateWithEvent_(self, event):
        printB("rotateWithEvent_",  event  ,only=general_event_info)

    def magnifyWithEvent_(self, event):
        printB("magnifyWithEvent_",  event  ,only=general_event_info)

    def swipeWithEvent_(self, event):
        printB("swipeWithEvent_",  event  ,only=general_event_info)



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

    # @objc.IBAction      # haha only kidding!
    def setItemPropertiesToDefault_(self, sender):
        """."""
        self.setLocation_(self._locationDefault)
        self.setItemColor_(self._itemColorDefault)
        self.setBackgroundColor_(self._backgroundColorDefault)

    def keyDown_(self, event):
        # print "keydown, event is %r" % event
        printB("keyDown",  event, only = general_event_info+key_event_info)

        handled = False
        characters = event.charactersIgnoringModifiers()
        
        if characters == u"r": # .isEqual_('r'):
            handled = True
            self.setItemPropertiesToDefault_(self)
        if handled is False:
            q = super(OpenView, self).keyDown_(event)  # beeps if not handled/forwarded to super (who doesn't know what to do?)
            print "keydown: q is", q

    def drawRect_(self, rect):
        printB("drawRect",  rect )
        
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
        return self._backgroundColor

    def setItemColor_(self, aColor):
        """."""
        printB("setItemColor",  self)
        
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
