# Python Calling Bot
A python script that automates calls in large numbers with custom audio files 🙂. Must be run on a system with [Asterisk](https://www.asterisk.org/) and VOIP fully working. Tested on [Raspberry-Asterisk](http://www.raspberry-asterisk.org/) with [Flowroute](https://www.flowroute.com/). 

# Usage

`python3 caller.py [number]`

```
'--callid', callerid to spoof to
'--prefix', callerid prefix, for sending calls from the same area code
'--file', path to a sound file that plays on pickup
'--folder', path to a folder with soundfiles to be randomly chosen from
'--frequency', sends a call every X seconds
'--numcalls', the total number of calls to send
```
