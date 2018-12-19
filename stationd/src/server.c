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
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <ctype.h>

#include "common.h"
#include "server.h"


void *udp_serv(void *argp)
{
    int sd = -1, status, recvlen;
    struct addrinfo hints, *servinfo, *p;
    struct sockaddr_storage remaddr;
    socklen_t addrlen;

    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_DGRAM;
    hints.ai_flags = AI_PASSIVE;

    logmsg(LOG_INFO, "Starting UDP server on port %s...", (char *)argp);
    if ((status = getaddrinfo(NULL, (char *)argp, &hints, &servinfo))) {
        logmsg(LOG_ERR, "getaddrinfo error: %s", gai_strerror(status));
        exit(EXIT_FAILURE);
    }
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
    if (p == NULL) {
        logmsg(LOG_ERR, "Error: Failed to bind socket");
        exit(EXIT_FAILURE);
    }
    freeaddrinfo(servinfo);
    addrlen = sizeof(remaddr);

    //Start input handling UDP server
    while (1) {
        sem_wait(&msgpending);
        if ((recvlen = recvfrom(sd, msg, MAXMSG - 1, 0, (struct sockaddr *)&remaddr, &addrlen)) < 0)
        {
            logmsg(LOG_ERR, "Error: Receive failure: %s", strerror(errno));
            exit(EXIT_FAILURE);
        }
        if (recvlen > 0) {
            msg[recvlen] = '\0';
            for (int c = 0; msg[c]; c++) {
                msg[c] = toupper(msg[c]);
            }
            logmsg(LOG_DEBUG, "Received %d byte message: \"%s\"", recvlen, msg);
        }
        sem_post(&msgpending);
        sleep(1);
    }

    logmsg(LOG_INFO, "Shutting down UDP server...");
    close(sd);
    pthread_exit(NULL);
}
