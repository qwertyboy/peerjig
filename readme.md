import os
data_path = "dataset"

class Torrent:
    def __init__(self):
        self.users = []
        self.peers = []

torrents = {} 
users = {}

def parse_users(torrent_id, filename):
    for line in open(filename).readlines():
        try:
            uid, username = line.strip().split(":")
            if username not in users:
                users[username] = []
            users[username].append(torrent_id)
            
            torrents[torrent_id].users.append(username)
        except:
            pass
        
def parse_peers(torrent_id, filename):
    for line in open(filename).readlines():
        try:
            ip, port = line.strip().split(":")
            torrents[torrent_id].peers.append(ip)
        except:
            pass
            
def parse_listing(listing):
    ip_inserts = []
    user_inserts = []
    for filename in listing:
        try:
            torrent_id, _, list_type = filename.split(".") 
            
            if torrent_id not in torrents:
                torrents[torrent_id] = Torrent()
            
            if list_type == "peerlist":
                parse_users(torrent_id, "%s/%s" % (data_path, filename))
            elif list_type == "peer":
                parse_peers(torrent_id, "%s/%s" % (data_path, filename))

        except:
            pass

if __name__ == "__main__":
    listing = os.listdir(data_path)
    parse_listing(listing)
    for user in users:
        peers = {}
        for torrent in [torrents[t] for t in users[user]]:
            for peer in torrent.peers:
                if peer not in peers:
                    peers[peer] = 0
                peers[peer] += 1
        top = sorted(peers, key=peers.get, reverse=True)[0]
        print "%s - %s (%s/%s)" % (user, top, peers[top], len(users[user]))
