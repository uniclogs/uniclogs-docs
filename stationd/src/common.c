#include <stdio.h>
#include <stdbool.h>
#include <syslog.h>
#include <stdarg.h>

#include "common.h"

void logmsg(int priority, const char *fmt, ...){
    va_list args;
    va_start(args, fmt);
    vsyslog(priority, fmt, args);
    vfprintf((priority>4?stdout:stderr), msg, args);
    fprintf((priority>4?stdout:stderr), "\n");
    va_end(args);
}
