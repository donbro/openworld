#
#  CGImageUtils.py
#  PadView
#
#  Created by donb on 2010.05.18.
#  Copyright (c) 2010 __MyCompanyName__. All rights reserved.
#

from Foundation import NSURL, NSLog

#
#   import Quartz
#

from Quartz import CGRectMake, CGPointMake, kCAConstraintMidY, kCAConstraintMidX, kCAConstraintWidth, kCAConstraintMinX, kCAConstraintMinY,\
            kCAConstraintMaxX, kCAConstraintMaxY
from Quartz import CGImageSourceCreateWithURL, CGImageSourceCreateImageAtIndex, kCGColorBlack, CGColorCreateGenericRGB
from Quartz import kCALayerWidthSizable , kCALayerMinYMargin, kCALayerMaxYMargin, kCAAlignmentCenter, kCAAlignmentLeft, kCATruncationMiddle
from Quartz import CATransform3DIdentity
from Quartz import CGColorSpaceCreatePattern, CGColorCreateWithPattern
from Quartz import CGContextDrawImage, CGRectMake, CGImageGetWidth, CGImageGetHeight, CGPatternCreate, CGAffineTransformIdentity, \
            kCGPatternTilingConstantSpacing

#pragma mark -
#pragma mark PATTERNS:
#MARK: PATTERNS

    #   I think it would be more efficient to set the layer's background
    #   "color" to a checkered pattern. You just need to load the pattern tile
    #   image (four squares) from a file into a CGImage (or draw it on the
    #   fly), then wrap the CGImage in a CGPattern and make a CGColor from it.
    #   The QuartzUtils module of my GeekGameBoard library has a
    #   GetCGPatternNamed function to do this:
    #   http://mooseyard.com/hg/hgwebdir.cgi/GeekGameBoard/file/tip/Source/QuartzUtils.m 
 
#   The userinfo for CGDataConsumerCreate, ... , CGPathApply, CGPatternCreate, ... can be any Python object.
#   CGPatternCreate: the callback argument is a single function: the drawPattern callback.
#   [http://pyobjc.sourceforge.net/documentation/pyobjc-framework-Quartz/api-notes.html]

#CGPatternRef 
def CreateImagePattern( inImage ): # CGImageRef image 


    def releasePatternImage(info):        # (void *info)
        NSLog( "releasePatternImage: info is: %r" % ( info, ) )
        image = info

    def drawPatternImage(info, context):
        image = info

        NSLog( "drawPatternImage: image is: %@, context is: %@" , info, context  )
    
        CGContextDrawImage(context, CGRectMake( 0,0, CGImageGetWidth(info),CGImageGetHeight(info) ), info);
        
    #end drawPatternImage()
 

    width = CGImageGetWidth(inImage)
    height = CGImageGetHeight(inImage)

    NSLog( "CreateImagePattern: image is: %@, width is: %@, height is: %@" , inImage  , width, height  )


    bounds = CGRectMake(0, 0, width, height)

    #   CGAffineTransformIdentity is <CGAffineTransform a=1.0 b=0.0 c=0.0 d=1.0 tx=0.0 ty=0.0>
    #   argument 8 must be 2-item sequence, not function  static const CGPatternCallbacks callbacks = {0, &drawPatternImage, &releasePatternImage};

    pattern = CGPatternCreate(inImage, bounds, 
                CGAffineTransformIdentity, 
                width, height, 
                kCGPatternTilingConstantSpacing, 
                True, 
                ( drawPatternImage, releasePatternImage ) 
              )

    return pattern





    #
    #   background (pattern or simple color) for layer
    #

def CreatePatternColor( inImage ):

#    from Quartz import CGColorSpaceCreatePattern, CGColorCreateWithPattern

    pattern = CreateImagePattern( inImage );
    
    #   
    #   CGColorSpaceCreatePattern ==>  Creates a pattern color space.
    #
    #       CGColorSpaceRef  
    #       CGColorSpaceCreatePattern (   CGColorSpaceRef baseSpace  )
    #           baseSpace ==> For masking patterns, the underlying color space that specifies the colors to be painted through the mask. 
    #             For colored patterns, you should pass NULL.


    theCGColorSpace = CGColorSpaceCreatePattern( None );
    
    
    #
    #   CGColorCreateWithPattern ==> Creates a Quartz color using a 
    #       list of intensity values (including alpha), a pattern color space, and a pattern.
    #
    #       CGColorRef 
    #       CGColorCreateWithPattern (  CGColorSpaceRef colorspace,  CGPatternRef pattern,  const CGFloat components[] )
    #
    #           colorspace ==> A pattern color space for the new color. Quartz retains the color space you pass in. On return, you may safely release it.
    #
    #           pattern ==> A pattern for the new color object. Quartz retains the pattern you pass in. On return, you may safely release it.
    #
    #           components ==> An array of intensity values describing the color. 
    #             The array should contain n + 1 values that correspond to the n color components 
    #               in the specified color space, followed by the alpha component. 
    #                 Each component value should be in the range appropriate for the color space. 
    #                 Values outside this range will be clamped to the nearest correct value.
    #
    #           Return Value ==> A new Quartz color. You are responsible for releasing this object using CGColorRelease.
    #


    theCGColor = CGColorCreateWithPattern( theCGColorSpace, pattern, (0.5, 0.5, 0.5, 1.0))  # alpha of 0.5 creates a transparent background?

    #    CGColorSpaceRelease(space);
    #    CGPatternRelease(pattern);
    
    return theCGColor


def CreatePatternColorFromPath( path ):

    url = NSURL.fileURLWithPath_(path)
    NSLog( "CreatePatternColorFromPath( %@ )",  url  );

    #
    #   Create image source from URL
    #
    #   An image source abstracts the data-access task and eliminates the need for you to manage data through a raw memory buffer. 
    #   An image source can contain more than one image, thumbnail images, and properties for each image and the image file. 
    #   When you are working with image data and your application runs in Mac OS X v10.4 or later, image 
    #     sources are the preferred way to move image data into your application.
    #
    #   CGImageSource objects, available in Mac OS X v10.4 or later, abstract the data-reading task. An image source can 
    #     read image data from a   URL, a CFData object, or a data consumer. After creating a CGImageSource object for the 
    #     appropriate source, you can obtain images, thumbnails, image properties, and other image information using CGImageSource functions.
    #
    #   CGImageSourceCreateWithURL ==> Creates an image source that reads from a location specified by a URL.
    #
    #   CGImageSourceCreateImageAtIndex ==> Creates a CGImage object for the image data associated with the specified index in an image source.
    #     Create an image from the first item in the image source.                                                   
    
    imagesrc = CGImageSourceCreateWithURL(url, None)        
#    NSLog( "CreatePatternColorFromPath: imagesrc is %r" % (imagesrc,) )

    theImage = CGImageSourceCreateImageAtIndex(imagesrc, 0, None);
#    NSLog( "CreatePatternColorFromPath: theImage is %r" % (theImage,) )

    #        pattern = CreatePatternColor( GetCGImageNamed(name) );

    return CreatePatternColor( theImage )


#       CFURLRef url = (CFURLRef) [NSURL fileURLWithPath: path];
#       CGImageSourceRef src = CGImageSourceCreateWithURL(url, NULL);
#       if( src ) {
#           image = CGImageSourceCreateImageAtIndex(src, 0, NULL);
#           CFRelease(src);
#           if(!image) NSLog(@"Warning: CGImageSourceCreateImageAtIndex failed on file %@ (ptr size=%u)",path,sizeof(void*));
#       }
#       return image;


def LoadImageFromPath( path ):

    url = NSURL.fileURLWithPath_(path)
    NSLog( "LoadImageFromPath( %@ )",  url  );

    #
    #   Create image source from URL
    #
    #   An image source abstracts the data-access task and eliminates the need for you to manage data through a raw memory buffer. 
    #   An image source can contain more than one image, thumbnail images, and properties for each image and the image file. 
    #   When you are working with image data and your application runs in Mac OS X v10.4 or later, image 
    #     sources are the preferred way to move image data into your application.
    #
    #   CGImageSource objects, available in Mac OS X v10.4 or later, abstract the data-reading task. An image source can 
    #     read image data from a   URL, a CFData object, or a data consumer. After creating a CGImageSource object for the 
    #     appropriate source, you can obtain images, thumbnails, image properties, and other image information using CGImageSource functions.
    #
    #   CGImageSourceCreateWithURL ==> Creates an image source that reads from a location specified by a URL.
    #
    #   CGImageSourceCreateImageAtIndex ==> Creates a CGImage object for the image data associated with the specified index in an image source.
    #     Create an image from the first item in the image source.                                                   
    
    imagesrc = CGImageSourceCreateWithURL(url, None)        
#    NSLog( "LoadImageFromPath: imagesrc is %r" % (imagesrc,) )

    theImage = CGImageSourceCreateImageAtIndex(imagesrc, 0, None);
#    NSLog( "LoadImageFromPath: theImage is %r" % (theImage,) )
    
    return theImage

   
if __name__ == '__main__':


    path = "/Users/donb/projects/PadView/UI/checkerboard bkgnd pattern cell 75px.png"


    theCGPatternColor = CreatePatternColorFromPath( path )

    NSLog( "theCGPatternColor is %r" % ( theCGPatternColor, )  )

    #   
    #   Setting theCGPatternColor to None changes:
    #       PyObjC: Exception during dealloc of proxy: <type 'exceptions.TypeError'>: 'NoneType' object is not callable
    #   Into:
    #       releasePatternImage: info is: <CGImage 0x225fad0>
    #   At the end of the script.

    theCGPatternColor = None

