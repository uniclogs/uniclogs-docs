#ifndef _MCP9808_H_
#define _MCP9808_H_

#include <stdint.h>
#include "common.h"

// Register values for MCP9808
#define MCP9808_TEMP_REG        0x05

#define TEMP_SIGN_MASK          0x1000
#define TEMP_VAL_MASK           0x0FFF

void MCP9808SetSlave(int i2c_fd);

float MCP9808GetTemp(int i2c_fd);

#endif
