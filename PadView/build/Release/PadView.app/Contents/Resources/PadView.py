# -*- coding: utf-8 -*-

#
#  PadView.py
#  PadView
#
#  Created by donb on 2010.05.06.
#  Copyright (c) 2010 __MyCompanyName__. All rights reserved.
#

import sys

from objc import YES, NO, IBAction, IBOutlet
from Foundation import *
from AppKit import *

# some routines to describe the geometry, etc., of the layers.

def PointToString(p):
    if p.x == int(p.x):
        pxs = "%.f" % p.x
    else:
        pxs = "%.2f" % p.x
        
    if p.y == int(p.y):
        pys = "%.f" % p.y
    else:
        pys = "%.2f" % p.y
        
    return "{%s, %s}" % (  pxs, pys )  
    #return "{%.2f, %.2f}" % (  p.x,   p.y, )  # extend decimal to quarter points for Points, eg x=395.5 y=189.25

def RectToString(rect):
    return "(%.0f,%.0f,%.0f,%.0f)" % (  rect.origin.x,   rect.origin.y,   rect.size.width,   rect.size.height )

def RectToString2(rect):
    return "(origin: (x=%.0f, y=%.0f), size: (width=%.0f, height=%.0f)" % (  rect.origin.x,   rect.origin.y,   rect.size.width,   rect.size.height )

    # l.anchorPoint() seems to always return {0,0} ?
    #print l.valueForKeyPath_("anchorPoint")
    # valueForKeyPath_ returns 'NSConcreteValue' object which has no attribute 'x'    
    # .rectValue(), pointValue()


    #   Wrapping Conventions 
    #   When using the key-value coding methods to access properties whose values are not 
    #   objects the standard key-value coding wrapping conventions support, 
    #   the following wrapping conventions are used: 
    #   Class               C Type 	
    #   NSValue 			CGPoint 	
    #   NSValue 			CGSize 	
    #   NSValue 			CGRect 
    #   NSAffineTransform 	CGAffineTransform 
    #   NSValue 			CATransform3D 

# create a python class that wraps a layer and provides pythonic accessors?  (still not enough for a subclass?)

def LayerToString(l, i=None):
    if i == None:
            s =  "layer (%s)" %  ( l.name() )
    else:
            s =  "layer[%d](%s)" %  ( i,  l.name() )

    if l.isKindOfClass_(CATextLayer): 
            return "%-16s '%s' f=%s, b=%s, p=%s, anchorPoint=%s, superlayer=%r" % \
                    ( s , l.string() , RectToString(l.frame()), RectToString(l.bounds()), PointToString(l.position()) , 
                                                                                PointToString( l.valueForKeyPath_("anchorPoint").pointValue() ) , l.superlayer().name())    
    else:
            return "%-16s frame=%s, bounds=%s, position=%s, anchorPoint=%s, superlayer=%r" % \
                    ( s, RectToString(l.frame()), RectToString(l.bounds()), PointToString(l.position()) , 
                                                                                PointToString( l.valueForKeyPath_("anchorPoint").pointValue() ) , l.superlayer().name()  )    
        
#            return "sublayer %d %r, %r, frame=%s, bounds=%s, position=%s, anchorPoint=%r" % \
#                 ( i, l, l.name(), RectToString(l.frame()), RectToString(l.bounds()), PointToString(l.position()) , l.valueForKeyPath_("anchorPoint")  )

from PVLayout import PVLayoutGrid

class PVLayout(NSObject):

    def init(self):
        self = super(PVLayout, self).init()
        if self:
            NSLog("class PVLayout received init")
            pass
        return self

        
    def layoutSublayersOfLayer_(self, layer):
        """ Method is called when the sublayers of the layer may need rearranging. 
            Typically called when a sublayer has changed its size. 
            Receiver (ie, this PVLayout object) is responsible for changing 
                the frame of each sublayer that requires layout.
        """
    
        from Quartz import CATransaction, kCATransactionDisableActions

        newBounds = layer.bounds();
        
        n =  len(layer.sublayers()) 
        
#        NSLog( "class PVLayout: layoutSublayersOfLayer %@ bounds=%@, %d sublayers", layer, RectToString(newBounds), n )        
        NSLog( "layout of layer %@ bounds=%@, %d sublayers", layer.name(), RectToString(newBounds), n )        

        self.layoutGrid = PVLayoutGrid(n)
        NSLog(  "PVLayout is: %r"  % ( self.layoutGrid , ) ) # PVLayout is: n=8, g=3, g2=9
        NSLog(  "i   g2ni gn0  gn0p gn5 (  x  ,  y  ) "  )
#        for i in range(self.layoutGrid.n):  
#            NSLog(  self.layoutGrid.str(i)  )

#        height = (newBounds.size.height-2*10.0)/n     # height of each is less by portion of separations of 10.0 at top and bottom
        height = (newBounds.size.height-(self.layoutGrid.g()+1)*10.0)/(self.layoutGrid.g()+1) # height/width of grid
        width = (newBounds.size.width-(self.layoutGrid.g()+1)*10.0)/(self.layoutGrid.g()+1 )# height/width of grid  # separate width from height, create a layout  based on aspect ration of window?
        
#        z = CATransaction.getValue_(<#value#>)   value_forKey_     value_forKey_(kCATransactionDisableActions)

        CATransaction.setValue_forKey_( YES , kCATransactionDisableActions )

        for i, l in enumerate(layer.sublayers()):

            NSLog(  self.layoutGrid.str(i)  )
        
            # I'm setting the *frame*. So whatever's going on inside the layer I don't care about, (like bounds and position and anchorPoint) :-)
        
            originalFrame = l.frame();  # bounds is *its* rectangle, frame is the *superlayer*'s rectangle.
            originalBounds = l.bounds()
            
            if l.isKindOfClass_(CATextLayer):  
                # no resizing, just move the origin.
                origin = (10,10 + i * height ) 
                size = ( originalBounds.size.width , originalBounds.size.height ) # really just want originalBounds.size.                                   
                l.setFrame_(  ( origin , size )  )                     
            else:
                #origin = (10,10 + i * height )                                  
                origin = (self.layoutGrid.xn(i) * newBounds.size.width , self.layoutGrid.yn(i) * newBounds.size.height )                                  
                #size = ( newBounds.size.width-2*10.0, height ) 
                size = ( width , height ) 
                l.setFrame_(  ( origin , size )  )                      # I'm setting the *frame*. So whatever's going on inside the layer I don't care about :-)

            NSLog( LayerToString( l , i ) )

        CATransaction.setValue_forKey_( NO , kCATransactionDisableActions)     # :[NSNumber numberWithBool:YES] :kCATransactionDisableActions];

    #   - (void)layoutSublayersOfLayer:(CALayer *)layer {
    #       id oldValue = [[CATransaction valueForKey:  forKey:kCATransactionDisableActions
    #       [CATransaction setValue:[NSNumber numberWithBool:YES] forKey:kCATransactionDisableActions];
    #       [super layoutSublayersOfLayer:layer];
    #       [CATransaction setValue:[NSNumber numberWithBool:NO] forKey:kCATransactionDisableActions];


    #        
    #preferredSizeOfLayer:
    #Returns the preferred size of the specified layer in its coordinate system.
    #
    #- (CGSize)preferredSizeOfLayer:(CALayer *)layer
    #
    #Parameters
    #layer
    #The layer that requires layout.
    #
    #Return Value
    #The preferred size of the layer in the coordinate space of layer.
    #
    #Discussion
    #This method is called when the preferred size of the specified layer may have changed. The receiver is responsible for recomputing the preferred size and returning it. If this method is not implemented the preferred size is assumed to be the size of the bounds of layer.

import math

def DEGREES_TO_RADIANS(degrees):
    return degrees * math.pi / 180.0

    
class PadView(NSView):

    thisPadViewsController = objc.IBOutlet()

    def initWithFrame_(self, frame):                

        self = super(PadView, self).initWithFrame_(frame)

        if self == None: return None
    
        NSLog("class PadView received initWithFrame")
        
        # 
        #   have to wait until here to import Quartz or else we get a '_CGSDefaultConnection() is NULL' error?
        #   could do it in PVAppController?  Will there be enough windowing system up at that point to Quartz to connect to?
        #

        NSLog("initWithFrame: begin import Quartz")     
        
        from Quartz import CGColorCreateGenericRGB,  CGColorCreateGenericGray, kCGColorBlack, kCGColorWhite
        NSLog("initWithFrame: end import Quartz")        
        
        
        #   The alpha value is the graphics state parameterthatQuartzusestodeterminehowtocompositenewly-painted 
        #   objects to the existing page. At full intensity, newly-paintedobjectsareopaque. Atzerointensity, 
        #   newly-paintedobjectsareinvisible.
        
        #   Quartz performs alpha blending by 
        #   combining thecomponentsofthesource color with the components of the destination color using the 
        #   formula: 
        #       destination = (alpha * source) + (1 - alpha) * destination 
        #   [Quartz 2D Programming Guide (drawingwithquartz2d), page 73]
        

        #self.textColor      = kCGColorBlack
        self.textColor      = CGColorCreateGenericGray(0.1, 1.0)                # dark charcoal, almost black
        self.textHighlight   = CGColorCreateGenericRGB(1.0, 0.8, 1.0, 0.9)
        #self.textHighlight   = CGColorCreateGenericRGB(0.1, 0.8, 0.1, 0.9)
        #self.textColor      = CGColorCreateGenericRGB(0.1, 0.15, 0.2, 1.0) 
        #self.textBkgndColor = CGColorCreateGenericRGB(0.8, 0.8, 0.8, 1.0);  # light gray
        self.textBkgndColor = CGColorCreateGenericRGB(0.8, 0.8, 0.8, 0.4)   # alpha=0.5 means more transparent.
        
        self.borderColor = CGColorCreateGenericGray(0.50, 0.75)
        #self.borderColor = CGColorCreateGenericGray(0.75, 0.75)
        
        self.viewBkgndColor = CGColorCreateGenericRGB(0.5, 1.0, 0.75, 0.5)   # light green

        self.font           = NSFont.fontWithName_size_("Skia",14.0)

        NSLog("initWithFrame: font is %r" % (self.font, ) )

        #
        #   Create background checkerboard color (pattern)
        #

        from CGImageUtils import CreatePatternColorFromPath, LoadImageFromPath
        
        #   application global value?
        
        path = "/Users/donb/projects/PadView/UI/checkerboard bkgnd pattern cell 75px.png"        
        
        self.checkerboard = CreatePatternColorFromPath( path )
                
        NSLog("initWithFrame: self.checkerboard is %r" % (self.checkerboard, ) )
        

        #
        #   Load some images
        #

        path = "/Library/Desktop Pictures/Small Ripples graphite.png"
        
        self.ripples = LoadImageFromPath( path )

        NSLog("initWithFrame: self.ripples is %r" % (self.ripples, ) )
        
        
        path = "/Users/donb/projects/PadView/UI/csv12 grey1 770px.psd" 
        
        self.csv12_grey1 = LoadImageFromPath( path )

        NSLog("initWithFrame: self.csv12_grey1 is %@" , self.csv12_grey1 )
        
        path = "/Users/donb/projects/PadView/UI/gray button 96px.psd" 
        
        self.gray_button_96px = LoadImageFromPath( path )

        NSLog("initWithFrame: self.gray_button_96px is %@" , self.gray_button_96px )
        
        
        
        #
        #   Create ripples background color pattern
        #

        self.ripplesPattern = CreatePatternColorFromPath( path )
                
        NSLog("initWithFrame: self.ripplesPattern is %r" % (self.ripplesPattern, ) )
        


        self.selectList = []            # list of all layers currently selected
        

        #NSLog("initWithFrame: thisPadViewsController is %r" % (self.thisPadViewsController, ) ) # thisPadViewsController is None (until after awake from NIB) .
        
        return self

    #
    #   AppKit does suppress the default animations during live resize:
    #
    #   > I have a layer-backed view that resizes to fit the available space
    #   > in the window. During live window resizes, I'd like the layers to
    #   > resize with no animation.
    #   
    #   For the "pure" layer-backed view case, where you're just setting
    #   wantsLayer=YES on various views and leaving it to AppKit automatically
    #   create and manage the backing layers, AppKit does automatically
    #   suppress the default animations that would otherwise occur for those
    #   layers during window live resize.
    #
    #   [http://www.cocoabuilder.com/archive/cocoa/198175-core-animation-layout-behavior-during-live-window-resize.html]

    def awakeFromNib(self):

        NSLog( "class PadView received awakeFromNib: PadView.frame=%s, PadView.bounds=%s" % ( RectToString( self.frame() ) , RectToString( self.bounds() ) ) )
        NSLog( "awakeFromNib: thisPadViewsController is %r" % (self.thisPadViewsController, ) ) #  thisPadViewsController is <PVController: 0x1f377e0>
#        self.setBounds_( ( (0,0), (247,469) ) )
#        self.setFrame_( ( (0,0), (247,469) ) )
        
        
        
        #
        #   here we programmatically create our own CALayer rootLayer 
        #   rather than relying on the NIB flag for "wantsLayer"
        #
        #   This way we *own* the layer more completely?
        #   We can use the generic CALayer creation routines even for the root layer?
        #
        #
        #   If we use layer backing as turned on in MainMenu.xib for the view(s) 
        #      (rather than programatically via -setWantsLayer.) then we have:
        
        # better be True! wantsLayer is set in NIB, better practice to set it here?
        
        # (donb 5/15/2010: removed setting in NIB.  *create* and set the layer here and it will be a CALayer not a NSViewBackingLayer?

        
        
        CreateOurOwnRootLayer = True # False
        
        if CreateOurOwnRootLayer:
        
            rootLayer = CALayer.layer()                                     # [[CALayer layer] retain]
            
            rootLayer.setBounds_( self.bounds() )                           # NSRectToCGRect(self.bounds)

            self.setLayer_(rootLayer)                                       #  self.layer() is: <CALayer: 0x1d3c240>
            
            self.setWantsLayer_( YES )                                      #     [self setWantsLayer: YES];
            
        else:
        
            self.setWantsLayer_( YES )                                      # self.wantsLayer() is True

            rootLayer = self.layer()    # self.layer() is: _NSViewBackingLayer(0x1d3cc40) p={0, 0} b=(0,0,791,498) superlayer=0x0

     
        NSLog( "rootLayer is: %@", rootLayer );        
        
            
        rootLayer.setName_( "rootLayer" )                                   #     rootLayer.name = @"container";


        #   You specify the content of a CALayer instance in one of the following ways:
        #
        #   • Explicitly set the contents property of a layer instance using a CGImageRef that contains the content image.
        #   • Specify a delegate that provides, or draws, the content.
        #   • Subclass CALayer and override one of the display methods.
        #
        #   [Core Animation Programming Guide (2010).pdf, page 33]

        rootLayer.setContents_( self.csv12_grey1 )

#        rootLayer.setBackgroundColor_( self.checkerboard )
        
#        NSLog( "backgroundColor (after) is %r" % ( rootLayer.backgroundColor() ,) )

        #rootLayer.setCornerRadius_( 25.0 )      

    
                    
        
        
 
        #
        #   Get Data
        #
        
        self.data = self.thisPadViewsController.data  # really.  how about sending controller a *message* and get back data!

        NSLog("PadView: Data is (%d) %r" %  ( len(self.data), self.data ) )  # Use %r, not %@, for a Python structure.


        
        #
        #   Create the layers.  (Move this to CGUtils?)
        #
        
        self.CreateTheLayers()

        
        #   
        #   Create an object PVLayout to be a proxy layout manager for theLayer.  And all sublayers???
        #

        
        rootLayer.setLayoutManager_( PVLayout.alloc().init() )  

        NSLog( "rootLayer.layoutManager is: %@" , rootLayer.layoutManager() )
        

    # end def awakeFromNib(self):
        

    def CreateTheLayers(self):

        
        from Quartz import CATransform3DIdentity, CAConstraint, kCAConstraintWidth, kCAConstraintMidX, kCAConstraintMidY, CAConstraintLayoutManager,\
                                kCAConstraintMinY

        rootLayer = self.layer()
        
        for i, node in enumerate( self.data ):  # iterating over dictionary gives keys

            r = self.data[node]

            # special first two for testing
            if False and i == 0:
                l = self.CreateCALayer(name=node, borderWidth=1.0, zPosition = i ) # "layerA", borderWidth=1.0)
                l.setTransform_(CATransform3DIdentity)
#                l.setBackgroundColor_(theCGColor)  # self.viewBkgndColor) 

                transform_rotation = DEGREES_TO_RADIANS(135) # 180 * M_PI # DegreesToRadians(180) # M_PI
                l.setValue_forKeyPath_(transform_rotation, "transform.rotation.x" ) 
                self.l1 = l

                l2 = self.CreateCATLayer( r['node_name'], name=node, isWrapped = False, zPosition = i ) 
                l.addSublayer_(l2)

            elif False and i == 1:

                l = self.CreateCALayer(name=node, borderWidth=1.0, zPosition = i ) # "layerA", borderWidth=1.0)
                l.setBorderWidth_(0.0)
                #l.setContents_( self.ripples )
                l.setBackgroundColor_( self.ripplesPattern )                
                l.setMasksToBounds_( True )
#                NSLog( "l.contents is %r" % (l.contents(),) ) # contents are, eg, <CGImage 0x1d39b20>
        
            else:
            
                l = self.CreateCALayer(name=node, borderWidth=1.0, zPosition = i )

                l.setMasksToBounds_( True )         # for some styles we want to be able to write outside the box.


                l.setContents_( self.gray_button_96px )


                l.setLayoutManager_( CAConstraintLayoutManager.layoutManager() )  # do we have to explicitly set the constraint layout manger?  yes? seems so...
                                                        # but we do get the text auto-sizing...


                # Note:  When a CATextLayer instance is positioned using the CAConstraintLayoutManager
                # the bounds of the layer is resized to fit the text content. 
                # [CATextLayer Class Reference, page 6]


                l2 = self.CreateCATLayer( r['node_name'], name=node+'text', isWrapped = True, zPosition = 10 ) 

#                l.addSublayer_(l2)  # do we *have* to add to superlayer before creating constraints?  No.

                ## This constraint sets the *width* to 20 points less than the width of the *superlayer*.
                #c = CAConstraint.constraintWithAttribute_relativeTo_attribute_offset_( kCAConstraintWidth, "superlayer", kCAConstraintWidth, -20.0)
                #c = CAConstraint.constraintWithAttribute_relativeTo_attribute_offset_( kCAConstraintWidth, "superlayer", kCAConstraintWidth, 0.0)
                c = CAConstraint.constraintWithAttribute_relativeTo_attribute_( kCAConstraintWidth, "superlayer", kCAConstraintWidth )
                l2.addConstraint_( c ) 

                # This constraint sets the *horizontal center* to   the *horizontal center* of the *superlayer*.
                c = CAConstraint.constraintWithAttribute_relativeTo_attribute_(kCAConstraintMidX, "superlayer", kCAConstraintMidX)
                l2.addConstraint_( c ) 
                
                c = CAConstraint.constraintWithAttribute_relativeTo_attribute_(kCAConstraintMidY, "superlayer", kCAConstraintMidY)
                l2.addConstraint_( c ) 

                l.addSublayer_(l2)  # do we *have* to add to superlayer before creating constraints?  No!  before adding constraints?  maybe?
                
                l3 = self.CreateCATLayer( r['node_name'], name="l3", isWrapped = True, textColor=self.textHighlight, zPosition = 0 ) # behind l2

                c = CAConstraint.constraintWithAttribute_relativeTo_attribute_( kCAConstraintWidth, "superlayer", kCAConstraintWidth )
                l3.addConstraint_( c ) 

                # This constraint sets the *horizontal center* to   the *horizontal center* of the *superlayer*.
                c = CAConstraint.constraintWithAttribute_relativeTo_attribute_(kCAConstraintMidX, "superlayer", kCAConstraintMidX)
                l3.addConstraint_( c ) 

                #   Sibling layersarereferencedbyname,usingthenamepropertyofeachlayer.Thespecial name superlayer 
                #   isused to refer to the layer's superlayer. 

                c = CAConstraint.constraintWithAttribute_relativeTo_attribute_offset_(kCAConstraintMinY, node+'text', kCAConstraintMinY, -1.0)
                l3.addConstraint_( c ) 

                l.addSublayer_(l3)

        
             
            rootLayer.addSublayer_(l)
            NSLog( "Creating layers: " + LayerToString( l , i ) )

        # end for i, node in enumerate( self.data ):

 
 
    def mouseDown_(self, event):
        """class PadView received mouseDown_"""

        eventLocation = event.locationInWindow()                # [theEvent locationInWindow] 

        self.target_point = self.convertPoint_fromView_(eventLocation, None)
#        NSLog( "mouseDown: self.target_point is %r" % (self.target_point,) )

        # SelectableLayer *hitLayer = (SelectableLayer *)[self.layer hitTest: NSPointToCGPoint(convertedPoint)];
        
        hitLayer = self.layer().hitTest_(self.target_point)     # self being the NSView, self.layer() being the CALayer "rootlayer"
#        NSLog( "mouseDown: hitLayer is: %s, p=%s" % ( PointToString( self.target_point ),  hitLayer.name() ) )
        
#        hitLayer.setBorderColor( CGColorCreateGenericGray(0.4, 0.4) )

        from Quartz import CGColorCreateGenericGray

        if hitLayer == self.layer():
            for l in self.selectList:
                l.setBorderWidth_( 0.0 )        
                l.setBackgroundColor_( self.textBkgndColor )
                
                #l.setBorderColor_( CGColorCreateGenericGray(0.4, 0.4) )

            self.selectList = []

        else:
            if hitLayer in self.selectList:             # list of all layers currently selected
                hitLayer.setBorderWidth_( 2.0 )  
                hitLayer.setBackgroundColor_( self.viewBkgndColor )
            else:
                self.selectList.append(hitLayer) 
                hitLayer.setBorderWidth_( 1.0 )        
                hitLayer.setBorderColor_( CGColorCreateGenericGray(0.75, 0.75) )        
                
        NSLog( "mouseDown: hitLayer is: %s, p=%s, selectList=%r" % (  hitLayer.name(), PointToString( self.target_point ), self.selectList ) )


#        if (hitLayer && hitLayer != self.layer) {
#            if (hitLayer != selectedLayer) {
#                selectedLayer.selected = NO;
#
#                selectedLayer = hitLayer;
#                selectedLayer.selected = YES;
#                [selectedLayer setNeedsDisplay];
#            }
#        }
#        else {
#            selectedLayer.selected = NO;
#            [selectedLayer setNeedsDisplay];
#            selectedLayer = nil;
#        }




#        self.l1.setPosition_( self.target_point ) # lower-left corner, when the anchorpoint is 0,0
        


    
    # create a list of cursors and cursorRects based on the layers so that AppKit can change the cursor?
    def resetCursorRects(self):
        super(PadView, self).resetCursorRects()
        b = self.bounds()  #  b.origin.x,   b.origin.y,   b.size.width,   b.size.height )

        NSLog( "class PadView received resetCursorRects.  bounds=%s", RectToString( self.bounds() ) ) # bounds=(0,0,791,498)

        self.addCursorRect_cursor_(self.bounds(), NSCursor.crosshairCursor()) # openHandCursor?

        # for resize triangle area.  TODO: create resize cursor.
        self.addCursorRect_cursor_(  ( ( b.size.width - 20.0, 0.0 ) , ( 20.0 , 20.0 ) ) , NSCursor.pointingHandCursor())  
                 
    def acceptsFirstResponder(self):
        """ accept keyboard events in the view """
        NSLog("class PadView received acceptsFirstResponder, returns YES.")
        return YES

    def keyDown_(self, ev): #  (NSEvent*)ev
        NSLog( "class PadView received keyDown_")
        #print dir(ev)
        NSLog(ev.characters())
        NSLog(ev.charactersIgnoringModifiers())

#       if( self.isInFullScreenMode ) {
#           if( [ev.charactersIgnoringModifiers hasPrefix: @"\033"] )       // Esc key
#               [self enterFullScreen: self];
#       }

    # almost want to subclass, but are there any new methods or variables?  yes: Pythonic accessors!
    
    def CreateCALayer(self, name , bounds=None , borderWidth=1.5, backgroundColor=None, borderColor=None, cornerRadius=25.0, zPosition = None ):
        
        l = CALayer.layer()
        l.setName_(name)
        if bounds != None:  
            l.setBounds_(bounds)
        l.setBorderWidth_(borderWidth)
        
        l.setCornerRadius_(cornerRadius)      
        
        if backgroundColor == None:
            l.setBackgroundColor_(self.textBkgndColor)
        else:
            l.setBackgroundColor_(backgroundColor)

        if borderColor == None:
            l.setBorderColor_( self.borderColor )
        else:
            l.setBorderColor_( borderColor )

#                hitLayer.setBorderColor_( CGColorCreateGenericGray(0.75, 0.75) )        

        if zPosition != None:  
            l.setZPosition_(zPosition)
            
        return l


    #    Case 2: If you're using a CATextLayer directly, you'll need to
    #    subclass CATextLayer and do something like the following in your
    #    drawing code:
    #
    #   We assume NSGraphicsContext saveGraphicsState in drawInContext
    #
    #    - (void)drawInContext:(CGContextRef)ctx
    #    {
    #    CGContextSetRGBFillColor (ctx, r, g, b, a);
    #    CGContextFillRect (ctx, [self bounds]);
    #    CGContextSetShouldSmoothFonts (ctx, true);
    #    [super drawInContext:ctx];
    #    }
    #
    #   also from WebKit(!)
    
#    [NSGraphicsContext saveGraphicsState];
#    CGContextSetShouldSmoothFonts([[NSGraphicsContext currentContext] graphicsPort], false);
#    [self _web_drawAtPoint:textPoint
#                      font:font
#                 textColor:bottomColor];
#
#    textPoint.y += 1;
#    [self _web_drawAtPoint:textPoint
#                      font:font
#                 textColor:topColor];
#    [NSGraphicsContext restoreGraphicsState];    

    #  The anchor point specifies how the bounds are positioned relative to the 
    # position property, as well as serving as the point that transforms are applied around. It is expressed in the 
    # unit coordinate system-the lower left of the layer bounds is 0.0,0.0, and the upper right is 1.0,1.0. 
    #  When you specify the frame of a layer, position is set relative to the anchor point. When you specify the 
    # position of the layer, bounds is set relative to the anchor point. 

    def CreateCATLayer(self, text , 
                        name=None,
                        font=None,   
                        textColor=None, backgroundColor=None,
                        bounds=None , borderWidth=0.0,  
                        theAnchorPoint = (0,0),
                        theAutoresizingMask = None , 
                        theAlignmentMode = None ,
                        thePosition = (20,20),
                        isWrapped = True , 
                        theTruncationMode = None,
                        zPosition = None
 ):                            


        from Quartz import CGImageSourceCreateWithURL, CGImageSourceCreateImageAtIndex, kCGColorBlack, CGColorCreateGenericRGB, CGRectMake, CGPointMake
        from Quartz import kCALayerWidthSizable , kCALayerMinYMargin, kCALayerMaxYMargin, kCAAlignmentCenter, kCAAlignmentLeft, kCATruncationMiddle, kCATruncationEnd


        cat = CATextLayer.alloc().init()

        # use attributed string?
        
        cat.setString_(text)
        

        if name != None:  
            cat.setName_(name)  # needed if we do our own layout?  really: will need even more complex "id" of each layer...

        if font==None: font = self.font

        cat.setFont_(font)
        cat.setFontSize_(font.pointSize() )        

        if textColor==None: 
            cat.setForegroundColor_(self.textColor)
        else:
            cat.setForegroundColor_(textColor)

        if backgroundColor == None:
            cat.setBackgroundColor_(self.textBkgndColor)
        else:
            cat.setBackgroundColor_(backgroundColor)


        #	calculate the size of the text layer

        theTextNSString = cat.string()
        
        attributes = NSDictionary.dictionaryWithObjectsAndKeys_(self.font, NSFontAttributeName, None )  # dict(object1,key1,object2,key2..,None)
                                          
        textSize =  theTextNSString.sizeWithAttributes_(attributes)        
 
#       No setting of bounds combined with constraint-based layout manager means auto text sizing?  

        # Note:  When a CATextLayer instance is positioned using the CAConstraintLayoutManager
        # the bounds of the layer is resized to fit the text content. 
        # [CATextLayer Class Reference, page 6]


#        if bounds == None:  
#            bounds = ( ( 0, font.descender() ) , ( textSize.width + 2 , font.ascender() - font.descender() ) )  # CGRectMake  # why "+ 2"? why not?
      
#        NSLog( "CreateCATLayer: bounds is: %r" % (bounds, ) )
        
#        cat.setBounds_(bounds)

        if zPosition != None:  
            cat.setZPosition_(zPosition)
            
        cat.setBorderWidth_( borderWidth )

        # following is workaround for not being able to import Quartz until *after* function definitions are read :(
        
        if theAlignmentMode == None: theAlignmentMode = kCAAlignmentCenter # kCAAlignmentLeft  
        if theTruncationMode == None: theTruncationMode = kCATruncationEnd # kCATruncationMiddle  
                                                    
        cat.setAlignmentMode_(theAlignmentMode)
        cat.setWrapped_(isWrapped)
        cat.setTruncationMode_(theTruncationMode)
        

        #    CGFloat inset = superlayer.borderWidth + 3;
        #    CGRect bounds = CGRectInset(superlayer.bounds, inset, inset);
        #    CGFloat height = font.ascender;
        #    CGFloat y = bounds.origin.y;
        #    if( resizingMask & kCALayerHeightSizable )
        #        y += (bounds.size.height-height)/2.0;
        #    else if( resizingMask & kCALayerMinYMargin )
        #        y += bounds.size.height - height;
        #    resizingMask &= ~kCALayerHeightSizable;
        #    catext1.bounds = CGRectMake(0, font.descender, bounds.size.width, height - font.descender);
        
        cat.setPosition_( thePosition  )
        
        cat.setAnchorPoint_( theAnchorPoint )

        #if theAutoresizingMask == None: 
        theAutoresizingMask = kCALayerWidthSizable  # | kCALayerMaxXMargin  

        #cat.setAutoresizingMask_( theAutoresizingMask )        
            
        return cat




        
#       rootLayer.backgroundColor = a

#       CGRect bounds = self.layer.bounds;
#       self.layer.backgroundColor = GetCGPatternNamed(@"/Library/Desktop Pictures/Small Ripples graphite.png");

#   drawRect is superfluous for this kind of display?

#   def drawRect_(self, rect):
#       NSLog("class PadView received drawRect_")
#       # drawing code here


        
        #// set the contents property to a CGImageRef .  The result of CGImageCreate is that we want 
        #// specified by theImage (loaded elsewhere) 

        #self.l2.setContents_( theImage )  # won't be clipped to corner radius?  unless we say clip to bounds?

    #   By default,thecontentofalayerisnotclippedto its bounds and corner radius.The masksToBounds property 
    #   can be set to true to clip the layer content to those values.         

        #self.l2.setMasksToBounds_( True )  # set to true to clip the layer content to layer's bounds and corner radius.

#        NSLog( "self.l2.contents is %r" % (self.l2.contents(),) ) # self.l2.contents is <CGImage 0x1d39b20>
        
#        rootLayer.addSublayer_(self.l2)
      
        #self.cat1 = self.CreateCATLayer( "Hello PadView TextLayer", name="cat1", isWrapped = True ) 

        #rootLayer.addSublayer_(self.cat1)

#        self.cat2 = self.CreateCATLayer( "Hello PadView TextLayer Too." ,  name="cat2", isWrapped = False, theTruncationMode = kCATruncationMiddle) 
#        rootLayer.addSublayer_(self.cat2)
        
#        NSLog( "self.cat2 is %r" % (self.cat2,) )


        
        #   CGRectMake() wants: (x, y, width, height)
        #   Rect is rect.origin.x,   rect.origin.y,   rect.size.width,   rect.size.height
