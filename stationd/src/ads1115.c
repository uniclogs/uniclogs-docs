#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <linux/i2c.h>
#include <math.h>
#include "common.h"
#include "ads1115.h"

float vhf_conversion(float volt);
float uhf_conversion(float volt);
float l_conversion(float volt);

static int retries;
static uint8_t pga[] = {
	0x4,
	0x2,
	0x1
};
static float gran[] = {
	15.625E-6,
	62.5E-6,
	125E-6
};
static float (*sensor_func[])(float) = {
	vhf_conversion,
	uhf_conversion,
	l_conversion
};

void ADS1115SetSlave(int i2c_fd)
{
	/* Set ADS1115 as slave device */
	if (ioctl(i2c_fd, I2C_SLAVE, ADS1115_I2C_ADDR) < 0) {
		logmsg(LOG_ERR, "Error: Failed setting ADS1115 as slave: %s\n", strerror(errno));
		exit(EXIT_FAILURE);
	}
}

float ADS1115ReadPwr(int i2c_fd, uint8_t sensor)
{
	int32_t regval = 0;

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

	regval &= ~(0xFE);
	regval |= ADS1115_STARTCONV(sensor) | pga[sensor];

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
	regval = ((regval << 8) & 0xFF00) | ((regval >> 8) & 0x00FF);
	logmsg(LOG_DEBUG, "Read 0x%04X...\n", regval);

	return (*sensor_func[sensor])(gran[sensor] * regval);
}

float vhf_conversion(float volt)
{
	return 74*volt + 1.05;
}

float uhf_conversion(float volt)
{
	return 5.21 * pow(volt, 2) + 5.34 * volt + 0.217;
}

float l_conversion(float volt)
{
	return 2.16 * pow(volt, 2) + 0.149 * volt + 0.105;
}
