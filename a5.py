# Mason Wong
# masonjw1@uci.edu
# 48567424

from ds_messenger import DirectMessenger
from gui import run

if __name__ == '__main__':
    mason = DirectMessenger('168.235.86.101', 'jonlee2', 'password')
    mason2 = DirectMessenger('168.235.86.101', 'oswald2', 'password')
    mason3 = DirectMessenger('168.235.86.101', 'masonwongjohn1', 'password')
    mason4 = DirectMessenger('168.235.86.101', 'masonwongjohn', 'password')
    # mason.send('hi this jon2 again', 'masonwongjohn1')
    # mason2.send('hi oswald2 again', 'masonwongjohn1')
    run()
