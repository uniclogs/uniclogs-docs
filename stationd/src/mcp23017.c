#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <linux/i2c.h>
#include "common.h"
#include "mcp23017.h"

void MCP23017SetSlave(int i2c_fd){
    logmsg(LOG_DEBUG, "Setting MCP23017 as Slave...\n");
    // Set MCP23017 as slave device
    if (ioctl(i2c_fd, I2C_SLAVE, MCP23017_I2C_ADDR) < 0){
        logmsg(LOG_ERR, "Error: Failed setting MCP23017 as slave: %s\n", strerror(errno));
        exit(EXIT_FAILURE);
    }
}

void MCP23017Init(int i2c_fd){
    logmsg(LOG_DEBUG, "Initializing MCP23017...\n");
    MCP23017SetSlave(i2c_fd);

    // Configure GPIOA and GPIOB as output (IODIR = 0x00)
    logmsg(LOG_DEBUG, "Configuring outputs...\n");
    if (i2c_smbus_write_word_data(i2c_fd, MCP23017_IODIR_WORD_REG, 0x0000) < 0){
        logmsg(LOG_ERR, "Error: Failed setting GPIO as output: %s\n", strerror(errno));
        exit(EXIT_FAILURE);
    }

    // Reset output pins
    MCP23017BitReset(i2c_fd);
    logmsg(LOG_DEBUG, "Initialization Done!\n");
}

int MCP23017BitSet(int i2c_fd, uint8_t bit){
    uint16_t regval;

    logmsg(LOG_DEBUG, "Setting bit %u on MCP23017...\n", bit);
    MCP23017SetSlave(i2c_fd);

    logmsg(LOG_DEBUG, "Reading current value...\n");
    if ((regval = i2c_smbus_read_word_data(i2c_fd, MCP23017_GPIO_WORD_REG)) < 0){
        logmsg(LOG_ERR, "Error: Failed reading current GPIO output state: %s\n", strerror(errno));
        return regval;
    }
    logmsg(LOG_DEBUG, "Read 0x%X...\n", regval);

    regval |= (0x1 << bit);

    logmsg(LOG_DEBUG, "Writing 0x%X...\n", regval);
    if (i2c_smbus_write_word_data(i2c_fd, MCP23017_GPIO_WORD_REG, regval) < 0){
        logmsg(LOG_ERR, "Error: Failed setting GPIO output state: %s\n", strerror(errno));
        return -1;
    }

    logmsg(LOG_DEBUG, "BitSet Done!\n");
    return regval;
}


int MCP23017BitClear(int i2c_fd, uint8_t bit){
    uint16_t regval;

    logmsg(LOG_DEBUG, "Clearing bit %u on MCP23017...\n", bit);
    MCP23017SetSlave(i2c_fd);

    logmsg(LOG_DEBUG, "Reading current value...\n");
    if ((regval = i2c_smbus_read_word_data(i2c_fd, MCP23017_GPIO_WORD_REG)) < 0){
        logmsg(LOG_ERR, "Error: Failed reading current GPIO output state: %s\n", strerror(errno));
        return regval;
    }
    logmsg(LOG_DEBUG, "Read 0x%X...\n", regval);

    regval &= ~(0x1 << bit);

    logmsg(LOG_DEBUG, "Writing 0x%X...\n", regval);
    if (i2c_smbus_write_word_data(i2c_fd, MCP23017_GPIO_WORD_REG, regval) < 0){
        logmsg(LOG_ERR, "Error: Failed setting GPIO output state: %s\n", strerror(errno));
        return -1;
    }

    logmsg(LOG_DEBUG, "BitClear Done!\n");
    return regval;

}

int MCP23017BitRead(int i2c_fd, uint8_t bit){
    uint16_t regval;

    logmsg(LOG_DEBUG, "Reading bit %u on MCP23017...\n", bit);
    MCP23017SetSlave(i2c_fd);

    logmsg(LOG_DEBUG, "Reading register...\n");
    if ((regval = i2c_smbus_read_word_data(i2c_fd, MCP23017_GPIO_WORD_REG)) < 0){
        logmsg(LOG_ERR, "Error: Failed to read bit %d: %s\n", bit, strerror(errno));
        return regval;
    }

    logmsg(LOG_DEBUG, "Read 0x%X\n", regval);
    return ((regval >> bit) & 0x1);
}

int MCP23017BitSetMask(int i2c_fd, uint16_t mask){
    uint16_t regval;

    logmsg(LOG_DEBUG, "Setting bit mask %X on MCP23017...\n", mask);
    MCP23017SetSlave(i2c_fd);

    logmsg(LOG_DEBUG, "Reading current value...\n");
    if ((regval = i2c_smbus_read_word_data(i2c_fd, MCP23017_GPIO_WORD_REG)) < 0){
        logmsg(LOG_ERR, "Error: Failed reading current GPIO output state: %s\n", strerror(errno));
        return regval;
    }
    logmsg(LOG_DEBUG, "Read 0x%X...\n", regval);

    regval |= mask;

    logmsg(LOG_DEBUG, "Writing 0x%X...\n", regval);
    if (i2c_smbus_write_word_data(i2c_fd, MCP23017_GPIO_WORD_REG, regval) < 0){
        logmsg(LOG_ERR, "Error: Failed setting GPIO output state: %s\n", strerror(errno));
        return -1;
    }

    logmsg(LOG_DEBUG, "BitSetMask Done!\n");
    return regval;
}

int MCP23017BitClearMask(int i2c_fd, uint16_t mask){
    uint16_t regval;

    logmsg(LOG_DEBUG, "Clearing bit mask %X on MCP23017...\n", mask);
    MCP23017SetSlave(i2c_fd);

    logmsg(LOG_DEBUG, "Reading current value...\n");
    if ((regval = i2c_smbus_read_word_data(i2c_fd, MCP23017_GPIO_WORD_REG)) < 0){
        logmsg(LOG_ERR, "Error: Failed reading current GPIO output state: %s\n", strerror(errno));
        return regval;
    }
    logmsg(LOG_DEBUG, "Read 0x%X...\n", regval);

    regval &= ~mask;

    logmsg(LOG_DEBUG, "Writing 0x%X...\n", regval);
    if (i2c_smbus_write_word_data(i2c_fd, MCP23017_GPIO_WORD_REG, regval) < 0){
        logmsg(LOG_ERR, "Error: Failed setting GPIO output state: %s\n", strerror(errno));
        return -1;
    }

    logmsg(LOG_DEBUG, "BitClearMask Done!\n");
    return regval;
}

uint16_t MCP23017GetState(int i2c_fd){
    uint16_t regval;

    logmsg(LOG_DEBUG, "Reading state of MCP23017...\n");
    MCP23017SetSlave(i2c_fd);

    logmsg(LOG_DEBUG, "Reading register...\n");
    if ((regval = i2c_smbus_read_word_data(i2c_fd, MCP23017_GPIO_WORD_REG)) < 0){
        logmsg(LOG_ERR, "Error: Failed to read state: %s\n", strerror(errno));
        return regval;
    }

    logmsg(LOG_DEBUG, "Read 0x%X\n", regval);
    return regval;
}

void MCP23017BitReset(int i2c_fd){
    logmsg(LOG_DEBUG, "Resetting MCP23017 bits...\n");
    MCP23017SetSlave(i2c_fd);

    logmsg(LOG_DEBUG, "Writing 0x0000...\n");
    // Reset GPIOA/GPIOB outputs
    if (i2c_smbus_write_word_data(i2c_fd, MCP23017_GPIO_WORD_REG, 0x0000) < 0){
        logmsg(LOG_ERR, "Error: Failed resetting GPIO output: %s\n", strerror(errno));
        exit(EXIT_FAILURE);
    }
    logmsg(LOG_DEBUG, "Reset Complete!\n");
}
