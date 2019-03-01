#ifndef _MCP9808_H_
#define _MCP9808_H_

#include <stdint.h>
#include "common.h"

// Register values for MCP9808
#define MCP9808_TEMP_REG    0x05

#define TEMP_MASK           0x1FFF

float MCP9808GetTemp(int i2c_fd);

#endif
