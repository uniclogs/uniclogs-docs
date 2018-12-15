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
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <signal.h>
#include <pthread.h>

#include "statemachine.h" //stationd State machine
#include "server.h"       //stationd Token processing server

#define DEFAULT_PORT "8080"
#define DEFAULT_PID_FILE "/run/stationd/stationd.pid"

static int daemon_flag = 0;

int main(int argc, char *argv[]){
    int c;
    char *port = DEFAULT_PORT;
    char *pid_file = DEFAULT_PID_FILE;
    FILE *run_fp = NULL;
    pid_t pid = 0, sid = 0;
    pthread_t statethread, servthread;

    //Command line argument processing
    while ((c = getopt(argc, argv, "dp:r:")) != -1){
        switch (c){
            case 'd':
                daemon_flag = 1;
                break;
            case 'p':
                port = optarg;
                break;
            case 'r':
                pid_file = optarg;
                break;
            case '?':

            default:
                fprintf(stderr, "Usage: %s [-d] [-p portnum] [-r pid_file]\n", argv[0]);
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

        //Parent process, log pid of child and exit
        if (pid){
            if ((run_fp = fopen(pid_file, "w+")) == NULL){
                fprintf(stderr, "Error: Unable to open file %s\nTerminating...\n", pid_file);
                kill(pid, SIGINT);
                exit(EXIT_FAILURE);
            }
            fprintf(run_fp, "%d\n", pid);
            fflush(run_fp);
            fclose(run_fp);
            exit(EXIT_SUCCESS);
        }

        //Child process, create new session for process group leader
        if ((sid = setsid()) < 0){
            fprintf(stderr, "Error: Failed to create new session! Terminating...\n");
            exit(EXIT_FAILURE);
        }

        umask(0);
        chdir("/");

        //Redirect std streams to /dev/null
        freopen("/dev/null", "r", stdin);
        freopen("/dev/null", "w+", stdout);
        freopen("/dev/null", "w+", stderr);
    }

    /*pthread_create(&servthread, NULL, udp_serv, NULL);*/
    /*pthread_join(servthread, NULL);*/

    return EXIT_SUCCESS;
}
