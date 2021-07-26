from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Back, init
import random
import termios
import sys
import time
import contextlib
from os import get_terminal_size
import os
import time
kanan = 'd'
kiri = 'a'
cheat = 'c'
auto = "g"
atas = 'w'
bawah = 's'
menembak = ' '
s_batu = 'x'
init(True)
class tembak:
    peluru_code = "*"
    user = '^'
    blank = ''
    batu = "@"
    def __init__(self) -> None:
        self.terminal_size = get_terminal_size()
        self.clear = os.popen( 'cls' if os.name == 'nt' else 'clear').read()
        self.color = ""
    def setup_game(self):
        self.board = [ ['']*self.terminal_size[0] for i in range(self.terminal_size[1]-1)]#np.zeros([get_terminal_size()[1]-1, get_terminal_size()[0]], str)
        self.position = [self.terminal_size[0]//2, self.terminal_size[1]-3]
        self.asteroids=[]
        self.createFrame()
        #signal.signal(2, self.shutdown)
        self.board[self.position[1]][self.position[0]] = self.user
    def start_(self) -> None:
        self.start = time.time()
        self.stop = False
        self.thr = ThreadPoolExecutor(max_workers=4)
        #self.thr=threading.Thread(target=self.send_keys, args=())
        #self.thr2 = threading.Thread(target=self.tembak, args=())
        #self.thr3 = threading.Thread(target=self.asteroid_move, args=())
        self.score = 0
        self.speed = 0.04
        #self.thr.start()
        #self.thr2.start()
        #self.thr3.start()
        self.thr.submit(self.send_keys)
        self.thr.submit(self.tembak)
        self.thr.submit(self.asteroid_move)
        self.display()
    def createFrame(self):
        self.board[0][0] = "+"
        self.board[0][-1] ="+"
        self.board[-1][0] ="+"
        self.board[-1][-1] ="+"
        for i in range(1,self.board[0].__len__()-1):
            self.board[0][i] = "#"
            self.board[-1][i] = "#"
        for i in range(1,self.board.__len__()-1):
            self.board[i][0] = "#"
            self.board[i][-1] = "#"
    def auto(self):
        if self.position[1] > 1:
            for y in range(1, self.board.__len__()-1):
                for x in range(1, self.board[y].__len__()-1):
                    if self.board[y][x] == self.batu:
                        self.board[self.position[1]-1][x] = self.peluru_code
            
    def banner(self):
        score=self.score.__str__().zfill(4)
        for i in zip(list(range(2,score.__len__()+2)[::-1]), score):
            if not self.board[1][-i[0]] in [self.batu, self.user]:
                self.board[1][-i[0]] = Fore.YELLOW+i[1]+Fore.RESET
        calc = time.time()-self.start
        for i in enumerate(f"{round(calc//60).__str__().zfill(2)}:{round(calc%60).__str__().zfill(2)}", 1):
            if not self.board[1][i[0]] in [self.batu, self.user]:
                self.board[1][i[0]] = Fore.YELLOW+i[1]+Fore.RESET
    def tembak(self):
        while True:
            #print('a')
            if self.stop:
                break
            for y in range(self.board.__len__()):
                for x in range(self.board[y].__len__()):
                    if self.board[y][x] == self.peluru_code:
                        if self.board[y-1][x]==self.batu:
                            self.board[y-1][x] = self.blank
                            self.board[y][x] = self.blank
                            self.score+=1
                        elif not y==1:
                            self.board[y][x] = self.blank
                            self.board[y-1][x] = self.peluru_code
                        elif y==1:
                            self.board[y][x] = self.blank
                    elif self.board[y][x] == self.batu:
                        self.asteroids.append([x, y])
            time.sleep(0.04)
    def asteroid_move(self):
        times = time.time()
        while True:
            if self.stop:
                break
            elif times<time.time():
                self.asteroid()
                times=time.time()+3
            for x,y in random.sample(self.asteroids, self.asteroids.__len__()):
                    if self.board[y][x] == self.batu and self.board[y+1][x] == self.batu:
                        True
                    elif self.board[y][x] == self.batu and  y == self.board.__len__()-2:
                        self.board[y][x] = self.blank
                    elif self.board[y][x] == self.batu and  self.board[y+1][x] == self.user:
                        self.score-=1
                        self.board[y][x] = self.blank
                    elif self.board[y][x] == self.batu and y >= self.board.__len__():
                        self.board[y][x]=self.blank
                    elif self.board[y][x] == self.batu:
                        self.board[y][x]=self.blank
                        self.board[y+1][x] = self.batu
                        time.sleep(0.1)
    def asteroid(self):
        batu = random.sample(range(1,self.board[0].__len__()-1),8)
        for i in batu:
            self.board[1][i] = self.batu
    def menembak(self):
        if not self.position[1] == 1:
            self.board[self.position[1]-1][self.position[0]] = self.peluru_code
    def toScrren(self):
        while True:
            text = ""
            self.banner()
            for y in range(self.board.__len__()):
                for x in range(self.board[y].__len__()):
                    brd = self.board[y][x]
                    #text+=brd.__str__()
                    text+= ' ' if brd == '' else brd
                    #text+= " "if brd==self.blank else "^" if brd == self.user else "*" if brd == self.peluru_code else "#" if brd == self.batu else brd if isinstance(brd, str) else ''
            yield text.replace(self.batu, f'{Fore.LIGHTRED_EX}{self.batu}{Fore.RESET}').replace(self.peluru_code, f'{Fore.LIGHTMAGENTA_EX}^{Fore.RESET}').replace(self.user, f'{Fore.LIGHTBLUE_EX}{self.user}{Fore.RESET}').replace('#', f'{Back.LIGHTGREEN_EX}%{Back.RESET}').replace('+', f'{Back.LIGHTBLUE_EX}+{Back.RESET}')
    @contextlib.contextmanager
    def raw_mode(self, file):
        old_attrs = termios.tcgetattr(file.fileno())
        new_attrs = old_attrs[:]
        new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
        try:
            termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
            yield
        finally:
            termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)
    def pindah(self, kanan=0, bawah=0, kiri=0, atas=0):
        x, y = get_terminal_size()
        self.board[self.position[1]][self.position[0]] = self.blank
        self.position[0] = self.position[0]-kiri+kanan
        self.position[1] = self.position[1]-atas+bawah
        self.position[0] =x-2 if self.position[0]>=x-2 else self.position[0]
        self.position[1] =y-3 if self.position[1]>=y-3 else self.position[1]
        self.position[0] = 1 if self.position[0]<1 else self.position[0]
        self.position[1] = 1 if self.position[1]<1 else self.position[1]
        self.position[0] = 0 if self.position[0] < 0 else self.position[0]
        self.position[1] = 0 if self.position[1] < 0 else self.position[1]
        if self.board[self.position[1]][self.position[0]]==self.batu:
            self.score-=1
        self.board[self.position[1]][self.position[0]] = self.user
    def send_keys(self):
        h = ""
        with self.raw_mode(sys.stdin):
            while True:
                if self.stop:
                    break
                h = sys.stdin.read(1).lower()
                #print(h.__repr__())
                self.pindah(kanan=1) if h == kanan else self.pindah(kiri=1) if h==kiri else self.position[0]
                self.pindah(bawah=1) if h == bawah else self.pindah(atas=1) if h==atas else self.position[1]
                self.menembak() if h == menembak else self.asteroid() if h==s_batu else self.auto() if h==auto else ''
                if h==cheat and self.position[1]>1:
                    for i in range(1, self.board[0].__len__()-1):
                        self.board[self.position[1]-1][i] = self.peluru_code
    def display(self):
        self.asteroid()
        for i in self.toScrren():
            try:
                x, y = get_terminal_size()
                if self.stop:
                    break
                elif x==self.terminal_size[0] and y==self.terminal_size[1]:
                    print('\x1b[H\x1b[2J\x1b[3J'+i)
                    time.sleep(0.01)
                else:
                    self.terminal_size = get_terminal_size()
                    self.setup_game()
            except KeyboardInterrupt:
                self.stop = True
                    
game = tembak()
game.setup_game()
game.start_()
