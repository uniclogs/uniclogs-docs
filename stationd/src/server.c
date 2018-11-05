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

#include "server.h"

#define MAXBUF 2048
#define PORT "8080"

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

    if ((status = getaddrinfo(NULL, PORT, &hints, &servinfo))) {
        fprintf(stderr, "getaddrinfo error: %s\n", gai_strerror(status));
        exit(EXIT_FAILURE);
    }
    for (p = servinfo; p != NULL; p = p->ai_next)
    {
        if ((sd = socket(p->ai_family, p->ai_socktype, p->ai_protocol)) < 0) {
            perror("Error: Cannot create socket\n");
            continue;
        }
        if (bind(sd, p->ai_addr, p->ai_addrlen) < 0) {
            close(sd);
            perror("Error: Bind failed\n");
            continue;
        }
        break;
    }
    if (p == NULL) {
        fprintf(stderr, "Error: Failed to bind socket\n");
        exit(EXIT_FAILURE);
    }
    freeaddrinfo(servinfo);

    addrlen = sizeof(remaddr);
    while (1) {
        printf("Waiting on port %s...\n", PORT);
        if ((recvlen = recvfrom(sd, buf, MAXBUF - 1, 0, (struct sockaddr *)&remaddr, &addrlen)) < 0)
        {
            perror("Error: Receive failure\n");
            exit(EXIT_FAILURE);
        }
        printf("Received %d bytes\n", recvlen);
        if (recvlen > 0) {
            buf[recvlen] = '\0';
            printf("Received message: \"%s\"\n", buf);
            if (!strncmp("q", buf, MAXBUF)) {
                break;
            }
        }
    }

    close(sd);
    pthread_exit(NULL);
}
