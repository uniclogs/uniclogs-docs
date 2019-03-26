#ifndef _COMMON_H_
#define _COMMON_H_

#include <stdarg.h>
#include <stdbool.h>
#include <pthread.h>
#include <syslog.h>

#ifndef DEFAULT_PORT
#define DEFAULT_PORT "8080"
#endif
#ifndef DEFAULT_PID_FILE
#define DEFAULT_PID_FILE "/run/stationd/stationd.pid"
#endif
#ifndef DEFAULT_I2C_DEV
#define DEFAULT_I2C_DEV  "/dev/i2c-0"
#endif
#ifndef MCP9808_I2C_ADDR
#define MCP9808_I2C_ADDR 0x18
#endif
#ifndef MCP23017_I2C_ADDR
#define MCP23017_I2C_ADDR 0x20
#endif
#ifndef ADS1115_I2C_ADDR
#define ADS1115_I2C_ADDR 0x48
#endif
#ifndef MAXMSG
#define MAXMSG 50
#endif

pthread_mutex_t msg_mutex;
pthread_cond_t msg_cond;
char msg[MAXMSG];

extern bool daemon_flag;
extern bool verbose_flag;

void logmsg(int priority, const char *fmt, ...);

#endif
