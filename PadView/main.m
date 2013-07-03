//
//  main.m
//  PadView
//
//  Created by donb on 2010.05.03.
//  Copyright __MyCompanyName__ 2010. All rights reserved.
//

#import <Python/Python.h>
#import <Cocoa/Cocoa.h>

int main(int argc, char *argv[])
{
    NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];
    
    NSBundle *mainBundle = [NSBundle mainBundle];
    NSString *resourcePath = [mainBundle resourcePath];
    NSArray *pythonPathArray = [NSArray arrayWithObjects: resourcePath, [resourcePath stringByAppendingPathComponent:@"PyObjC"], nil];
    
    setenv("PYTHONPATH", [[pythonPathArray componentsJoinedByString:@":"] UTF8String], 1);
    
    NSArray *possibleMainExtensions = [NSArray arrayWithObjects: @"py", @"pyc", @"pyo", nil];
    NSString *mainFilePath = nil;
    
    for (NSString *possibleMainExtension in possibleMainExtensions) {
        mainFilePath = [mainBundle pathForResource: @"main" ofType: possibleMainExtension];
        if ( mainFilePath != nil ) break;
    }
    
	if ( !mainFilePath ) {
        [NSException raise: NSInternalInconsistencyException format: @"%s:%d main() Failed to find the Main.{py,pyc,pyo} file in the application wrapper's Resources directory.", __FILE__, __LINE__];
    }
    /*
	  When you use NSApplication, some Cocoa things are initialized. Since I was not using NSApplication and just doing this drawing from main(), bad things would happen. I need to initialize some Cocoa stuff myself. Fortunately, this is just one line of code: [http://javworld.com/Extreme/GraphicsProg.html]
	 */
	
	//NSApplicationLoad(); 
	
    Py_SetProgramName("/usr/bin/python");
    Py_Initialize();
    PySys_SetArgv(argc, (char **)argv);
    
    const char *mainFilePathPtr = [mainFilePath UTF8String];
    FILE *mainFile = fopen(mainFilePathPtr, "r");
    int result = PyRun_SimpleFile(mainFile, (char *)[[mainFilePath lastPathComponent] UTF8String]);
    
    if ( result != 0 )
        [NSException raise: NSInternalInconsistencyException
                    format: @"%s:%d main() PyRun_SimpleFile failed with file '%@'.  See console for errors.", __FILE__, __LINE__, mainFilePath];
    
    [pool drain];
    
    return result;
}
