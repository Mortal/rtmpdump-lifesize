# rtmpdump-lifesize
Use rtmpdump to download videos from vc.au.dk (a server running LifeSize UVC Video Center).

You need to check out
[my fork of rtmpdump, branch `ecma_array`](https://github.com/Mortal/rtmpdump)
in the directory where you check out this repository and compile it.

Then, you need to install the Python 3 `requests` module and simply run the
Python 3 script with the URL of the video you wish to download.

The script is depended on some GNU tools that you will have to install before running the script.
These can be installed in the following way:
`sudo apt install libgnutls28-dev`


```
rav@pictoris:~/work$ git clone git://github.com/Mortal/rtmpdump-lifesize.git
Cloning into 'rtmpdump-lifesize'...
...
Receiving objects: 100% (9/9), done.
rav@pictoris:~/work$ cd rtmpdump-lifesize/
rav@pictoris:~/work/rtmpdump-lifesize$ git clone git://github.com/Mortal/rtmpdump.git
Cloning into 'rtmpdump'...
...
Resolving deltas: 100% (1761/1761), done.
rav@pictoris:~/work/rtmpdump-lifesize$ cd rtmpdump/
rav@pictoris:~/work/rtmpdump-lifesize/rtmpdump$ git checkout ecma_array
Branch ecma_array set up to track remote branch ecma_array from origin.
Switched to a new branch 'ecma_array'
rav@pictoris:~/work/rtmpdump-lifesize/rtmpdump$ make
make[1]: Entering directory '/home/rav/work/rtmpdump-lifesize/rtmpdump/librtmp'
...
gcc -Wall  -o rtmpsuck rtmpsuck.o thread.o -lpthread -Llibrtmp -lrtmp -lssl -lcrypto -lz
rav@pictoris:~/work/rtmpdump-lifesize/rtmpdump$ cd ..
rav@pictoris:~/work/rtmpdump-lifesize$ pip3 install --user requests
...
rav@pictoris:~/work/rtmpdump-lifesize$ python3
Python 3.5.2 (default, Jun 28 2016, 08:46:01)
[GCC 6.1.1 20160602] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import requests
>>> exit()
rav@pictoris:~/work/rtmpdump-lifesize$ python3 fetch.py https://vc.au.dk/videos/video/5497/
Playback token is 323272562
RTMPDump v2.4
(c) 2010 Andrej Stepanchuk, Howard Chu, The Flvstreamer Team; license: GPL
Connecting ...
INFO: Connected...
Starting Live Stream
...
```
