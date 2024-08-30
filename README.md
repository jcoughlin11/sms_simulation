# SMS Simulation

`sms_simulation` is a command-line interface (CLI) tool written in Python for 
simulating the generation and sending of an arbitrary number of sms messages.

## Requirements

* Python >= 3.12
* Ubuntu 24.04

NOTE: Any Python 3.x.x should work, though some of the type annotations may not be 
available in earlier versions of Python. Additionally, I do not have a Windows or Mac 
machine to test on, so the code has only been checked on Ubuntu 24.04. Earlier versions 
of Ubuntu (or really any other linux variant) should work.

## Installation

It is strongly recommended that you install `sms_simulation` in a virtual environment
so as to avoid creating or running into any conflicts with existing packages on your
system. As such, the instructions below contain steps on how to do that. If you do not 
want to use a virtual environment, simply omit those steps.


### Linux
NOTE: I'm not positive, but I believe that these instructions should work on MacOS, too.

```bash
git clone https://github.com/jcoughlin11/sms_simulation
cd sms_simulation/
mkdir -p ~/.venvs 
python3 -m venv ~/.venvs/sms_simulation 
source ~/.venvs/sms_simulation/bin/activate
python3 -m pip install .
```


### Windows

NOTE: These instructions assume that you're using [git bash](https://git-scm.com/download/win).

```bash
git clone https://github.com/jcoughlin11/sms_simulation
cd sms_simulation/
mkdir -p ~/.venvs 
python -m venv ~/.venvs/sms_simulation 
source ~/.venvs/sms_simulation/Scripts/activate
python -m pip install .
```

NOTE: If you're using Windows and Git Bash, you may encounter issues with the way the 
progress display updates.


## Usage
Installing the package as described above makes available a command-line utility called
`sms_simulation` that you can run from your terminal. It is invoked via:

```bash
sms_simulation [-h] [-n NMESSAGES] [-s NSENDERS] [-t [TIMETOSEND ...]] [-f [SENDFAILURERATE ...]] [-p PROGUPDATETIME]
```

The available options are:

* -h, --help : Show the help message and exit

* -n NMESSAGES, --n-messages NMESSAGES : The number of SMS messages to send. If not specified, a default value of 1000 is used.

* -s NSENDERS, --n-senders NSENDERS : The number of processes to use for sending messages. If not specified, a default value of 1 is used.

* -t [TIMETOSEND ...], --time-to-send [TIMETOSEND ...] : Each sender process takes a certain amount of time to physically send the message. That time is drawn from a normal distribution with standard deviation = 0.1 seconds and mean given by the value of this option (in seconds). This option can be specified multiple times, once for each sender instance. If fewer values of this option are given than there are senders, the default value will be used for the remaining senders. If more values of this option are specified than there are senders, only the first `nSenders` values will be used. The default value is 0.1 second.

* -f [SENDFAILURERATE ...], --failure-rate [SENDFAILURERATE ...] : Specifies the probability, drawn from a uniform distribution, that a sender will fail to send any given sms. This option can be specified multiple times, once for each sender instance. If fewer values of this option are given than there are senders, the default value will be used for the remaining senders. If more values of this option are specified than there are senders, only the first `nSenders` values will be used. The default value is 0.1.

* -p PROGUPDATETIME, --prog-update-time PROGUPDATETIME : The time, in seconds, between progress refreshes. The default value is 1 second.


For example, to send 100 messages using 5 senders, where the first two senders have a 
mean send time of 3 and 4 seconds respectively, the first sender has a failure rate of 
0.6, and the progress updates ever 0.1 second, you would run:

```bash
sms_simulation -n 100 -s 5 -t 3 4 -f 0.6 -p 0.1
```

The third, fourth, and fifth senders would have a mean send time of 0.1 second 
(the default value). The second, third, fourth, and fifth senders would have a failure 
rate of 0.1 (the default value).


## Testing
If you want to run the unit tests for this package, the easist way to do that is to 
install [poetry](https://python-poetry.org/docs/#installing-with-the-official-installer).

From the root of the repository, you can run

```bash
poetry install --with dev 
```

to install the development dependencies alongside the package. You should then just
be able to run 

```bash
poetry run pytest
```

The tests should take less than 1 minute to run.
