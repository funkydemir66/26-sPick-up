import sys
from g_python.gextension import Extension
from g_python.hmessage import Direction
from time import sleep
import threading


extension_info = {
    "title": "26's Pick Up",
    "description": "dl: set&off&stack&pick ",
    "version": "0.1.1",
    "author": "funkydemir66"
}

ext = Extension(extension_info, sys.argv, silent=True)
ext.start()

KATMER = "MoveObject"

KASAR = "PassCarryItem"

HIYAR = "SetCustomStackingHeight"

kod = ""

kod2 = ""

sec_kod = sc = False

def konusma(msj):
    global sc, sec_kod, sec_player


    def main():
        while sc:
            for i in range(256):
                if sc:
                    ext.send_to_server('{out:'+str(KATMER)+'}{i:'+str(kod2)+'}{i:1}{i:11}{i:0}')
                    sleep(0.3)


    text = msj.packet.read_string()

    if text == ':dl stack':
        msj.is_blocked = True
        sec_kod = True
        ext.send_to_client('{in:Chat}{i:123456789}{s:"Select and move the furniture you want to stack, then type :dl set"}{i:0}{i:30}{i:0}{i:0}')

    if text == ':dl pick':
        msj.is_blocked = True
        sec_player = True
        ext.send_to_client('{in:Chat}{i:123456789}{s:""double click on the furniture you want to remove}{i:0}{i:30}{i:0}{i:0}')

    if text == ':dl set':
        msj.is_blocked = True
        sc = True
        ext.send_to_server('{out:'+str(KATMER)+'}{i:'+str(kod)+'}{i:1}{i:11}{i:0}')
        ext.send_to_server('{out:SetCustomStackingHeight}{i:'+str(kod)+'}{i:3500}')
        ext.send_to_client('{in:Chat}{i:123456789}{s:"Stack setting "}{i:0}{i:30}{i:0}{i:0}')
        thread = threading.Thread(target=main)
        thread.start()

    if text == ':dl off':
        msj.is_blocked = True
        sc = False
        ext.send_to_client('{in:Chat}{i:123456789}{s:"Script: off "}{i:0}{i:30}{i:0}{i:0}')
        sec_player = False


def yukle_kod(p):
    global kod, sec_kod

    if sec_kod:
        mobi_id, _, _, _, _ = p.packet.read("iiiii")
        kod = str(mobi_id)
        ext.send_to_client('{in:Chat}{i:123456789}{s:"idd: saved "}{i:0}{i:30}{i:0}{i:0}')
        sec_kod = False


def yukle_kod2(p):
    global kod2, sec_player

    if sec_player:
        player_id, _, _ = p.packet.read("iii")
        kod2 = str(player_id)
        ext.send_to_client('{in:Chat}{i:123456789}{s:"Pick up '+str(kod2)+' "}{i:0}{i:30}{i:0}{i:0}')



ext.intercept(Direction.TO_SERVER, konusma, 'Chat')
ext.intercept(Direction.TO_SERVER, yukle_kod, 'MoveObject')
ext.intercept(Direction.TO_SERVER, yukle_kod2, 'UseFurniture')