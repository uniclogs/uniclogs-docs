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

void *get_in_addr(struct sockaddr *sa)
{
    if (sa->sa_family == AF_INET) {
        return &(((struct sockaddr_in*)sa)->sin_addr);
    }

    return &(((struct sockaddr_in6*)sa)->sin6_addr);
}

// UDP Server Thread
void *udp_serv(void *argp)
{
    int sd = -1, status, recvlen, sendlen;
    struct addrinfo hints, *servinfo, *p;
    struct sockaddr_storage remaddr;
    socklen_t addrlen;
    char srcaddrstr[INET6_ADDRSTRLEN];

    // Initialize hints addrinfo struct
    // This is an IPv4/IPv6 DGRAM (UDP) socket
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_DGRAM;
    hints.ai_flags = AI_PASSIVE;

    // Initialize the I2C subsystem
    logmsg (LOG_INFO,"Initializing State Machine...\n");
    init_statemachine();
    // Register alarm signal handler
    signal(SIGALRM, handle_alarm_signal);

    // Start the UDP server
    logmsg(LOG_INFO, "Starting UDP server on port %s...\n", (char *)argp);
    // Query addresses to bind with
    if ((status = getaddrinfo(NULL, (char *)argp, &hints, &servinfo))) {
        logmsg(LOG_ERR, "getaddrinfo error: %s\n", gai_strerror(status));
        exit(EXIT_FAILURE);
    }
    // Attempt to create socket and bind with an address
    for (p = servinfo; p != NULL; p = p->ai_next)
    {
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
    addrlen = sizeof(remaddr);
    logmsg(LOG_DEBUG, "Started UDP server. Ready to receive messages\n");

    //Start input handling UDP server
    while (1) {
        // Wait for a new message to be received
        logmsg(LOG_DEBUG, "UDP Server awaiting message...\n");
        if ((recvlen = recvfrom(sd, msg, MAXMSG - 1, 0, (struct sockaddr *)&remaddr, &addrlen)) < 0){
            logmsg(LOG_ERR, "Error: Receive failure: %s", strerror(errno));
            exit(EXIT_FAILURE);
        }
        // Verify an actual message was received, and if so process it
        if (recvlen > 0) {
            // NULL terminate the message to make it a valid C string
            msg[recvlen] = '\0';
            // Strip any trailing newlines
            msg[strcspn(msg, "\n")] = '\0';
            // Convert the string to upper case
            for (int c = 0; msg[c]; c++) {
                msg[c] = toupper(msg[c]);
            }
            logmsg(LOG_DEBUG, "Received %d byte message from %s: \"%s\"\n", recvlen, inet_ntop(remaddr.ss_family, get_in_addr((struct sockaddr *)&remaddr), srcaddrstr, sizeof(srcaddrstr)), msg);
            state_config.token = parse_token(msg);
            logmsg(LOG_DEBUG, "Token parsed to %s\n", inputTokens[state_config.token]);

            // Process special tokens
            // If it was an invalid token, the token value will be MAX_TOKENS
            if (state_config.token == MAX_TOKENS){
                logmsg(LOG_WARNING, "Ignoring unknown token \"%s\"\n", msg);
                continue;
            }

            // Temperature requests
            if (state_config.token == GETTEMP){
                if ((sendlen = sendto(sd, "test\n", strlen("test\n"), 0, (struct sockaddr *)&remaddr, addrlen)) < 0){
                    logmsg(LOG_ERR, "Error: Send failure: %s", strerror(errno));
                    exit(EXIT_FAILURE);
                }
                logmsg(LOG_NOTICE, "Temperature: %fC\n", MCP9808GetTemp(i2c_fd));
                continue;
            }

            // Status requests
            if(state_config.token == STATUS){
                logmsg(LOG_NOTICE, "State: %s\n", states[state_config.state]);
                logmsg(LOG_NOTICE, "Secondary state: %s\n", secstates[state_config.sec_state]);
                logmsg(LOG_NOTICE, "Next State: %s\n", states[state_config.next_state]);
                logmsg(LOG_NOTICE, "Next Secondary state: %s\n", secstates[state_config.next_sec_state]);
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
