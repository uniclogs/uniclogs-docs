#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <linux/i2c.h>
#include "common.h"
#include "mcp23017.h"

void MCP23017Init(int i2c_fd){
    // Set MCP23017 as slave device
    if (ioctl(i2c_fd, I2C_SLAVE, MCP23017_I2C_ADDR) < 0){
        logmsg(LOG_ERR, "Error: Failed setting MCP23017 as slave: %s\n", strerror(errno));
        exit(EXIT_FAILURE);
    }

    // Configure GPIOA and GPIOB as output (IODIR = 0x00)
    if (i2c_smbus_write_word_data(i2c_fd, MCP23017_IODIR_WORD_REG, 0x0000) < 0){
        logmsg(LOG_ERR, "Error: Failed setting GPIO as output: %s\n", strerror(errno));
        exit(EXIT_FAILURE);
    }

    // Reset output pins
    MCP23017BitReset(i2c_fd);
}

int MCP23017BitSet(int i2c_fd, uint8_t bit){
    uint16_t regval;

    if ((regval = i2c_smbus_read_word_data(i2c_fd, MCP23017_GPIO_WORD_REG)) < 0){
        logmsg(LOG_ERR, "Error: Failed reading current GPIO output state: %s\n", strerror(errno));
        return regval;
    }

    regval |= (0x1 << bit);

    if (i2c_smbus_write_word_data(i2c_fd, MCP23017_GPIO_WORD_REG, regval) < 0){
        logmsg(LOG_ERR, "Error: Failed setting GPIO output state: %s\n", strerror(errno));
        return -1;
    }

    return regval;
}


int MCP23017BitClear(int i2c_fd, uint8_t bit){
    uint16_t regval;

    if ((regval = i2c_smbus_read_word_data(i2c_fd, MCP23017_GPIO_WORD_REG)) < 0){
        logmsg(LOG_ERR, "Error: Failed reading current GPIO output state: %s\n", strerror(errno));
        return regval;
    }

    regval &= ~(0x1 << bit);

    if (i2c_smbus_write_word_data(i2c_fd, MCP23017_GPIO_WORD_REG, regval) < 0){
        logmsg(LOG_ERR, "Error: Failed setting GPIO output state: %s\n", strerror(errno));
        return -1;
    }

    return regval;

}

int MCP23017BitRead(int i2c_fd, uint8_t bit){
    uint16_t regval;
    if ((regval = i2c_smbus_read_word_data(i2c_fd, MCP23017_GPIO_WORD_REG)) < 0){
        logmsg(LOG_ERR, "Error: Failed to read bit %d: %s\n", bit, strerror(errno));
        return regval;
    }
    return ((regval >> bit) & 0x1);
}

int MCP23017BitSetMask(int i2c_fd, uint16_t mask){
    uint16_t regval;

    if ((regval = i2c_smbus_read_word_data(i2c_fd, MCP23017_GPIO_WORD_REG)) < 0){
        logmsg(LOG_ERR, "Error: Failed reading current GPIO output state: %s\n", strerror(errno));
        return regval;
    }

    regval |= mask;

    if (i2c_smbus_write_word_data(i2c_fd, MCP23017_GPIO_WORD_REG, regval) < 0){
        logmsg(LOG_ERR, "Error: Failed setting GPIO output state: %s\n", strerror(errno));
        return -1;
    }
    return regval;
}
int MCP23017BitClearMask(int i2c_fd, uint16_t mask){
    uint16_t regval;

    if ((regval = i2c_smbus_read_word_data(i2c_fd, MCP23017_GPIO_WORD_REG)) < 0){
        logmsg(LOG_ERR, "Error: Failed reading current GPIO output state: %s\n", strerror(errno));
        return regval;
    }

    regval &= ~mask;

    if (i2c_smbus_write_word_data(i2c_fd, MCP23017_GPIO_WORD_REG, regval) < 0){
        logmsg(LOG_ERR, "Error: Failed setting GPIO output state: %s\n", strerror(errno));
        return -1;
    }
    return regval;
}

void MCP23017BitReset(int i2c_fd){
    // Reset GPIOA/GPIOB outputs
    if (i2c_smbus_write_word_data(i2c_fd, MCP23017_GPIO_WORD_REG, 0x0000) < 0){
        logmsg(LOG_ERR, "Error: Failed resetting GPIO output: %s\n", strerror(errno));
        exit(EXIT_FAILURE);
    }
}
