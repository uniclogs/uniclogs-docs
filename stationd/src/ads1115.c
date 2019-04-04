#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <linux/i2c.h>
#include "common.h"
#include "ads1115.h"

void ADS1115SetSlave(int i2c_fd)
{
	/* Set ADS1115 as slave device */
	if (ioctl(i2c_fd, I2C_SLAVE, ADS1115_I2C_ADDR) < 0) {
		logmsg(LOG_ERR, "Error: Failed setting ADS1115 as slave: %s\n", strerror(errno));
		exit(EXIT_FAILURE);
	}
}
