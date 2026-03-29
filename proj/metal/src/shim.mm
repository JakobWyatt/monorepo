#include "shim.h"

#import <AppKit/AppKit.h>
#import <QuartzCore/QuartzCore.h>

void ConfigureMetalWindow(id metalWindow, CA::MetalLayer* metalLayer)
{
    auto* window = (__bridge NSWindow*)metalWindow;
    auto* layer = (__bridge CAMetalLayer*)metalLayer;
    window.contentView.wantsLayer = true;
    window.contentView.layer = layer;
}
