#ifndef _MCP23017_H_
#define _MCP23017_H_

#include <stdint.h>
#include "common.h"

// Register values for MCP23017 (IOCON.BANK = 0)
#define MCP23017_IODIR_WORD_REG     0x00
#define MCP23017_IODIRA_REG         0x00
#define MCP23017_IODIRB_REG         0x01
#define MCP23017_IPOL_WORD_REG      0x02
#define MCP23017_IPOLA_REG          0x02
#define MCP23017_IPOLB_REG          0x03
#define MCP23017_GPINTEN_WORD_REG   0x04
#define MCP23017_GPINTENA_REG       0x04
#define MCP23017_GPINTENB_REG       0x05
#define MCP23017_DEFVAL_WORD_REG    0x06
#define MCP23017_DEFVALA_REG        0x06
#define MCP23017_DEFVALB_REG        0x07
#define MCP23017_INTCON_WORD_REG    0x08
#define MCP23017_INTCONA_REG        0x08
#define MCP23017_INTCONB_REG        0x09
#define MCP23017_IOCON_REG          0x0A
#define MCP23017_GPPU_WORD_REG      0x0C
#define MCP23017_GPPUA_REG          0x0C
#define MCP23017_GPPUB_REG          0x0D
#define MCP23017_INTF_WORD_REG      0x0E
#define MCP23017_INTFA_REG          0x0E
#define MCP23017_INTFB_REG          0x0F
#define MCP23017_INTCAP_WORD_REG    0x10
#define MCP23017_INTCAPA_REG        0x10
#define MCP23017_INTCAPB_REG        0x11
#define MCP23017_GPIO_WORD_REG      0x12
#define MCP23017_GPIOA_REG          0x12
#define MCP23017_GPIOB_REG          0x13
#define MCP23017_OLAT_WORD_REG      0x14
#define MCP23017_OLATA_REG          0x14
#define MCP23017_OLATB_REG          0x15

void MCP23017Init(int i2c_fd);

uint16_t MPC23017BitSet(int i2c_fd, uint8_t bit);
uint16_t MPC23017BitClear(int i2c_fd, uint8_t bit);
uint16_t MPC23017BitRead(int i2c_fd, uint8_t bit);
void MPC23017BitReset(int i2c_fd);

#endif
