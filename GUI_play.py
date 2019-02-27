from tkinter import *
from move import *

class GUI :
    turn = 'W'
    move = ""
    move_count = 1
    fifty_move_count = 0
    
    @staticmethod
    def read_FEN(string):
        x = 0
        y = 7
        i=0
        space_count = 0
        while i < len(string) :
            
            if space_count == 0 :
                if string[i] == 'r' :
                    edit_board(x,y,'BR') 
                elif string[i] == 'n' :
                    edit_board(x,y,'BN')
                elif string[i] == 'b' :
                    edit_board(x,y,'BB')
                elif string[i] == 'q' :
                    edit_board(x,y,'BQ')
                elif string[i] == 'k' :
                    edit_board(x,y,'BK')
                elif string[i] == 'p' :
                    edit_board(x,y,'BP')
                elif string[i] == 'R' :
                    edit_board(x,y,'WR')
                elif string[i] == 'N' :
                    edit_board(x,y,'WN')
                elif string[i] == 'B' :
                    edit_board(x,y,'WB')
                elif string[i] == 'Q' :
                    edit_board(x,y,'WQ')
                elif string[i] == 'K' :
                    edit_board(x,y,'WK')
                elif string[i] == 'P' :
                    edit_board(x,y,'WP')
                elif string[i] == ' ':
                    space_count += 1
                elif string[i] >= '1' and string[i] <= '8' :
                    for k in range (x,x+ord(string[i])-ord('0')):
                        edit_board(k,y,'0')
                    x = x + ord(string[i])-ord('0')-1
                if string[i] == '/' :        #Need case if string is a number
                    for k in range (x,8):
                        edit_board(k,y,'0')
                    x = 0
                    y -= 1
                else : x += 1
            elif space_count == 1 :
                if string[i] == 'w' :
                    GUI.turn = 'W'
                elif string[i] == 'b' :
                    GUI.turn = 'B'
                elif string[i] == 'K' :
                    GUI.turn = 'B'
                elif string[i] == ' ' :
                    space_count += 1

            elif space_count == 2 :
                a = 0
                b = 0
                c = 0
                d = 0
                while string[i] != ' ':
                    if string[i] == 'K' :
                        a = 1
                    elif string[i] == 'Q' :
                        b = 1
                    elif string[i] == 'k' :
                        c = 1
                    elif string[i] == 'q' :
                        d = 1
                    i += 1
                edit_castle_rights(a,b,c,d)
                                
                if string[i] == ' ' :
                    space_count += 1
            elif space_count == 3 :
                if string[i] != '-' :
                    edit_double_pawn(True,string[i])
                    space_count += 1
                    i += 2
                elif  string[i] == '-':
                    space_count += 1
                    i += 1
            elif space_count == 4 :
                if string[i] == ' ':
                    i += 1
                else:
                    digit_count = 0
                    while string[i] != ' ':
                        digit_count += 1
                        i += 1
                    power = 1
                    GUI.fifty_move_count = 0
                    for k in range (digit_count):
                        GUI.fifty_move_count += power*(ord(string[i-1-k])-ord('0'))
                        power *= 10

                    
                space_count += 1
            elif space_count == 5 :
                if string[i] == ' ':
                    i += 1
                else:
                    digit_count = 0
                    while i < len(string) and string[i] != ' ':
                        digit_count += 1
                        i += 1
                    power = 1
                    GUI.move_count = 0
                    for k in range (digit_count):
                        GUI.move_count += power*(ord(string[i-1-k])-ord('0'))
                        power *= 10
                       
                space_count += 1
            i += 1
        GUI.move='0'
        update_GUI()
            
    @staticmethod
    def get_FEN() :
        string = ""
        for j in range(8):
            count = 0
            for i in range(8):
                
                if count >0 :
                    if board[i][7-j] != '0':
                        string += str(count)
                        count = 0
                    elif i == 7 :
                        string += str(count+1)
                        count = 0
                        
                if board[i][7-j] == 'BP' :
                    string += 'p'
                elif board[i][7-j] == 'BR' :
                    string += 'r'
                elif board[i][7-j] == 'BN' :
                    string += 'n'
                elif board[i][7-j] == 'BB' :
                    string += 'b'
                elif board[i][7-j] == 'BQ' :
                    string += 'q'
                elif board[i][7-j] == 'BK' :
                    string += 'k'
                elif board[i][7-j] == 'WP' :
                    string += 'P'
                if board[i][7-j] == 'WR' :
                    string += 'R'
                elif board[i][7-j] == 'WN' :
                    string += 'N'
                elif board[i][7-j] == 'WB' :
                    string += 'B'
                elif board[i][7-j] == 'WQ' :
                    string += 'Q'
                elif board[i][7-j] == 'WK' :
                    string += 'K'
                elif board[i][7-j] == '0' :
                    count += 1
            if j <7  :  
                string += '/'
        if GUI.turn == 'W' :
            string += ' w'
        else : string += ' b'

        string += ' '
        if get_castle_rights('W') == [0,0] and get_castle_rights('B') == [0,0] :
            string += '-'
        else :
            if get_castle_rights('W')[0] == 1 :
                string += 'K'
            if get_castle_rights('W')[1] == 1 :
                string += 'Q'
            if get_castle_rights('B')[0] == 1 :
                string += 'k'
            if get_castle_rights('B')[1] == 1 :
                string += 'q'
        if get_double_pawn()[0] == False :
            string += ' -'
        else :
            string += ' ' + get_double_pawn()[1]
            if GUI.turn == 'W' :
                string += '6'
            else : string += '3'
        string += ' ' + str(GUI.fifty_move_count)
        string += ' ' + str(GUI.move_count)
        return string

    @staticmethod
    def game_over(turn):
        top = Toplevel()
        top.title("Game over")
        text_result = ""
        if turn == 'B':
            text_result = "White wins! 1-0"
        elif result == 'W':
            text_result = "Black wins! 0-1"
        elif result == 's':
            text_result = "Stalemate! 1/2-1/2"
        else : text_result = "It's a draw! 1/2-1/2"
        msg = Message(top, text = text_result)
        msg.pack()

class Square(GUI):

    clicked = False
    start = 0
    clicked_piece = '0'

    def __init__(self, master, pos, piece, button):

        self.pos = pos
        self.piece = piece
        if (s_to_i(pos)[0]+s_to_i(pos)[1])%2 == 0 :
            self.color = 'brown'
        else :
            self.color = 'white'


        if button :
            self.button = Button(text=self.piece, fg="red", command = self.callback)
            self.button.grid(row = 7-(ord(self.pos[1])-49), column = ord(self.pos[0])-97)

    def callback(self):
        if Square.clicked == False :
            if self.piece[0] == GUI.turn :
                Square.clicked_piece = self.piece
                Square.start = self.pos
                Square.clicked = True
                self.button.config(background = "yellow")
        else :
            GUI.move = find_move(Square.start,self.pos,GUI.turn,Square.clicked_piece[-1])
            if GUI.move != False :
                if GUI.move[-1] == '=' :
                    promote = promotion(GUI.turn)
                    root.wait_window(promote.new_window)
                    GUI.move += promote.promote_to
                                    
                if update_position(Square.start, self.pos,GUI.move,Square.clicked_piece[-1],GUI.turn) :

                    GUI.move += move_suffix(GUI.turn)
                    
                    if GUI.turn == 'W':
                        GUI.turn = 'B'
                    else :
                        GUI.turn = 'W'
                        GUI.move_count += 1
                    movelist.add_move(GUI.move, GUI.turn)
                    update_GUI()

                    if GUI.move[-1] == '#':
                        GUI.game_over(GUI.turn)
                    elif stalemate(GUI.turn) :
                        GUI.game_over('s')
                     
            Square.clicked = False
            GUI_board[s_to_i(Square.start)[0]][s_to_i(Square.start)[1]].button.config(background=GUI_board[s_to_i(Square.start)[0]][s_to_i(Square.start)[1]].color)
              
def update_GUI() :
    if Square.clicked:
        GUI_board[s_to_i(Square.start)[0]][s_to_i(Square.start)[1]].button.config(background=GUI_board[s_to_i(Square.start)[0]][s_to_i(Square.start)[1]].color)
        Square.clicked = False
    if 'x' in GUI.move :
        GUI.fifty_move_count = 0
    elif ord(GUI.move[0]) >= ord('a') and ord(GUI.move[0]) <= ord('h') :
        GUI.fifty_move_count = 0
    else : GUI.fifty_move_count += 1
    
    for i in range (8) :
        for j in range (8) :
            if GUI_board[i][j].piece != board[i][j] :
                GUI_board[i][j].piece = board[i][j]
                if GUI_board[i][j].piece == '0' :
                    GUI_board[i][j].button.config(image="",height=4,width=8)                
                else :
                    photo = PhotoImage (file = GUI_board[i][j].piece + ".png")
                    if(board[i][j][-1] == 'N'):
                        photo = photo.subsample(9)
                    elif(board[i][j][-1] == 'R'):
                        photo = photo.subsample(17)
                    else : photo = photo.subsample(15)
                    GUI_board[i][j].photo = photo
                    GUI_board[i][j].button.config(image = GUI_board[i][j].photo , text="",height =65, width = 60)
                    
class promotion :
    def __init__(self,turn):
        prefix = './assets/'
        self.turn = turn
        self.promote_to = '0'
        self.new_window = Toplevel()
        self.photo1 = PhotoImage(file = prefix + turn + 'Q.png')
        self.photo1 = self.photo1.subsample(15)
        self.button1 = Button(self.new_window, image = self.photo1, height = 70, width = 70, command = self.callback1)
        self.button1.grid(row = 0, column = 0)
        self.photo2 = PhotoImage(file = prefix + turn + 'R.png')
        self.photo2 = self.photo2.subsample(17)
        self.button2 = Button(self.new_window, image = self.photo2, height = 70, width = 70, command = self.callback2)
        self.button2.grid(row = 1, column = 0)
        self.photo3 = PhotoImage(file = prefix + turn + 'B.png')
        self.photo3 = self.photo3.subsample(15)
        self.button3 = Button(self.new_window, image = self.photo3, height = 70, width = 70, command = self.callback3)
        self.button3.grid(row = 0, column = 1)
        self.photo4 = PhotoImage(file = prefix + turn + 'N.png')
        self.photo4 = self.photo4.subsample(9)
        self.button4 = Button(self.new_window, image = self.photo4, height = 70, width = 70, command = self.callback4)
        self.button4.grid(row = 1, column = 1)

    def callback1(self) :
        self.new_window.destroy()
        self.promote_to = 'Q'
    def callback2(self) :
        self.new_window.destroy()
        self.promote_to = 'R'
    def callback3(self) :
        self.new_window.destroy()
        self.promote_to = 'B'
    def callback4(self) :
        self.new_window.destroy()
        self.promote_to = 'N'

class move_list(GUI) :
    pgn_moves = ""
    def __init__(self,master,turn) :
        self.scrollbar = Scrollbar(master)
        self.scrollbar.grid(row=3, column = 8)
        self.listbox = Listbox(master, selectmode = SINGLE, yscrollcommand=self.scrollbar.set, height = 10, width=10)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)
        self.listbox.grid(row=0, column = 9, rowspan = 8)
        self.scrollbar.config(command=self.listbox.yview)
        self.FEN = []
        self.FEN.append(GUI.get_FEN())


    def add_move(self, new_move,turn):
        half_move = 0
        if turn == 'W':
            new_move = str(GUI.move_count-1)+ '...' + new_move
            half_move = 2*(GUI.move_count-1)
        elif turn == 'B':
            new_move = str(GUI.move_count) + '. ' + new_move
            half_move = 2*(GUI.move_count-1)+1

        if  self.listbox.curselection():
            self.listbox.delete(self.listbox.curselection()[0]+1,END)
            n = len(self.FEN)-(self.listbox.curselection()[0]+2)
            self.FEN = self.FEN[:-n or None]
            self.listbox.selection_clear(0,END)
        
        self.listbox.insert(END, new_move)
        self.listbox.grid(row=0, column = 9, rowspan = 8)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.see(END)
        self.FEN.append(GUI.get_FEN())
        
        
    def on_select(self,evt):
        a = self.listbox.curselection()[0]
        GUI.read_FEN(self.FEN[a+1])
        
        

root = Tk()

GUI_board = [[Square(root, chr(i+97) + chr(j+49), board[i][j],False) for j in range (8)] for i in range (8)]
for i in range (8):
    for j in range (8):
        if(GUI_board[i][j].piece == '0'):
            GUI_board[i][j].button = Button(bg = GUI_board[i][j].color, fg="red", height = 4, width = 8, command = GUI_board[i][j].callback)
        else :
            photo = PhotoImage(file = GUI_board[i][j].piece+".png")
            if(GUI_board[i][j].piece[1] == 'N'):
                photo = photo.subsample(9)
            elif(GUI_board[i][j].piece[1] == 'R'):
                photo = photo.subsample(17)
            else :
                photo = photo.subsample(15)
            GUI_board[i][j].photo = photo
            GUI_board[i][j].button = Button(text="",bg = GUI_board[i][j].color, fg="red", command = GUI_board[i][j].callback)
            GUI_board[i][j].button.config(image=GUI_board[i][j].photo, height =65, width = 60)
        GUI_board[i][j].button.grid(row = 7-(ord(GUI_board[i][j].pos[1])-49), column = ord(GUI_board[i][j].pos[0])-97)
movelist = move_list(root,GUI.turn)


root.mainloop()

