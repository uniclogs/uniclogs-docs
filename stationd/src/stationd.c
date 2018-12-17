/*
 * =====================================================================================
 *
 *       Filename:  stationd.c
 *
 *    Description:  stationd main implementation
 *
 *        Version:  0.1.0
 *        Created:  10/25/2018 12:29:28 PM
 *       Compiler:  gcc
 *
 *         Author:  Miles Simpson (heliochronix), miles.a.simpson@gmail.com
 *   Organization:  PSAS
 *
 * =====================================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <signal.h>
#include <syslog.h>
#include <pthread.h>

#include "statemachine.h" //stationd State machine
#include "server.h"       //stationd Token processing server

#ifndef DEFAULT_PORT
#define DEFAULT_PORT "8080"
#endif
#ifndef DEFAULT_PID_FILE
#define DEFAULT_PID_FILE "/run/stationd/stationd.pid"
#endif

static bool daemon_flag = false;
static int verbose_flag = false;

int main(int argc, char *argv[]){
    int c;
    char *port = DEFAULT_PORT;
    char *pid_file = DEFAULT_PID_FILE;
    FILE *run_fp = NULL;
    pid_t pid = 0, sid = 0;
    pthread_t statethread, servthread;

    //Command line argument processing
    while ((c = getopt(argc, argv, "dp:r:v")) != -1){
        switch (c){
            case 'd':
                daemon_flag = true;
                break;
            case 'p':
                port = optarg;
                break;
            case 'r':
                pid_file = optarg;
                break;
            case 'v':
                verbose_flag = true;
                break;
            case '?':

            default:
                fprintf(stderr, "Usage: %s [-d] [-p portnum] [-r pid_file] [-v]\n", argv[0]);
                exit(1);
        }
    }

    //Run as daemon if needed
    if (daemon_flag){
        //Fork
        if ((pid = fork()) < 0){
            fprintf(stderr, "Error: Failed to fork! Terminating...\n");
            exit(EXIT_FAILURE);
        }

        //Parent process exits
        if (pid){
            exit(EXIT_SUCCESS);
        }

        //Child process continues on
        //Log PID
        if ((run_fp = fopen(pid_file, "w+")) == NULL){
            fprintf(stderr, "Error: Unable to open file %s\nTerminating...\n", pid_file);
            exit(EXIT_FAILURE);
        }
        fprintf(run_fp, "%d\n", getpid());
        fflush(run_fp);
        fclose(run_fp);

        //Create new session for process group leader
        if ((sid = setsid()) < 0){
            fprintf(stderr, "Error: Failed to create new session! Terminating...\n");
            exit(EXIT_FAILURE);
        }

        //Set default umask and cd to root to avoid blocking filesystems
        umask(0);
        chdir("/");

        //Redirect std streams to /dev/null
        freopen("/dev/null", "r", stdin);
        freopen("/dev/null", "w+", stdout);
        freopen("/dev/null", "w+", stderr);
    }

    //Open syslog for all logging purposes
    if (verbose_flag){
        setlogmask(LOG_UPTO(LOG_DEBUG));
    } else {
        setlogmask(LOG_UPTO(LOG_NOTICE));
    }
    openlog(argv[0], LOG_PID|LOG_CONS, LOG_DAEMON);

    //Register signal handlers

    //Create threads
    pthread_create(&servthread, NULL, udp_serv, port);
    pthread_join(servthread, NULL);

    closelog();
    return EXIT_SUCCESS;
}
