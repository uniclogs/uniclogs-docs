#include <stdio.h>
#include <stdbool.h>
#include <syslog.h>
#include <stdarg.h>

#include "common.h"

void logmsg(int priority, const char *msg, va_list args){
    syslog(priority, msg, args);
    fprintf((priority > 4 ? stdout : stderr), msg, args);
    fprintf((priority > 4 ? stdout : stderr), "\n");
}
