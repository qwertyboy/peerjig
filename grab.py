from gevent.pool import Pool
from gevent.monkey import patch_all
patch_all()
import requests 
import re
import bencode
import urllib
import hashlib

data_dir = "data"
site = "http://libble.me"
torrent_pass = "6qfuh4gv7fnp73pgzl5per3286v7u13s"
auth_key = "808e87d2cb7ecc453946ac85ecc2b2cf"

def get_session(user, pwd):
    session = requests.Session() 
    res = session.post("%s/login.php" % site, data={'username': user, 'password': pwd}, verify=False)
    print res.text
    if "logout" in res.text.lower():
        return session
    
def get_data(session, torrent_ids):

    def get_peers(torrent_file):
        t = bencode.bdecode(open(torrent_file, 'rb').read())
        announce = t['announce']
        info =  t['info']
        info_encode = bencode.bencode(info)
        sha = hashlib.sha1(info_encode).digest()
        info_hash =  urllib.quote_plus(sha)
        peer_id = '-lt0D20-%97%FA%2A%AE%CC%9B%83P1%BAyB'
        res = session.get("%s?info_hash=%s&peer_id=%s&key=64214229&compact=1&port=9999&uploaded=0&downloaded=0&left=543534" % (announce, info_hash, peer_id), verify=False)
        requests.get("%s?info_hash=%s&peer_id=%s&key=64214229&compact=1&port=9999&uploaded=0&downloaded=0&left=0" % (announce, info_hash, peer_id), verify=False)
        t = bencode.bdecode(res.content)
        peers = [t['peers'][i:i+6] for i in range(0, len(t['peers']), 6)]
        with open("%s/%s.torrent" % (data_dir, torrent_id), "w") as torrent:
             [log.write("%s\n" % socket.inet_ntoa(p[:4])) for p in peers]
        
    def get_torrent(torrent_id):
        res = session.get("%s/torrents.php?action=download&id=%s&authkey=%s&torrent_pass=%s" % (site, torrent_id, auth_key, torrent_pass), verify=False)
        with open("%s/%s.torrent" % (data_dir, torrent_id), "w") as torrent:
            torrent.write(res.content)
        get_peers(torrent_file)

    def get_peerlist(torrent_id):
        res = session.get("%s/torrents.php?action=peerlist&torrentid=%d" % (site, torrent_id), verify=False)
        users = re.findall("href=.*>(.+?)<", res.text.replace("&nbsp;",""), re.I)
        if len(users) < 1:  return
        with open("%s/%s.torrent.peerlist" % (data_dir, torrent_id), "w") as peers:
            [peers.write("%s\n" % u) for u in users]


    p = Pool(1)
    [p.spawn(get_torrent, t) for t in torrent_ids]
    [p.spawn(get_peerlist, t) for t in torrent_ids]
    p.join()
    
session = get_session("000", "niggers1")
if session:
    get_data(session, range(1, 1000))
