# DRAW YOUR THINGS (login required)
#### Video Demo:  <https://youtu.be/Gpu8sGA3cHg>
#### Description:
A simple whiteboard(login required) build with Flask, Twilio Sync and CS50 Library, allow users to draw or write on the website.

1. Users have to register for the program.
2. Users may change their passwords.
3. Users can draw or write anything they want on this whiteboard.

#### Why whiteboard?

I want to create a space that users can draw or write anything. The most important thing is that users have to register and log in so that they can keep their paintings safe.

Just draw and write whatever you like!!


## Installation

Python version is 3.8.5.
Use SQLite3 to build the database. (Stores the users' passwords)
Other small libraries or packages.

Clone the repo and build the environment:
```
$ git clone https://github.com/ken1009us/draw

git clone [url]: Clone (download) a repository that already exists on GitHub,
including all of the files, branches & commits.

$ cd draw
$ python3 -m venv venv  # use "python -m venv venv" on Windows
$ . venv/bin/activate  # use "venv\Scripts\activate" on Windows
(venv) $ pip install -r requirements.txt
```

The git clone command is used to create a copy of a specific repository or branch within a repository. Git is a distributed version control system. Maximize the advantages of a full repository on your own machine by cloning. (Github - Git Guides)

virtualenv (venv) is used to manage Python packages for different projects. Using virtualenv allows you to avoid installing Python packages globally which could break system tools or other projects. Make sure to activate virtualenv.

People generate and share requirements.txt files to make it easier for other developers to install the correct versions of the required Python libraries (or “packages”) to run the Python code we've written.

Make sure to rename the `.env.example` to `.env`, and fill the variables in it.
(You will need to register a free [Twilio account](http://www.twilio.com/referral/w6qBg0)).

example:

```
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_SYNC_SERVICE_SID=
TWILIO_API_KEY=
TWILIO_API_SECRET=
```

## Execution

Run the application with:
```
(venv) $ flask run
```

Then you can open http://localhost:5000 to check the program.

Now we are ready to go!

After logging in, the interface will be redirected to the main page, then Users can press their cursor to start drawing or writing.

As for the buttons in the upper right corner, they provide the functions of changing users' passwords and logging out.

After changing the password, make sure to re-login to check your password.

## Possible improvements

As all applications this one can also be improved. Possible improvements:

- Allow users to save their paintings.
- Add the button for changing the size of the pen.
- Add more account details.
- Have a way for users to upload pictures to draw.
- Have a way for users to download the paintings they drew.

The above is the simple project I completed by myself after taking a series of online classes.
