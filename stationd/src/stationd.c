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

#include "common.h"
#include "statemachine.h" //stationd State machine
#include "server.h"       //stationd Token processing server


bool daemon_flag = false;
bool verbose_flag = false;

void sig_exit(int sig);

int main(int argc, char *argv[]){
    int c;
    char *port = DEFAULT_PORT;
    char *pid_file = DEFAULT_PID_FILE;
    FILE *run_fp = NULL;
    pid_t pid = 0, sid = 0;
    pthread_t statethread, servthread;

    //Register signal handlers
    signal(SIGINT, sig_exit);
    signal(SIGTERM, sig_exit);

    //Initialize message pending condition variable and mutex
    pthread_mutex_init(&msg_mutex, NULL);
    pthread_cond_init(&msg_cond, NULL);

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

    //Open syslog for all logging purposes
    if (verbose_flag){
        setlogmask(LOG_UPTO(LOG_DEBUG));
    } else {
        setlogmask(LOG_UPTO(LOG_NOTICE));
    }
    openlog(argv[0], LOG_PID|LOG_CONS, LOG_DAEMON);

    //Run as daemon if needed
    if (daemon_flag){
        logmsg(LOG_DEBUG, "Starting as daemon...\n");
        //Fork
        if ((pid = fork()) < 0){
            logmsg(LOG_ERR, "Error: Failed to fork!\n");
            exit(EXIT_FAILURE);
        }

        //Parent process exits
        if (pid){
            exit(EXIT_SUCCESS);
        }

        //Child process continues on
        //Log PID
        if ((run_fp = fopen(pid_file, "w+")) == NULL){
            logmsg(LOG_ERR, "Error: Unable to open file %s\n", pid_file);
            exit(EXIT_FAILURE);
        }
        fprintf(run_fp, "%d\n", getpid());
        fflush(run_fp);
        fclose(run_fp);

        //Create new session for process group leader
        if ((sid = setsid()) < 0){
            logmsg(LOG_ERR, "Error: Failed to create new session!\n");
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

    //Create threads
    logmsg(LOG_INFO, "Starting threads...\n");
    pthread_create(&servthread, NULL, udp_serv, port);
    pthread_create(&statethread, NULL, statemachine, NULL);
    pthread_join(servthread, NULL);
    pthread_join(statethread, NULL);

    logmsg(LOG_DEBUG, "Threads terminated.\n");

    sig_exit(SIGTERM);
}

void sig_exit(int sig){
    logmsg(LOG_INFO,"Shutting Down...\n");
    i2c_exit();
    pthread_mutex_destroy(&msg_mutex);
    pthread_cond_destroy(&msg_cond);
    closelog();
    exit(EXIT_SUCCESS);
}
