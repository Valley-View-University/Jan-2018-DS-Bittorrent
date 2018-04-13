#!/usr/bin/env python

import sys

from logic.torrio import DownloadSession, Torrent


if __name__ == '__main__':
    torrent = Torrent(sys.argv[1])
    downloader = DownloadSession(torrent)
    del torrent.info[b'info'][b'pieces']
    print(torrent)
    print(downloader)
