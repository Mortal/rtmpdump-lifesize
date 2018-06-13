import re
import argparse
import requests
import subprocess

DOMAINS = ['vc.agrsci.dk', 'vc.au.dk', '130.226.243.18']
domain_regex = '|'.join(re.escape(domain) for domain in DOMAINS)
prefix_regex = '^https?://(?P<domain>%s)' % domain_regex

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--feed',
                        choices='main presentation all'.split())
    parser.add_argument('-u', '--username')
    parser.add_argument('-p', '--password')
    parser.add_argument('url')
    args = parser.parse_args()

    mo = re.match(prefix_regex + r'/videos/video/(?P<id>\d+)/$', args.url)
    if mo is None:
        parser.error("Invalid URL")
    id = int(mo.group('id'))
    domain = mo.group('domain')

    s = requests.Session()
    # Force HTTPS
    response = s.get('https://%s/videos/video/%s/' % (domain, id), verify=False)
    if response.history:
        # We were redirected, so a login is probably needed
        token_pattern = (r"<input type='hidden' name='csrfmiddlewaretoken' " +
                         r"value='([^']+)' />")
        mo = re.search(token_pattern, response.text)
        assert mo is not None
        if not args.username or not args.password:
            parser.error("Login required")
        referer = response.url
        response = s.post(
            response.url,
            data=dict(username=args.username, password=args.password,
                      csrfmiddlewaretoken=mo.group(1)),
            headers=dict(referer=referer))
        assert response.status_code == 200, response.status_code
    response = s.get(
        'https://%s/videos/video/%s/authorize-playback/' % (domain, id), verify=False)
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
        # Note O:2 means "ECMA Array" and requires a patched rtmpdump
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
