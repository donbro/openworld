#
#  main.py
#  PadView
#
#  Created by donb on 2010.05.03.
#  Copyright __MyCompanyName__ 2010. All rights reserved.
#

import sys
import os
import objc
import Foundation
from Foundation import NSLog
import AppKit

from PyObjCTools import AppHelper

 # Importing the Quartz framework before Cocoa connects to the window  
 # server, eg , doing an 'import  Quartz' before doing 'AppHelper.runEventLoop()' or  
 # 'NSApplication.sharedApplication' will fail,
 # [http://mail.python.org/pipermail/pythonmac-sig/2007-November/019430.html]

NSLog("main.py: sys.version is " + "".join(sys.version.split('\n')) )


# import modules containing classes required to start application and load MainMenu.nib
import PVAppController, PVController, PadView

appBundleResoucePath = AppKit.NSBundle.mainBundle().resourcePath().fileSystemRepresentation()
NSLog("main.py: application bundle is: %s" % ( appBundleResoucePath ) )

pyfiles = [x for x in os.listdir( appBundleResoucePath ) if x[-3:] == '.py']
NSLog("main.py: Python files are: %r" % ( pyfiles ,  ) )

if sys.argv[0] in pyfiles: pyfiles.remove(sys.argv[0])
NSLog("main.py: sys.argv[0] is %s" %  sys.argv[0]	)

#for file in pyfiles:
#  __import__(os.path.splitext(file)[0])
  
# pass control to AppKit
AppHelper.runEventLoop()