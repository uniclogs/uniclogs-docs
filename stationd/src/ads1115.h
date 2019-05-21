#ifndef _ADS1115_H_
#define _ADS1115_H_

#include <stdint.h>
#include "common.h"

/* Register values for ADS1115 */
#define ADS1115_CONV_REG	0x00
#define ADS1115_CONFIG_REG	0x01
#define ADS1115_LO_REG		0x02
#define ADS1115_HIGH_REG	0x03

#define ADS1115_START_CONV(n)	((0xC + n) << 12)

void ADS1115SetSlave(int i2c_fd);
int16_t ADS1115ReadVal(int i2c_fd, uint8_t sensor);

#endif
