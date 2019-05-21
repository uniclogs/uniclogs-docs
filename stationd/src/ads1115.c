#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <linux/i2c.h>
#include "common.h"
#include "ads1115.h"

static int retries;

void ADS1115SetSlave(int i2c_fd)
{
	/* Set ADS1115 as slave device */
	if (ioctl(i2c_fd, I2C_SLAVE, ADS1115_I2C_ADDR) < 0) {
		logmsg(LOG_ERR, "Error: Failed setting ADS1115 as slave: %s\n", strerror(errno));
		exit(EXIT_FAILURE);
	}
}

int16_t ADS1115ReadVal(int i2c_fd, uint8_t sensor)
{
	int16_t regval = 0;
	logmsg(LOG_DEBUG, "Reading value of sensor number: %u\n", sensor);
	if (sensor > 3) {
		logmsg(LOG_WARNING, "Invalid sensor number!\n");
		return 0;
	}
	ADS1115SetSlave(i2c_fd);

	logmsg(LOG_DEBUG, "Reading current config register state...\n");
	if ((regval = i2c_smbus_read_word_data(i2c_fd, ADS1115_CONFIG_REG)) < 0) {
		logmsg(LOG_ERR, "Error: Failed reading current config register state: %s\n", strerror(errno));
		return 0;
	}
	logmsg(LOG_DEBUG, "Read 0x%04X...\n", regval);

	regval &= ~(0xF << 12);
	regval |= ADS1115_START_CONV(sensor);

	logmsg(LOG_DEBUG, "Writing 0x%04X...\n", regval);
	for (retries = 2; retries > 0 && i2c_smbus_write_word_data(i2c_fd, ADS1115_CONFIG_REG, regval) < 0; retries--)
		usleep(100);
	if (retries == 0) {
		logmsg(LOG_ERR, "Error: Failed starting conversion of sensor %u: %s\n", sensor, strerror(errno));
		return 0;
	}
	usleep(100);
	logmsg(LOG_DEBUG, "Reading conversion value...\n");
	if ((regval = i2c_smbus_read_word_data(i2c_fd, ADS1115_CONV_REG)) < 0) {
		logmsg(LOG_ERR, "Error: Failed reading conversion value: %s\n", strerror(errno));
		return 0;
	}
	logmsg(LOG_DEBUG, "Read 0x%04X...\n", regval);

	return regval;
}
