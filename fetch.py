import re
import argparse
import requests
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--feed',
                        choices='main presentation all'.split())
    parser.add_argument('url')
    args = parser.parse_args()

    mo = re.match(r'^https://vc.agrsci.dk/videos/video/(\d+)/$', args.url)
    if mo is None:
        parser.error("Invalid URL")
    id = mo.group(1)

    s = requests.Session()
    response = s.get(
        'https://vc.agrsci.dk/videos/video/%s/authorize-playback/' % id)
    o = response.json()
    assert o['status'] == 0
    path1 = o['main_feed']
    path2 = o['pres_feed']
    streamer = o['streamer']
    mo = re.match(r'([^/]+)/(.*)', streamer)
    hostname = mo.group(1)
    streamer_path = mo.group(2)
    token = o['playback_token']
    print("Playback token is %s" % token)

    name = o['video_name']

    cmd1 = [
        'rtmpdump/rtmpdump', '-v', '-r',
        'rtmp://%s:1935' % hostname + '/' + streamer_path + '/' + path1,
        '-a', streamer_path,
        '-t', 'rtmp://%s:1935' % hostname + '/' + streamer_path,
        '-f', 'LNX 11,2,202,569',
        '-C', 'O:2', '-C', 'NN:0:%s' % token, '-C', 'NB:1:0',
        '-y', path1,
        '-o', '%s (main).mp4' % name,
    ]

    cmd2 = [
        'rtmpdump/rtmpdump', '-v', '-r',
        'rtmp://%s:1935' % hostname + '/' + streamer_path + '/' + path2,
        '-a', streamer_path,
        '-t', 'rtmp://%s:1935' % hostname + '/' + streamer_path,
        '-f', 'LNX 11,2,202,569',
        '-C', 'O:2', '-C', 'NN:0:%s' % token, '-C', 'NB:1:0',
        '-y', path2,
        '-o', '%s (presentation).mp4' % name,
    ]

    env = dict(LD_LIBRARY_PATH='rtmpdump/librtmp')
    if args.feed == 'all':
        p1 = subprocess.Popen(cmd1, env=env)
        p2 = subprocess.Popen(cmd2, env=env)
        p1.wait()
        p2.wait()
    elif args.feed == 'presentation':
        subprocess.check_call(cmd2, env=env)
    else:
        subprocess.check_call(cmd1, env=env)


if __name__ == "__main__":
    main()
