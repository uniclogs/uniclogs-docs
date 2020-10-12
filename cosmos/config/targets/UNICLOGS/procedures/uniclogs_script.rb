# Script Runner test script
cmd("UNICLOGS COMMAND")
wait_check("UNICLOGS STATUS BOOL == 'FALSE'", 5)
