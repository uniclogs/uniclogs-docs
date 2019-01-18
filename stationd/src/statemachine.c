#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <ctype.h>
#include <signal.h>
#include <errno.h>

#include "common.h"
#include "statemachine.h"
#include "mcp23017.h"

const char *inputTokens[] = {
    "NO_ACTION",
    "V_TX",
    "U_TX",
    "L_TX",
    "PWR_ON",
    "OPERATE",
    "S_ON",
    "S_OFF",
    "KILL",

    "V_LEFT",
    "V_RIGHT",
    "V_TX_ON",
    "V_TX_OFF",
    "SHUTDOWN",

    "U_LEFT",
    "U_RIGHT",
    "U_TX_ON",
    "U_TX_OFF",

    "L_TX_ON",
    "L_TX_OFF",

    "EXIT",
    "STATUS",
    "MAX_TOKENS"
};

const char *states[] = {
    "INIT",
    "SYS_PWR_ON",
    "STANDBY",
    "S_SYS_ON",
    "S_SYS_OFF",

    "V_TRAN",
    "U_TRAN",
    "L_TRAN"
} pwr_state;

const char *secstates[] = {
    "NONE",
    "VHF_TRANSMIT",
    "V_SWITCH",
    "V_SHUTDOWN",
    "V_PA_COOL",
    "V_PA_DOWN",
    "V_UHF_LHCP",
    "V_UHF_RHCP",
    "V_TRANS_ON",
    "V_TRANS_OFF",
    "V_LHCP",
    "V_RHCP",

    "UHF_TRANSMIT",
    "U_SWITCH",
    "U_SHUTDOWN",
    "U_PA_COOL",
    "U_PA_DOWN",
    "U_VHF_LHCP",
    "U_VHF_RHCP",
    "U_TRANS_ON",
    "U_TRANS_OFF",
    "U_LHCP",
    "U_RHCP",

    "L_TRANSMIT",
    "L_SWITCH",
    "L_SHUTDOWN",
    "L_PA_COOL",
    "L_PA_DOWN",
    "L_VHF_LHCP",
    "L_VHF_RHCP",
    "L_TRANS_ON",
    "L_TRANS_OFF",
    "L_UHF_LHCP",
    "L_UHF_RHCP"
}
//I2C bus
static char *i2c_dev = DEFAULT_I2C_DEV;
static int i2c_fd;


/*
   Overview
   ---------
   The code is checks for input token in a loop using getInput().The token is validated in processToken().
   If the token is good, approriate nextstate is stored in pwr_Config and changeState() is called.
*/

void *statemachine(void *argp){
    logmsg (LOG_INFO,"Starting State Machine...\n");
    init_statemachine();
    //define signals that will be handled.
    signal(SIGALRM, handle_alarm_signal);  //The 2 minute cooldown counter creates this signal.

    while(1){
        // Default token to NO_ACTION
        pwrConfig.token = NO_ACTION;

        getInput();

        if(pwrConfig.token == NO_ACTION){
            continue;
        }

        if(pwrConfig.token == EXIT){
            break;
        }

        if(pwrConfig.token == STATUS){
            logmsg(LOG_NOTICE, "State: %d\n", pwrConfig.state);
            logmsg(LOG_NOTICE, "Secondary state: %d\n", pwrConfig.sec_state);
            logmsg(LOG_NOTICE, "Next State: %d\n", pwrConfig.next_state);
            logmsg(LOG_NOTICE, "Next Secondary state: %d\n", pwrConfig.next_sec_state);
            continue;
        }

        processToken();

        if (pwrConfig.token != NO_ACTION)
            changeState();
    }

    raise(SIGTERM);
    return 0;
}

void handle_alarm_signal(int sig){
    if (pwrConfig.state == SYS_PWR_ON){
        pwrConfig.state = STANDBY;
        pwrConfig.sec_state = NONE;
    }
    else if (pwrConfig.state == V_TRAN && pwrConfig.sec_state == V_PA_COOL){
        pwrConfig.sec_state = V_PA_DOWN;
        MCP23017BitClear(i2c_fd, V_PA);
        MCP23017BitClear(i2c_fd, V_KEY);
        pwrConfig.state = STANDBY;
        pwrConfig.sec_state = NONE;
    }
    else if (pwrConfig.state == U_TRAN && pwrConfig.sec_state == U_PA_COOL){
        pwrConfig.sec_state = U_PA_DOWN;
        MCP23017BitClear(i2c_fd, U_PA);
        MCP23017BitClear(i2c_fd, U_KEY);
        pwrConfig.state = STANDBY;
        pwrConfig.sec_state = NONE;
    }
    else if (pwrConfig.state == L_TRAN && pwrConfig.sec_state == L_PA_COOL){
        pwrConfig.sec_state = L_PA_DOWN;
        MCP23017BitClear(i2c_fd, L_PA);
        pwrConfig.state = STANDBY;
        pwrConfig.sec_state = NONE;
    }
    else
        stateWarning();
}


int init_statemachine(void){
    // Set initial state machine states
    pwrConfig.state = INIT;
    pwrConfig.sec_state = NONE;

    // Open the I2C device for read/write
    if ((i2c_fd = open(i2c_dev, O_RDWR)) < 0){
        logmsg(LOG_ERR,"Error: Failed to open i2c device \'%s\': %s\n", i2c_dev, strerror(errno));
        exit(EXIT_FAILURE);
    }

    // Initialize I2C devices
    MCP23017Init(i2c_fd);
}


//Handles proper exit after a crash or user EXIT token
void i2c_exit(void){
    MCP23017BitReset(i2c_fd);

    if (close(i2c_fd) < 0){
        logmsg(LOG_ERR,"Error: Failed to close I2C device: %s\n", strerror(errno));
    }
}


//Get user token and validate with list of input tokens.
int getInput(void){
    int i;

    sem_wait(&msgpending);
    for(i=0;i<MAX_TOKENS;i++){
        if(!strcmp(msg, inputTokens[i])){
            pwrConfig.token = i;
            logmsg (LOG_INFO,"Token entered %s\n",inputTokens[i]);
            break;
        }
    }
    sem_post(&msgpending);
    sleep(1);

    if(i == MAX_TOKENS) {
        logmsg (LOG_WARNING,"Not a known token. No action taken.\n");
    }

}


int processToken(void){

    if(pwrConfig.token == KILL){
        pwrConfig.next_state = INIT;
        pwrConfig.next_sec_state =  NONE;
        return 0;
    }

    switch(pwrConfig.state){
        case INIT:
            if(pwrConfig.token == PWR_ON)
                pwrConfig.next_state = SYS_PWR_ON;
            else
                tokenError();
            break;
        case SYS_PWR_ON:
            if(pwrConfig.token == OPERATE)
                pwrConfig.next_state = STANDBY;
            else
                tokenError();
            break;
        case STANDBY:
            if(pwrConfig.token == S_ON)
                pwrConfig.next_state = S_SYS_ON;
            else if(pwrConfig.token == S_OFF)
                pwrConfig.next_state = S_SYS_OFF;
            else if(pwrConfig.token == V_TX){
                pwrConfig.next_state = V_TRAN;
                pwrConfig.next_sec_state = VHF_TRANSMIT;
            }
            else if(pwrConfig.token == U_TX){
                pwrConfig.next_state = U_TRAN;
                pwrConfig.next_sec_state = UHF_TRANSMIT;
            }
            else if(pwrConfig.token == L_TX){
                pwrConfig.next_state = L_TRAN;
                pwrConfig.next_sec_state = L_TRANSMIT;
            }
            else
                tokenError();
            break;
        case S_SYS_ON:
            BandSwitchErrorRecovery();
            break;

        case S_SYS_OFF:
            BandSwitchErrorRecovery();
            break;

        case V_TRAN:
            processVHFTokens();
            break;

        case U_TRAN:
            processUHFTokens();
            break;

        case L_TRAN:
            processLBandTokens();
            break;

        default:
            tokenError();
            break;
    }
}


int processVHFTokens(void){
    switch(pwrConfig.sec_state){
        case VHF_TRANSMIT:
        case V_SWITCH:
            if(pwrConfig.token == V_LEFT)
                pwrConfig.next_sec_state =  V_LHCP;
            else if(pwrConfig.token == V_RIGHT)
                pwrConfig.next_sec_state =  V_RHCP;
            else if(pwrConfig.token == V_TX_ON)
                pwrConfig.next_sec_state =  V_TRANS_ON;
            else if(pwrConfig.token == V_TX_OFF)
                pwrConfig.next_sec_state =  V_TRANS_OFF;
            else if(pwrConfig.token == U_RIGHT)
                pwrConfig.next_sec_state =  V_UHF_RHCP;
            else if(pwrConfig.token == U_LEFT)
                pwrConfig.next_sec_state =  V_UHF_LHCP;
            else if(pwrConfig.token == SHUTDOWN)
                pwrConfig.next_sec_state =  V_SHUTDOWN;
            else
                tokenError();
            break;
        case V_LHCP:
        case V_RHCP:
        case V_UHF_RHCP:
        case V_UHF_LHCP:
        case V_PA_DOWN:
        case V_TRANS_ON:
        case V_TRANS_OFF:
            VHFErrorRecovery();
            break;
        case V_SHUTDOWN:
        case V_PA_COOL:
            CoolDown_Wait();
            break;
        default:
            tokenError();
            break;
    }
}


int processUHFTokens(void){
    switch(pwrConfig.sec_state){
        case UHF_TRANSMIT:
        case U_SWITCH:
            if(pwrConfig.token == U_LEFT)
                pwrConfig.next_sec_state =  U_LHCP;
            else if(pwrConfig.token == U_RIGHT)
                pwrConfig.next_sec_state =  U_RHCP;
            else if(pwrConfig.token == U_TX_ON)
                pwrConfig.next_sec_state =  U_TRANS_ON;
            else if(pwrConfig.token == U_TX_OFF)
                pwrConfig.next_sec_state =  U_TRANS_OFF;
            else if(pwrConfig.token == V_RIGHT)
                pwrConfig.next_sec_state =  U_VHF_RHCP;
            else if(pwrConfig.token == V_LEFT)
                pwrConfig.next_sec_state =  U_VHF_LHCP;
            else if(pwrConfig.token == SHUTDOWN)
                pwrConfig.next_sec_state =  U_SHUTDOWN;
            else
                tokenError();
            break;
        case U_LHCP:
        case U_RHCP:
        case U_VHF_RHCP:
        case U_VHF_LHCP:
        case U_PA_DOWN:
        case U_TRANS_ON:
        case U_TRANS_OFF:
            UHFErrorRecovery();
            break;
        case U_SHUTDOWN:
        case U_PA_COOL:
            CoolDown_Wait();
            break;
        default:
            tokenError();
            break;
    }
}


int processLBandTokens(void){
    switch(pwrConfig.sec_state){
        case L_TRANSMIT:
        case L_SWITCH:
            if(pwrConfig.token == U_LEFT)
                pwrConfig.next_sec_state =  L_UHF_LHCP;
            else if(pwrConfig.token == U_RIGHT)
                pwrConfig.next_sec_state =  L_UHF_RHCP;
            else if(pwrConfig.token == L_TX_ON)
                pwrConfig.next_sec_state =  L_TRANS_ON;
            else if(pwrConfig.token == L_TX_OFF)
                pwrConfig.next_sec_state =  L_TRANS_OFF;
            else if(pwrConfig.token == V_RIGHT)
                pwrConfig.next_sec_state =  L_VHF_RHCP;
            else if(pwrConfig.token == V_LEFT)
                pwrConfig.next_sec_state =  L_VHF_LHCP;
            else if(pwrConfig.token == SHUTDOWN)
                pwrConfig.next_sec_state =  L_SHUTDOWN;
            else
                tokenError();
            break;
        case L_VHF_LHCP:
        case L_VHF_RHCP:
        case L_UHF_RHCP:
        case L_UHF_LHCP:
        case L_PA_DOWN:
        case L_TRANS_ON:
        case L_TRANS_OFF:
            LErrorRecovery();
            break;
        case L_SHUTDOWN:
        case L_PA_COOL:
            CoolDown_Wait();
            break;
        default:
            tokenError();
            break;
    }
}



int BandSwitchErrorRecovery(void){
    logmsg(LOG_WARNING,"The system should not have been in this state. Corrective action taken.");
    logmsg(LOG_WARNING,"Please reenter your token and manually validate the action.");
    pwrConfig.next_state = STANDBY;
}


int tokenError(void){
    logmsg (LOG_WARNING,"Token not valid for the state. Please refer to state diagram. No action taken.");
    pwrConfig.token = NO_ACTION;
}

int VHFErrorRecovery(void){
    logmsg(LOG_WARNING,"The system should not have been in this state. Corrective action taken \n");
    logmsg(LOG_WARNING,"Please reenter your token and manually validate the action. \n");
    pwrConfig.next_state = V_SWITCH;
}

int UHFErrorRecovery(void){
    logmsg(LOG_WARNING,"The system should not have been in this state. Corrective action taken \n");
    logmsg(LOG_WARNING,"Please reenter your token and manually validate the action. \n");
    pwrConfig.next_state = U_SWITCH;
}

int LErrorRecovery(void){
    logmsg(LOG_WARNING,"The system should not have been in this state. Corrective action taken \n");
    logmsg(LOG_WARNING,"Please reenter your token and manually validate the action. \n");
    pwrConfig.next_state = L_SWITCH;
}

void stateError(void){
    logmsg(LOG_ERR,"ERROR: There is a program error. Contact coder. \n");
    logmsg(LOG_ERR,"Results unpredictable. Please Kill and start over. \n");
}

void stateWarning(void){
    logmsg(LOG_WARNING,"The system should not have been in this state. KILL token likely entered before.");
}


int CoolDown_Wait(void){
    logmsg(LOG_WARNING,"Waiting for cooldown.No action taken.If required, force exit via KILL or EXIT tokens. \n");
    pwrConfig.token = NO_ACTION;
}


int changeState(void){
    uint8_t temporary;

    switch(pwrConfig.next_state){
        case INIT:
            MCP23017BitReset(i2c_fd);
            pwrConfig.state = INIT;
            pwrConfig.sec_state = NONE;
            break;
        case SYS_PWR_ON:
            MCP23017BitSet(i2c_fd, SDR_ROCK);
            MCP23017BitSet(i2c_fd, SDR_LIME);
            MCP23017BitSet(i2c_fd, ROT_PWR);
            pwrConfig.state = SYS_PWR_ON;
            alarm(60);
            break;
        case STANDBY:
            pwrConfig.state = STANDBY;
            break;
        case S_SYS_ON:
            MCP23017BitSet(i2c_fd, S_PWR);
            pwrConfig.state = STANDBY;
            break;
        case S_SYS_OFF:
            MCP23017BitClear(i2c_fd, S_PWR);
            pwrConfig.state = STANDBY;
            break;

        case V_TRAN:
            pwrConfig.state = V_TRAN;
            switch(pwrConfig.next_sec_state){
                case VHF_TRANSMIT:
                    MCP23017BitSet(i2c_fd, U_LNA);
                    MCP23017BitSet(i2c_fd, V_PA);
                    MCP23017BitSet(i2c_fd, V_KEY);
                    pwrConfig.sec_state = V_SWITCH;
                    break;
                case V_SWITCH:
                    break;
                case V_SHUTDOWN:
                    MCP23017BitClear(i2c_fd, U_LNA);
                    MCP23017BitClear(i2c_fd, U_POL);
                    MCP23017BitClear(i2c_fd, V_POL);
                    MCP23017BitClear(i2c_fd, V_PTT);
                    pwrConfig.sec_state = V_SHUTDOWN;

                    pwrConfig.sec_state = V_PA_COOL;
                    alarm(120);
                    break;
                case V_PA_COOL:
                case V_PA_DOWN:
                    break;
                case V_UHF_LHCP:
                    MCP23017BitSet(i2c_fd, U_POL);
                    pwrConfig.sec_state = V_SWITCH;
                    break;
                case V_UHF_RHCP:
                    MCP23017BitClear(i2c_fd, U_POL);
                    pwrConfig.sec_state = V_SWITCH;
                    break;
                case V_TRANS_ON:
                    MCP23017BitSet(i2c_fd, V_PTT);
                    pwrConfig.sec_state = V_SWITCH;
                    break;
                case V_TRANS_OFF:
                    MCP23017BitClear(i2c_fd, V_PTT);
                    pwrConfig.sec_state = V_SWITCH;
                    break;
                case V_LHCP:
                    temporary = MCP23017BitRead(i2c_fd, V_PTT);
                    MCP23017BitClear(i2c_fd, V_PTT);
                    usleep(100);
                    MCP23017BitSet(i2c_fd, V_POL);
                    usleep(100);
                    if(temporary)
                        MCP23017BitSet(i2c_fd, V_PTT);
                    else
                        MCP23017BitClear(i2c_fd, V_PTT);
                    pwrConfig.sec_state = V_SWITCH;
                    break;

                case V_RHCP:
                    temporary = MCP23017BitRead(i2c_fd, V_PTT);
                    MCP23017BitClear(i2c_fd, V_PTT);
                    usleep(100);
                    MCP23017BitClear(i2c_fd, V_POL);
                    usleep(100);
                    if(temporary)
                        MCP23017BitSet(i2c_fd, V_PTT);
                    else
                        MCP23017BitClear(i2c_fd, V_PTT);
                    pwrConfig.sec_state = V_SWITCH;
                    break;
                default:
                    stateError();
                    break;
            }
            break;

        case U_TRAN:
            pwrConfig.state = U_TRAN;
            switch(pwrConfig.next_sec_state){
                case UHF_TRANSMIT:
                    MCP23017BitSet(i2c_fd, V_LNA);
                    MCP23017BitSet(i2c_fd, U_PA);
                    MCP23017BitSet(i2c_fd, U_KEY);
                    pwrConfig.sec_state = U_SWITCH;
                    break;
                case U_SWITCH:
                    break;
                case U_SHUTDOWN:
                    MCP23017BitClear(i2c_fd, V_LNA);
                    MCP23017BitClear(i2c_fd, V_POL);
                    MCP23017BitClear(i2c_fd, U_POL);
                    MCP23017BitClear(i2c_fd, U_PTT);
                    pwrConfig.sec_state = U_SHUTDOWN;

                    pwrConfig.sec_state = U_PA_COOL;
                    alarm(120);
                    break;
                case U_PA_COOL:
                case U_PA_DOWN:
                    break;
                case U_VHF_LHCP:
                    MCP23017BitSet(i2c_fd, V_POL);
                    pwrConfig.sec_state = U_SWITCH;
                    break;
                case U_VHF_RHCP:
                    MCP23017BitClear(i2c_fd, V_POL);
                    pwrConfig.sec_state = U_SWITCH;
                    break;
                case U_TRANS_ON:
                    MCP23017BitSet(i2c_fd, U_PTT);
                    pwrConfig.sec_state = U_SWITCH;
                    break;
                case U_TRANS_OFF:
                    MCP23017BitClear(i2c_fd, U_PTT);
                    pwrConfig.sec_state = U_SWITCH;
                    break;
                case U_LHCP:
                    temporary = MCP23017BitRead(i2c_fd, U_PTT);
                    MCP23017BitClear(i2c_fd, U_PTT);
                    usleep(100);
                    MCP23017BitSet(i2c_fd, U_POL);
                    usleep(100);
                    if(temporary)
                        MCP23017BitSet(i2c_fd, U_PTT);
                    else
                        MCP23017BitClear(i2c_fd, U_PTT);
                    pwrConfig.sec_state = U_SWITCH;
                    break;

                case U_RHCP:
                    temporary = MCP23017BitRead(i2c_fd, U_PTT);
                    MCP23017BitClear(i2c_fd, U_PTT);
                    usleep(100);
                    MCP23017BitClear(i2c_fd, U_POL);
                    usleep(100);
                    if(temporary)
                        MCP23017BitSet(i2c_fd, U_PTT);
                    else
                        MCP23017BitClear(i2c_fd, U_PTT);
                    pwrConfig.sec_state = U_SWITCH;
                    break;
                default:
                    stateError();
                    break;
            }
            break;

        case L_TRAN:
            pwrConfig.state = L_TRAN;
            switch(pwrConfig.next_sec_state){
                case L_TRANSMIT:
                    MCP23017BitSet(i2c_fd, U_LNA);
                    MCP23017BitSet(i2c_fd, V_LNA);
                    MCP23017BitSet(i2c_fd, L_PA);
                    pwrConfig.sec_state = L_SWITCH;
                    break;
                case L_SWITCH:
                    break;
                case L_SHUTDOWN:
                    MCP23017BitClear(i2c_fd, L_PTT);
                    MCP23017BitClear(i2c_fd, U_POL);
                    MCP23017BitClear(i2c_fd, V_POL);
                    MCP23017BitClear(i2c_fd, V_LNA);
                    MCP23017BitClear(i2c_fd, U_LNA);
                    pwrConfig.sec_state = L_SHUTDOWN;

                    pwrConfig.sec_state = L_PA_COOL;
                    alarm(120);
                    break;
                case L_PA_COOL:
                case L_PA_DOWN:
                    break;
                case L_UHF_LHCP:
                    MCP23017BitSet(i2c_fd, U_POL);
                    pwrConfig.sec_state = L_SWITCH;
                    break;
                case L_UHF_RHCP:
                    MCP23017BitClear(i2c_fd, U_POL);
                    pwrConfig.sec_state = L_SWITCH;
                    break;
                case L_TRANS_ON:
                    MCP23017BitSet(i2c_fd, L_PTT);
                    pwrConfig.sec_state = L_SWITCH;
                    break;
                case L_TRANS_OFF:
                    MCP23017BitClear(i2c_fd, L_PTT);
                    pwrConfig.sec_state = L_SWITCH;
                    break;
                case L_VHF_LHCP:
                    MCP23017BitSet(i2c_fd, V_POL);
                    pwrConfig.sec_state = L_SWITCH;
                    break;
                case L_VHF_RHCP:
                    MCP23017BitClear(i2c_fd, V_POL);
                    pwrConfig.sec_state = L_SWITCH;
                    break;
                default:
                    stateError();
                    break;
            }
            break;

        default:
            stateError();
            break;
    }
}
