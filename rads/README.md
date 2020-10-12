# RADS (Request Approve / Deny Service)
Mangages requests to use OreSat live. Allows for modification of a PSQL schedule and allows for an override to reserve a pass for PSAS through a curses GUI. 

# Prerequisite Services:
Services Required to run before can RADS can be used

* PostgreSQL Daemon

# PSQL Table Note
Make to run all sql scripts in uniclogs-software/db_schema to properly create the tables used for RADS


## Dependencies

**Packages**
`loguru`
`sqlalchemy`
`reverse_geocoder`
`pass-calculator`

**Dependencies Install**
`$` `pip install -r requirements.txt`


## Program Installation

**Local Install:**

`$` `pip install uniclogs-rads`

**Global Install**

`$` `sudo pip install uniclogs-rads`


## Run

**Local: (user install)**

`$` `python3 -m rads`

**Global: (global install)**

`$` `rads`

#### Usage
```
Arrow keys to move the highlight selection arround(universal). Enter to use a RADS feature 

***Approve/Deny Request(Incoming requests to use OreSat live that need to be approved or denied)***
'a' is used to accept a request and will automatically deny overlapping incoming requests.
'd' is used to deny a request
'w' is used to reset selected request and their overlaps back to pending.
's' is used to save and update all request changes to PSQL database then quit
'c' is used to quit witout saving request changes to PSQL Database

Green represents a approved request
Red represents a denied request
Yellow represents an overlap in an already approved requests and will prevent the request from being accepted.
Blue reperesents an overlap with an incoming request and will override the color yellow

Requests are ordered by when they were created (First come first serve).


***Check Schedule(A list of all approved requests to use OreSat live and allows for passes to be canceled)***
'a' is used to accept a request
'd' is used to deny an approved upcoming request
's' is used to save and update all request changes to PSQL database then quit
'c' is used to quit witout saving request changes to PSQL Database

Red represents a request that has been changed to denied

Requests are ordered by AOS ASC


***Archive(A history of all requests)***

Reqests are ordered by AOS DESC


***EB passes(Allows for PSAS to reserve a pass for the EB(Engineering Building)***

'a' is used to accept and schedule a uniclogs pass
'd' is used to remove a new uniclogs pass
'f' to switch focus to the other list to scroll through
's' is used to save and update all request changes to PSQL database then quit
'c' is used to quit witout saving request changes to PSQL Database

Left list represents all upcoming passes
Right list represents all approved requests in the database

Green represents an approval for a new eb pass
Yellow represents an overlap when selecting upcoming passes list on the left
Red represents a request is removed
```
