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
# import Quartz



class PadViewAppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, sender):
        NSLog("Application did finish launching.")

def PointToString(p):
    return "{ %.0f, %.0f }" % (  p.x,   p.y, )

def RectToString(rect):
    return "(%.0f,%.0f,%.0f,%.0f)" % (  rect.origin.x,   rect.origin.y,   rect.size.width,   rect.size.height )

def RectToStringz(rect):
    return "(%4s,%4s), size (%4s,%4s)" % ( "%.1f" % rect.origin.x, "%.1f" % rect.origin.y, "%.1f" % rect.size.width, "%.1f" % rect.size.height )
    return "(%5s,%5s), size (%5s,%5s)" % ( "%.1f" % rect.origin.x, "%.1f" % rect.origin.y, "%.1f" % rect.size.width, "%.1f" % rect.size.height )

def RectToLongString(rect):
    return "origin: (x=%-5s, y=%-5s), size: (width=%-5s, height=%-5s)" % ( "%.1f" % rect.origin.x, "%.1f" % rect.origin.y, "%.1f" % rect.size.width, "%.1f" % rect.size.height )


class PadView(NSView):

	def initWithFrame_(self, frame):                

		NSLog("class PadView received initWithFrame")
		NSLog("initWithFrame: sys.version is " + "".join(sys.version.split('\n')) )

		super(PadView, self).initWithFrame_(frame)       # NSView not correctly initialized. Did you forget to call super?"
		
		NSLog("initWithFrame: begin import Quartz")		# have to wait until here to import Quartz or else we get a '_CGSDefaultConnection() is NULL' error?
		from Quartz import CGColorCreateGenericRGB
		NSLog("initWithFrame: end import Quartz")

		self.textColor = CGColorCreateGenericRGB(0.1, 0.2, 0.3, 1.0);
		self.textBkgndColor = CGColorCreateGenericRGB(0.8, 0.8, 0.8, 1.0);  # light gray

		self.font       =   NSFont.fontWithName_size_("Skia",14.0)

		NSLog("initWithFrame: font is %r" % (self.font, ) )

		#self.showsGrid = True
		
		return self


	def awakeFromNib(self):

		NSLog( "class PadView received awakeFromNib")
		NSLog( "awakeFromNib: frame=%s, bounds=%s" % ( RectToString( self.frame() ) , RectToString( self.bounds() ) ) )

		NSLog( "self.wantsLayer() is %r" % (self.wantsLayer(),)  )

		rootLayer = self.layer()

		# self.postsLayer.layoutManager = [[[CStackLayoutManager alloc] init] autorelease];

		NSLog( "(original) backgroundColor is %r" % ( rootLayer.backgroundColor() ,) )
		
		NSLog( "rootLayer.bounds() is %s" % (RectToString(rootLayer.bounds()) ,) )
		#NSLog( "rootLayer.bounds() is %@" ,rootLayer.bounds() ) # <CGRect origin=<CGPoint x=0.0 y=0.0> size=<CGSize width=791.0 height=498.0>>
		
#		print rootLayer["frame"] # TypeError: '_NSViewBackingLayer' object is unsubscriptable
		
		# [layer setValue:[NSNumber numberWithFloat:50.0f] forKeyPath:@"frame.size.width"];
		print rootLayer.valueForKeyPath_("frame.size.width")
		
		NSLog( "rootLayer is: %@", rootLayer );



		# if you get a call signature resembling ['__call__', '__class__', .., 'selector', 'self', 'signature'] 
		# then you have an 'objc.native_selector' object which you probably want to call, not refer to.
		
		path = "/Library/Desktop Pictures/Small Ripples graphite.png"
		
		url = NSURL.fileURLWithPath_(path)
		
		NSLog( "url is: %@",  url  );
		NSLog( "url is: %@", str(url) );

#		print url
#		NSLog( "url is %r" % (url,) )
		
		from Quartz import CGImageSourceCreateWithURL, CGImageSourceCreateImageAtIndex, kCGColorBlack, CGColorCreateGenericRGB, CGRectMake, CGPointMake
		from Quartz import kCALayerWidthSizable , kCALayerMinYMargin, kCALayerMaxYMargin, kCAAlignmentCenter, kCAAlignmentLeft, kCATruncationMiddle

		#kCALayerMaxYMargin  The top margin between the receiver and its superview is flexible.

		
		imagesrc = CGImageSourceCreateWithURL(url, None)
		
		NSLog( "imagesrc is %r" % (imagesrc,) )
		
		image = CGImageSourceCreateImageAtIndex(imagesrc, 0, None);

		NSLog( "image is %r" % (image,) )



#		CATransaction.begin()
		
		

#		self.setWantsLayer_(YES)

		

		rootLayer.setBackgroundColor_(kCGColorBlack) 
		
#		rootLayer.setNeedsDisplay()

#		CATransaction.commit()
		
		
#		rootLayer.setNeedsDisplayOnBoundsChange_(True)

		b = rootLayer.backgroundColor()  # None

		NSLog( "backgroundColor (after) is %r" % (b,) )
		
#		bounds.size.height -= 32;
#		catext1 = AddTextLayer(self.layer,
#								 nil, [NSFont boldSystemFontOfSize: 24], 
#								 kCALayerWidthSizable | kCALayerMinYMargin);


		#CGColorRef 
		#textColor = CGColorCreateGenericRGB(0.1, 0.2, 0.3, 1.0);
		#exampleCATextLayer.foregroundColor = fgColor;

		theBounds = CGRectMake(0, 20, 200, 40)
		theAnchorPoint = CGPointMake(0,0) 
		theAutoresizingMask = kCALayerWidthSizable | kCALayerMaxYMargin 
		theAlignmentMode = kCAAlignmentLeft # kCAAlignmentCenter # Text is visually center aligned
		
		isWrapped = True

									# kCAAlignmentLeft Text is visually left aligned.

		# kCALayerWidthSizable   The receiver's width is flexible.

		# The font property is only used when the string property is not an NSAttributedString.
		
		theTruncationMode = kCATruncationMiddle
		#Each line is displayed so that the beginning and end fit in the container and the missing text is indicated by some kind of ellipsis glyph in the middle.

		#Available in Mac OS X v10.5 and later.		

		thePosition = [40,20] # CGPointMake(5,20) 
		self.catext1 = AddTextLayer(rootLayer, "Hello PadView TextLayer", self.font, self.textColor,   self.textBkgndColor, 
							theBounds, thePosition, theAnchorPoint , theAutoresizingMask , theAlignmentMode, isWrapped, theTruncationMode)
		
		thePosition = [240,20] # CGPointMake(5,20) 
		isWrapped = False
		self.catext2 = AddTextLayer(rootLayer, "Hello PadView TextLayer Too.", self.font, self.textColor,   self.textBkgndColor, 
							theBounds, thePosition, theAnchorPoint , theAutoresizingMask , theAlignmentMode, isWrapped, theTruncationMode)

		
		NSLog( "self.catext1 is %r" % (self.catext1,) )
		


#		CFURLRef url = (CFURLRef) [NSURL fileURLWithPath: path];
#		CGImageSourceRef src = CGImageSourceCreateWithURL(url, NULL);
#		if( src ) {
#			image = CGImageSourceCreateImageAtIndex(src, 0, NULL);
#			CFRelease(src);
#			if(!image) NSLog(@"Warning: CGImageSourceCreateImageAtIndex failed on file %@ (ptr size=%u)",path,sizeof(void*));
#		}
#		return image;


		
#		rootLayer.backgroundColor = a

#		CGRect bounds = self.layer.bounds;
#		self.layer.backgroundColor = GetCGPatternNamed(@"/Library/Desktop Pictures/Small Ripples graphite.png");

#	drawRect is superfluous for this kind of display?

#	def drawRect_(self, rect):
#		NSLog("class PadView received drawRect_")
#		# drawing code here
 
 
	def mouseDown_(self, event):
		eventLocation = event.locationInWindow()
		#NSLog("class PadView received mouseDown_")


		self.target_point = self.convertPoint_fromView_(eventLocation, None)
		NSLog( "mouseDown: self.target_point is %r" % (self.target_point,) )

		thePosition = [240,220] # CGPointMake(5,20) 
		self.catext1.setPosition_( self.target_point ) # lower-left corner, when the anchorpoint is 0,0

		self.catext2.setBorderWidth_(1.0)
	
		
#		print dir(self.acceptsFirstResponder)
		
	def acceptsFirstResponder(self):
		NSLog("class PadView received acceptsFirstResponder, returns YES.")
		return YES

	def keyDown_(self, ev): #  (NSEvent*)ev
		NSLog( "class PadView received keyDown_")
		#print dir(ev)
		NSLog(ev.characters())
		NSLog(ev.charactersIgnoringModifiers())

#		if( self.isInFullScreenMode ) {
#			if( [ev.charactersIgnoringModifiers hasPrefix: @"\033"] )       // Esc key
#				[self enterFullScreen: self];
#		}

 
# from Quartz.CoreGraphics import CGRectMake, CGPointMake

def AddTextLayer(  superlayer, text,  font, textColor ,  textBkgndColor, theBounds, thePosition, theAnchorPoint, theResizingMask, theAlignmentMode, isWrapped , theTruncationMode):

	catext1 = CATextLayer.alloc().init()
	
	catext1.setString_(text)
	catext1.setFont_(font)
	catext1.setFontSize_(font.pointSize() ) # 14.0) # self.fontSize # font.pointSize) # ValueError: depythonifying 'float', got 'objc.native_selector'

	NSLog( "AddTextLayer: superlayer at " + RectToString( superlayer.bounds() )  )
	NSLog( "AddTextLayer: new text layer at " + RectToString( theBounds )  )

	#The default foreground color is white, so we get more contrast with something darker...

	catext1.setForegroundColor_(textColor)
	catext1.setBackgroundColor_(textBkgndColor)

	# kCAAlignmentCenter
	
	# kCALayerWidthSizable , kCALayerMinYMargin
	
	#    NSString *mode;
	
	#    if( resizingMask & kCALayerWidthSizable )
	#        mode = @"center";
	#    else if( resizingMask & kCALayerMinXMargin )
	#        mode = @"right";
	#    else
	#        mode = @"left";
	#    resizingMask |= kCALayerWidthSizable;
	
	#    catext1.alignmentMode = mode;
	
	catext1.setAlignmentMode_(theAlignmentMode)
	catext1.setWrapped_(isWrapped)
	catext1.setTruncationMode_(theTruncationMode)
	

	#    CGFloat inset = superlayer.borderWidth + 3;
	#    CGRect bounds = CGRectInset(superlayer.bounds, inset, inset);
	#    CGFloat height = font.ascender;
	#    CGFloat y = bounds.origin.y;
	#    if( resizingMask & kCALayerHeightSizable )
	#        y += (bounds.size.height-height)/2.0;
	#    else if( resizingMask & kCALayerMinYMargin )
	#        y += bounds.size.height - height;
	#    resizingMask &= ~kCALayerHeightSizable;

	catext1.setBounds_( theBounds )
	
	#    catext1.bounds = CGRectMake(0, font.descender, bounds.size.width, height - font.descender);
	
	catext1.setPosition_( thePosition  )
	
	catext1.setAnchorPoint_( theAnchorPoint )

	catext1.setAutoresizingMask_(theResizingMask)

	NSLog( "adding text layer(    %s, %r,  %r, %r ,%r, %s, %s, %s)" \
		% (  RectToString (superlayer.bounds()), text,font.fontName(), font.pointSize(), textColor, RectToString( catext1.bounds() ) , 
						PointToString(catext1.position()), PointToString(catext1.anchorPoint()) )  )
	

	superlayer.addSublayer_(catext1)
	
	return catext1





#		aLayer.name = u"vlcopengllayer"
#		if self.layoutManager:
#			self.layoutManager.setOriginalVideoSize_(aLayer.bounds().size())

#		rootLayer.setLayoutManager_(layoutManager)
#		rootLayer.insertSublayer_atIndex_(aLayer, 0)
#		aLayer.setNeedsDisplayOnBoundsChange_(True)
