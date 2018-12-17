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
#include <syslog.h>
#include <pthread.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>

#include "server.h"

#define MAXBUF 2048

void *udp_serv(void *argp)
{
    int sd = -1, status, recvlen;
    struct addrinfo hints, *servinfo, *p;
    struct sockaddr_storage remaddr;
    socklen_t addrlen;
    char buf[MAXBUF];

    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_DGRAM;
    hints.ai_flags = AI_PASSIVE;

    if ((status = getaddrinfo(NULL, (char *)argp, &hints, &servinfo))) {
        syslog(LOG_ERR, "getaddrinfo error: %s", gai_strerror(status));
        fprintf(stderr, "getaddrinfo error: %s\n", gai_strerror(status));
        exit(EXIT_FAILURE);
    }
    for (p = servinfo; p != NULL; p = p->ai_next)
    {
        if ((sd = socket(p->ai_family, p->ai_socktype, p->ai_protocol)) < 0) {
            syslog(LOG_ERR, "Error: Cannot create socket: %s", strerror(errno));
            fprintf(stderr, "Error: Cannot create socket: %s\n", strerror(errno));
            continue;
        }
        if (bind(sd, p->ai_addr, p->ai_addrlen) < 0) {
            close(sd);
            syslog(LOG_ERR, "Error: Bind failed: %s", strerror(errno));
            fprintf(stderr, "Error: Bind failed: %s\n", strerror(errno));
            continue;
        }
        break;
    }
    if (p == NULL) {
        syslog(LOG_ERR, "Error: Failed to bind socket");
        fprintf(stderr, "Error: Failed to bind socket\n");
        exit(EXIT_FAILURE);
    }
    freeaddrinfo(servinfo);

    addrlen = sizeof(remaddr);
    syslog(LOG_INFO, "Starting UDP server on port %s...", (char *)argp);
    fprintf(stdout, "Starting UDP server on port %s...\n", (char *)argp);
    while (1) {
        if ((recvlen = recvfrom(sd, buf, MAXBUF - 1, 0, (struct sockaddr *)&remaddr, &addrlen)) < 0)
        {
            syslog(LOG_ERR, "Error: Receive failure: %s", strerror(errno));
            fprintf(stderr, "Error: Receive failure: %s\n", strerror(errno));
            exit(EXIT_FAILURE);
        }
        if (recvlen > 0) {
            buf[recvlen] = '\0';
            syslog(LOG_DEBUG, "Received %d byte message: \"%s\"", recvlen, buf);
            fprintf(stdout, "Received %d byte message: \"%s\"\n", recvlen, buf);
            if (!strncmp("q", buf, MAXBUF)) {
                break;
            }
        }
    }

    close(sd);
    pthread_exit(NULL);
}
