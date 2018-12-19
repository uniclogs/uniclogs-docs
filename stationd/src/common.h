#ifndef _COMMON_H_
#define _COMMON_H_

#include <stdarg.h>
#include <stdbool.h>
#include <syslog.h>
#include <semaphore.h>

#ifndef DEFAULT_PORT
#define DEFAULT_PORT "8080"
#endif
#ifndef DEFAULT_PID_FILE
#define DEFAULT_PID_FILE "/run/stationd/stationd.pid"
#endif
#ifndef DEFAULT_I2C_DEV
#define DEFAULT_I2C_DEV  "/dev/i2c-0"
#endif
#ifndef DEFAULT_I2C_ADDR
#define DEFAULT_I2C_ADDR 0x20
#endif
#ifndef MAXMSG
#define MAXMSG 50
#endif

sem_t msgpending;
char msg[MAXMSG];

extern bool daemon_flag;
extern bool verbose_flag;

void logmsg(int priority, const char *fmt, ...);

#endif
