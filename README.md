# DRAW YOUR THINGS (login required)
#### Video Demo:  <URL HERE>
#### Description:
A simple whiteboard(login required) build with Flask, Twilio Sync and CS50 Library.
Use SQLite3 to build the database.

## Installation

Clone the repo and build the environment:
```
$ git clone https://github.com/ken1009us/draw
$ cd draw
$ python3 -m venv venv  # use "python -m venv venv" on Windows
$ . venv/bin/activate  # use "venv\Scripts\activate" on Windows
(venv) $ pip install -r requirements.txt
```

Rename the `.env.example` to `.env`, fill the variables in it.
(You will need to register a free [Twilio account](http://www.twilio.com/referral/w6qBg0)).

## Execution

Run the application with:
```
(venv) $ flask run
```

Then you can open http://localhost:5000 to check the program.
