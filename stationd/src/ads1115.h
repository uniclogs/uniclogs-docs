#ifndef _ADS1115_H_
#define _ADS1115_H_

#include <stdint.h>
#include "common.h"

/* Register values for ADS1115 (IOCON.BANK = 0) */

void ADS1115SetSlave(int i2c_fd);

#endif
