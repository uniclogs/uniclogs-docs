/*
 * =====================================================================================
 *
 *       Filename:  server.c
 *
 *    Description:  stationd UDP server implementation
 *
 *        Version:  0.1.0
 *        Created:  10/25/2018 03:15:54 PM
 *       Compiler:  gcc
 *
 *         Author:  Miles Simpson (heliochronix), miles.a.simpson@gmail.com
 *   Organization:  PSAS
 *
 * =====================================================================================
 */

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <pthread.h>
#include <signal.h>
#include <time.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <ctype.h>

#include "common.h"
#include "server.h"
#include "statemachine.h"

// I2C device and file descriptor
char *i2c_dev = DEFAULT_I2C_DEV;
int i2c_fd;

// UDP messages buffers
char cmd[MAXMSG];
char sendbuf[MAXMSG];

// Support function prototypes
void *get_in_addr(struct sockaddr *sa);
int start_udp_serv(const char *port);

// UDP Server Thread
void *udp_serv(void *argp) {
    int sd, cmdlen, sendlen;
    struct sockaddr_storage remaddr;
    socklen_t addrlen = sizeof(remaddr);
    char srcaddrstr[INET6_ADDRSTRLEN];

    // Register alarm signal handler
    signal(SIGALRM, handle_alarm_signal);

    // Initialize the I2C subsystem state machine
    logmsg (LOG_INFO,"Initializing I2C State Machine...\n");
    init_statemachine();

    // Start the UDP server
    logmsg(LOG_INFO, "Starting UDP server on port %s...\n", (char *)argp);
    sd = start_udp_serv((char *)argp);
    logmsg(LOG_DEBUG, "Started UDP server. Ready to receive messages\n");

    // Begin message processing loop
    while (1) {
        // Wait for a new message to be received
        logmsg(LOG_DEBUG, "UDP Server awaiting message...\n");
        if ((cmdlen = recvfrom(sd, cmd, MAXMSG - 1, 0, (struct sockaddr *)&remaddr, &addrlen)) < 0) {
            logmsg(LOG_ERR, "Error: Receive failure: %s", strerror(errno));
            exit(EXIT_FAILURE);
        }

        // Verify a message was received and process it
        if (cmdlen > 0) {
            // Format the received message
            // First NULL terminate the message to make it a valid C string
            cmd[cmdlen] = '\0';
            // Then strip any trailing newlines
            cmd[strcspn(cmd, "\n")] = '\0';
            // Convert the string to upper case
            for (int c = 0; cmd[c]; c++) {
                cmd[c] = toupper(cmd[c]);
            }
            logmsg(LOG_DEBUG, "Received %d byte message from %s: \"%s\"\n", cmdlen, inet_ntop(remaddr.ss_family, get_in_addr((struct sockaddr *)&remaddr), srcaddrstr, sizeof(srcaddrstr)), cmd);

            // Match to a token if possible
            state_config.token = parse_token(cmd);
            logmsg(LOG_DEBUG, "Token parsed to %s\n", inputTokens[state_config.token]);

            // If it was an invalid token, the token value will be MAX_TOKENS
            // Disregard and wait for a new token
            if (state_config.token == MAX_TOKENS) {
                sprintf(sendbuf, "INVALID\n");
                if ((sendlen = sendto(sd, sendbuf, strlen(sendbuf), 0, (struct sockaddr *)&remaddr, addrlen)) < 0) {
                    logmsg(LOG_ERR, "Error: Send failure: %s", strerror(errno));
                }
                logmsg(LOG_WARNING, "Ignoring unknown token \"%s\"\n", cmd);
                continue;
            }

            // Temperature requests
            if (state_config.token == GETTEMP) {
                sprintf(sendbuf, "TEMP: %fC\n", MCP9808GetTemp(i2c_fd));
                if ((sendlen = sendto(sd, sendbuf, strlen(sendbuf), 0, (struct sockaddr *)&remaddr, addrlen)) < 0) {
                    logmsg(LOG_ERR, "Error: Send failure: %s", strerror(errno));
                }
                logmsg(LOG_INFO, "%s", sendbuf);
                continue;
            }

            // Status requests
            if(state_config.token == STATUS) {
                sprintf(sendbuf, "STATE: %s\nSEC_STATE: %s\nNEXT_STATE: %s\nNEXT_SEC_STATE: %s\nGPIO_STATE: 0x%04X\n", states[state_config.state], secstates[state_config.sec_state], states[state_config.next_state], secstates[state_config.next_sec_state], MCP23017GetState(i2c_fd));
                if ((sendlen = sendto(sd, sendbuf, strlen(sendbuf), 0, (struct sockaddr *)&remaddr, addrlen)) < 0) {
                    logmsg(LOG_ERR, "Error: Send failure: %s", strerror(errno));
                }
                logmsg(LOG_INFO, "%s", sendbuf);
                continue;
            }

            processToken();
            changeState();
        }
    }

    logmsg(LOG_INFO, "Shutting down UDP server...\n");
    close(sd);
    pthread_exit(NULL);
}

void *get_in_addr(struct sockaddr *sa) {
    if (sa->sa_family == AF_INET) {
        return &(((struct sockaddr_in*)sa)->sin_addr);
    }

    return &(((struct sockaddr_in6*)sa)->sin6_addr);
}

int start_udp_serv(const char *port) {
    int sd = -1, ret;
    struct addrinfo hints, *servinfo, *p;

    // Initialize hints addrinfo struct
    // This is an IPv4/IPv6 DGRAM (UDP) socket
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_DGRAM;
    hints.ai_flags = AI_PASSIVE;

    // Query addresses to bind with
    if ((ret = getaddrinfo(NULL, port, &hints, &servinfo))) {
        logmsg(LOG_ERR, "getaddrinfo error: %s\n", gai_strerror(ret));
        exit(EXIT_FAILURE);
    }

    // Attempt to create socket and bind with an address
    for (p = servinfo; p != NULL; p = p->ai_next) {
        if ((sd = socket(p->ai_family, p->ai_socktype, p->ai_protocol)) < 0) {
            logmsg(LOG_ERR, "Error: Cannot create socket: %s", strerror(errno));
            continue;
        }
        if (bind(sd, p->ai_addr, p->ai_addrlen) < 0) {
            close(sd);
            logmsg(LOG_ERR, "Error: Bind failed: %s", strerror(errno));
            continue;
        }
        break;
    }
    // Fail if we could not bind with an address
    if (p == NULL) {
        logmsg(LOG_ERR, "Error: Failed to bind socket\n");
        exit(EXIT_FAILURE);
    }

    // Release memory used for binding
    freeaddrinfo(servinfo);
    return sd;
}
