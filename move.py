def sign(x):
    if x < 0 :
        return -1
    elif x > 0 :
        return 1
    elif x == 0:
        return 0

castling_W = [1,1]
castling_B = [1,1]
double_pawn = [False,'0']

def initial_position():
    board = [['0' for x in range (8)] for y in range (8)]
    for i in range (0,8):
        board[i][1] = 'WP'
        board[i][6] = 'BP'
    board[0][0] = 'WR'
    board[1][0] = 'WN'
    board[2][0] = 'WB'
    board[3][0] = 'WQ'
    board[4][0] = 'WK'
    board[5][0] = 'WB'
    board[6][0] = 'WN'
    board[7][0] = 'WR'
    board[0][7] = 'BR'
    board[1][7] = 'BN'
    board[2][7] = 'BB'
    board[3][7] = 'BQ'
    board[4][7] = 'BK'
    board[5][7] = 'BB'
    board[6][7] = 'BN'
    board[7][7] = 'BR'
    return board

def edit_board(x,y,piece) :
    board[x][y] = piece

def get_board(x,y):
    if x>7 or x<0 or y<0 or y>7:
        return False
    return board[x][y]
def s_to_i(square) :
    a = []
    a.append(ord(square[0])-97)
    a.append(ord(square[1])-49)
    return a

def i_to_s(x,y) :
    return chr(x+97) + chr(y+49)

def update_position(start, end, move, piece, turn):
    global double_pawn
    global castling_W
    global castling_B
    x_1 = s_to_i(start)[0]
    y_1 = s_to_i(start)[1]
    x_2 = s_to_i(end)[0]
    y_2 = s_to_i(end)[1]
    if abs(x_2>7) or abs(y_2>7) :
        return False
    elif board[x_2][y_2][0] == turn :
        return False
    elif find_move(start, end,turn, piece) == False :
        return False
    
    if move == 'O-O' or move == '0-0' : # Kingside castles
        double_pawn = [False,'0']
        if Kside_castle(turn) :
            if turn == 'W' :
                board[4][0] = '0'
                board[5][0] = 'WR'
                board[6][0] = 'WK'
                board[7][0] = '0'
                castling_W = [0,0]
            elif turn == 'B' :
                board[4][7] = '0'
                board[5][7] = 'BR'
                board[6][7] = 'BK'
                board[7][7] = '0'
                castling_B = [0,0]
            return True

    elif move == 'O-O-O' or move == '0-0-0' : # Queenside castles
        double_pawn = [False,'0']
        if Qside_castle(turn) :
            if turn == 'W' :
                board[0][0] = '0'
                board[2][0] = 'WK'
                board[3][0] = 'WR'
                board[4][0] = '0'
                castling_W = [0,0]
            elif turn == 'B' :
                board[0][7] = '0'
                board[2][7] = 'BK'
                board[3][7] = 'BR'
                board[4][7] = '0'
                castling_B = [0,0]
            return True
        
    elif piece == 'N' or piece == 'B' or piece == 'Q' : #Knight, Bishop, Rook move
        double_pawn = [False,'0']
        temp1 = board[x_1][y_1]
        temp2 = board[x_2][y_2]
        board[x_1][y_1] = '0'
        board[x_2][y_2] = turn + piece
        if check(turn) :
            board[x_1][y_1] = temp1
            board[x_2][y_2] = temp2
            return False
        return True
                       
    elif piece == 'R' : #Rook move
        double_pawn = [False,'0']
        if x_1 == 0 and y_1 == 0:
            castling_W[1] = 0
        elif  x_1 == 7 and y_1 == 0 :
            castling_W[0] = 0
        elif x_1 == 0 and y_1 == 7 :
            castling_B[1] = 0
        elif x_1 == 7 and y_1 == 7 :
            castling_B[0] = 0
            
        temp1 = board[x_1][y_1]
        temp2 = board[x_2][y_2]
        board[x_1][y_1] = '0'
        board[x_2][y_2] = turn + piece
        if check(turn) :
            board[x_1][y_1] = temp1
            board[x_2][y_2] = temp2
            return False
        return True

    elif piece == 'K': #King move
        double_pawn = [False,'0']
        if turn == 'W' :
            castling_W = [0,0]
        else : castling_B = [0,0]
        temp1 = board[x_1][y_1]
        temp2 = board[x_2][y_2]
        board[x_1][y_1] = '0'
        board[x_2][y_2] = turn + piece
        if check(turn) :
            board[x_1][y_1] = temp1
            board[x_2][y_2] = temp2
            return False
        return True
                   
    elif piece =='P' : #Pawn move
        if move[-4:] == 'e.p.' :
            board[x_1][y_1] = '0'
            board[x_2][y_2] = turn + 'P'
            temp = '0'
            if turn == 'W' :
                temp = board[x_2][y_2-1]
                board[x_2][y_2-1] = '0'
            elif turn == 'B' :
                temp = board[x_2][y_2+1]
                board[x_2][y_2+1] = '0'
            if(check(turn)) :
                board[x_1][y_1] = turn +'P'
                if turn == 'W' :
                    board[x_2][y_2-1] = temp
                elif turn == 'B':
                    board[x_2][y_2+1] = temp
                return False
            double_pawn = [False,'0']
            return True
                        
        if y_2 == 0 or y_2 == 7 :
            if move[-1] == '+' or move[-1] == '#' :
                piece = move[-2]
            else: piece = move[-1]
        temp = board[x_2][y_2]
        board[x_1][y_1] = '0'
        board[x_2][y_2] = turn + piece
        if check(turn):
            board[x_1][y_1] = turn + 'P'
            board[x_2][y_2] = temp
            return False
        if abs(y_2-y_1) == 2 :
            double_pawn = [True,start[0]]
        else : double_pawn = [False,'0']
        return True
    return False
    
def N_move(start, end, turn):
    x_1 = ord(start[0])-97
    y_1 = ord(start[1])-49
    x_2 = ord(end[0])-97
    y_2 = ord(end[1])-49
    if abs(x_2) > 7 or abs(y_2) > 7 :
        return False
    if x_2 == x_1 and y_2 == y_1 :
        return False
    if board[x_1][y_1] != turn + 'N' :
        return False
    
    if x_1+2 == x_2 and (y_1 + 1 == y_2 or y_1 - 1 == y_2) :
        return True
    elif x_1-2 == x_2 and (y_1 + 1 == y_2 or y_1 - 1 == y_2) :
        return True
    elif x_1+1 == x_2 and (y_1 + 2 == y_2 or y_1 - 2 == y_2) :
        return True
    elif x_1-1 == x_2 and (y_1 + 2 == y_2 or y_1 - 2 == y_2) :
        return True
    else : return False

    return False

def B_move(start, end, turn):
    x_1 = ord(start[0])-97
    y_1 = ord(start[1])-49
    x_2 = ord(end[0])-97
    y_2 = ord(end[1])-49
    if abs(x_2) > 7 or abs(y_2) > 7 :
        return False
    if x_2 == x_1 and y_2 == y_1 :
        return False
    if board[x_1][y_1] != turn + 'B' :
        return False

    if(abs(y_2-y_1) != abs(x_2-x_1)):
        return False
    if(y_2>y_1 and x_2>x_1):                        #diagonal 1
        for i in range (1,abs(y_2-y_1)) :
            if board[x_1 + i][y_1+i] != '0' : 
                return False
    elif(y_2<y_1 and x_2>x_1):                      #diagonal 2
        for i in range (1,abs(y_2-y_1)) :
            if board[x_1 + i][y_1-i] != '0' : 
                return False
    elif(y_2<y_1 and x_2<x_1):                      #diagonal 3
        for i in range (1,abs(y_2-y_1)) :
            if board[x_1 - i][y_1-i] != '0' : 
                return False
    elif(y_2>y_1 and x_2<x_1):                      #diagonal 4
        for i in range (1,abs(y_2-y_1)) :
            if board[x_1 - i][y_1+i] != '0' :
                return False
    return True

def R_move(start, end, turn):
    x_1 = ord(start[0])-97
    y_1 = ord(start[1])-49
    x_2 = ord(end[0])-97
    y_2 = ord(end[1])-49
    if abs(x_2) > 7 or abs(y_2) > 7 :
        return False
    if x_2 == x_1 and y_2 == y_1 :
        return False
    if board[x_1][y_1] != turn + 'R' :
        return False
    if(x_1 != x_2 and y_1 != y_2):
        return False
    if x_1 == x_2 :
        for i in range (sign(y_2-y_1), y_2-y_1, sign(y_2-y_1)) :
            if board[x_1][y_1+i] != '0' :
                return False
    elif y_1 == y_2 :
        for i in range (sign(x_2-x_1), x_2-x_1, sign(x_2-x_1)) :
            if board[x_1+i][y_1] != '0' :
                return False
    return True

def Q_move(start, end, turn) :
    x_1 = ord(start[0])-97
    y_1 = ord(start[1])-49
    x_2 = ord(end[0])-97
    y_2 = ord(end[1])-49
    if board[x_1][y_1] != turn + 'Q' :
        return False
    
    board[x_1][y_1] = turn + 'R'
    if R_move(start,end,turn) :
        board[x_1][y_1] = turn + 'Q'
        return True
    board[x_1][y_1] = turn + 'B'
    if B_move(start,end,turn) :
        board[x_1][y_1] = turn + 'Q'
        return True
    board[x_1][y_1] = turn + 'Q'
    return False

def K_move(start, end, turn) :
    x_1 = ord(start[0])-97
    y_1 = ord(start[1])-49
    x_2 = ord(end[0])-97
    y_2 = ord(end[1])-49
    if abs(x_2) > 7 or abs(y_2) > 7 :
        return False
    other_side = 'W'
    if(turn == 'W'):
        other_side = 'B'
    if board[x_2][y_2][0] == turn :
        return False
    if board[x_1][y_1] != turn + 'K' :
        return False
    if x_1 + sign(x_2-x_1) == x_2 and y_1 + sign(y_2-y_1) == y_2 :
        return True
    return False

def P_move(start, end, turn) :
    global double_pawn
    x_1 = ord(start[0])-97
    y_1 = ord(start[1])-49
    x_2 = ord(end[0])-97
    y_2 = ord(end[1])-49
    if abs(x_2) > 7 or abs(y_2) > 7 :
        return False
    if x_2 == x_1 and y_2 == y_1 :
        return False
    if en_passant(start,end,turn) :
        return True
    
    if turn == 'W' :
        if y_2 - y_1 == 1:
            
            if x_1 == x_2 and board[x_2][y_2] == '0':
                return True
            if abs(x_2-x_1) == 1 and board[x_2][y_2][0] == 'B':
                return True
               
        elif y_2-y_1 == 2 and x_1 == x_2 and \
             board[x_1][y_1+1] == '0' and board[x_2][y_2] == '0' and y_1 == 1 :
            return True
            
    elif turn == 'B' :
        if y_2 - y_1 == -1 :
            if x_1 == x_2 and board[x_2][y_2] == '0':
                return True
            if abs(x_2-x_1) == 1 and board[x_2][y_2][0] == 'W' :
                return True
        elif y_2-y_1 == -2 and x_1 == x_2 and \
             board[x_1][y_1-1] == '0' and board[x_2][y_2] == '0' and y_1 == 6 :
            return True
    return False

def en_passant(start, end, turn) :
    global double_pawn
    x_1 = s_to_i(start)[0]
    y_1 = s_to_i(start)[1]
    x_2 = s_to_i(end)[0]
    y_2 = s_to_i(end)[1]
    if double_pawn[0] == False:
        return False
    if turn == 'W' and y_2-y_1 == 1 and abs(x_2-x_1) == 1 and \
       board[x_2][y_2] == '0' and y_1 == 4 and double_pawn[1] == end[0] :
        return True
    elif turn == 'B' and y_2-y_1 == -1 and abs(x_2-x_1) == 1 and \
       board[x_2][y_2] == '0' and y_1 == 3 and double_pawn[1] == end[0] :
        return True
    return False

def get_double_pawn() :
    global double_pawn
    return double_pawn

def edit_double_pawn(a,b):
    global double_pawn
    double_pawn = [a,b]
    
    
def find_move(start, end, turn, piece):
    x_1 = ord(start[0])-97
    y_1 = ord(start[1])-49
    x_2 = ord(end[0])-97
    y_2 = ord(end[1])-49
    
    other_side ='W'
    if turn == 'W' :
        other_side = 'B'
    return_move = '0'
    if board[x_2][y_2][0] == turn :
        return False
    if start == end :
        return False
    
    if piece == 'N' and N_move(start, end, turn):
            return_move = 'N'
    elif piece == 'B' and B_move(start, end, turn):
            return_move = 'B'
    elif piece == 'R' and R_move(start, end, turn):
            return_move = 'R'
    elif piece == 'Q' and Q_move(start, end, turn):
            return_move = 'Q'
    elif piece == 'K' :
        if K_move(start, end, turn):
            return_move = 'K'
        if turn == 'W' :
            if end == 'g1' and Kside_castle('W') :
                return 'O-O'
            elif end == 'c1' and Qside_castle('W'):
                return 'O-O-O'
        elif turn == 'B' :
            if end == 'g8' and Kside_castle('B') :
                return 'O-O'
            elif end == 'c8' and Qside_castle('B') :
                return 'O-O-O'
        if K_move(start, end, turn):
            return_move = 'K'
        else : return False
    elif piece == 'P' and P_move(start, end, turn):
        if board[x_2][y_2][0] == other_side  :
            return_move = start[0] + 'x' + end
        elif en_passant(start,end,turn) :
            return_move = start[0] + 'x' + end +' e.p.'
        elif board[x_2][y_2] == '0' :
            return_move = end
        if y_2 == 0 or y_2 == 7 :
            return_move += '='
        return return_move
    else : return False

    if not legal_pos(start,end, turn) :
        return False
    if piece == 'N':
        a = []
        let_var = False
        num_var = False
        for i in range (8) :
            for j in range (8) :
                if board[i][j] == turn + piece and i_to_s(i,j) != start and\
                   N_move(i_to_s(i,j),end,turn):
                    a.append(i_to_s(i,j))
        for i in range (len(a)) :
            if start[0] == a[i][0] :
                let_var = True
            if start[1] == a[i][1] :
                num_var = True
        if(num_var):
            return_move += start[0]
        if(let_var):
            return_move += start[1]
        if len(a) > 0 :
            if start[0] != a[i][0] and start[1] != a[i][1]:
                return_move += start[0]

    elif piece == 'R':
        a = []
        let_var = False
        num_var = False
        for i in range (8) :
            for j in range (8) :
                if board[i][j] == turn + piece and i_to_s(i,j) != start and \
                   R_move(i_to_s(i,j),end,turn):
                    a.append(i_to_s(i,j))
        for i in range (len(a)) :
            if start[0] == a[i][0] :
                let_var = True
            if start[1] == a[i][1] :
                num_var = True
        if(num_var):
            return_move += start[0]
        if(let_var):
            return_move += start[1]
        if len(a) > 0 :
            if start[0] != a[i][0] and start[1] != a[i][1]:
                return_move += start[0]

    elif piece == 'B':
        a = []
        let_var = False
        num_var = False
        for i in range (8) :
            for j in range (8) :
                if board[i][j] == turn + piece and i_to_s(i,j) != start and \
                   B_move(i_to_s(i,j),end,turn):
                    a.append(i_to_s(i,j))
        for i in range (len(a)) :
            if start[0] == a[i][0] :
                let_var = True
            if start[1] == a[i][1] :
                num_var = True
        if(num_var):
            return_move += start[0]
        if(let_var):
            return_move += start[1]
        if len(a) > 0 :
            if start[0] != a[i][0] and start[1] != a[i][1]:
                return_move += start[0]

    elif piece == 'Q':
        a = []
        let_var = False
        num_var = False
        for i in range (8) :
            for j in range (8) :
                if board[i][j] == turn + piece and i_to_s(i,j) != start and \
                   Q_move(i_to_s(i,j),end,turn):
                    a.append(i_to_s(i,j))
        for i in range (len(a)) :
            if start[0] == a[i][0] :
                let_var = True
            if start[1] == a[i][1] :
                num_var = True
        if num_var :
            return_move += start[0]
        if let_var:
            return_move += start[1]
        if len(a) > 0 :
            if start[0] != a[i][0] and start[1] != a[i][1]:
                return_move += start[0]
       
                
    if board[x_2][y_2][0] == other_side :
        return_move += 'x'
    return return_move + end

def move_suffix(turn):
    if(turn == 'B'):
        if checkmate('W') :
            return '#'
        elif check('W') :
            return '+'
    else :
        if checkmate('B') :
            return '#'
        elif check('B') :
            return '+'
    return ""
    
    

def square_attacked(square,side) : #Answers if a square is attacked by side (e.g. by black)
    return_list = []
    return_list.append(False)
    a = 1
    if side == 'B' :
        a=-1
    for i in range (8) :
        for j in range (8) :
            square_ij = i_to_s(i,j)
            if board[i][j][0] == side :
                if N_move(square_ij, square,side) == True :
                   return_list[0] = True
                   return_list.append('N'+square_ij)
                if B_move(square_ij, square,side) == True :
                    return_list[0] = True
                    return_list.append('B'+square_ij)
                if R_move(square_ij, square,side) == True:
                    return_list[0] = True
                    return_list.append('R'+square_ij)
                if Q_move(square_ij, square,side) == True :
                    return_list[0] = True
                    return_list.append('Q'+square_ij)
                if K_move(square_ij, square,side) == True :
                    return_list[0] = True
                    return_list.append('K'+square_ij)
                if board[i][j] == side+'P' and s_to_i(square)[1]-j == a \
                   and abs(s_to_i(square)[0]-i)==1: #pawn attack
                    return_list[0] = True
                    return_list.append('P'+square_ij)
    return return_list

def legal_pos(start, end, turn) :
    x_1 = ord(start[0])-97
    y_1 = ord(start[1])-49
    x_2 = ord(end[0])-97
    y_2 = ord(end[1])-49
    temp1 = board[x_1][y_1]
    temp2 = board[x_2][y_2]
    if x_2 >7 or x_2 <0 or y_2 >7 or y_2 <0 :
        return False
    elif end == find_king(turn) :
        return False
    board[x_1][y_1] = '0'
    board[x_2][y_2] = temp1
    if check(turn):
        board[x_1][y_1] = temp1
        board[x_2][y_2] = temp2
        return False
    else :
        board[x_1][y_1] = temp1
        board[x_2][y_2] = temp2
        return True

def find_king(side):
    square = False
    for i in range (8) :
        for j in range (8) :
            if board[i][j] == side + 'K' :
                square =  i_to_s(i,j)
    if square == False :
        print("Error: find_king")
        print_position()
    return square

def check(side) :
    square = find_king(side)
    if side == 'W' and square_attacked(square, 'B')[0] == True :
        return True
    elif side == 'B' and square_attacked(square, 'W')[0] == True :
        return True
    return False

def checkmate(side) :
    if check(side) == False:
        return False
    square = find_king(side)
    x = ord(square[0])-97
    y = ord(square[1])-49
    other_side ='W'
    if side == 'W' :
        other_side ='B'
    attackers = square_attacked(square,other_side)
    #Can the king move?
    if get_board(x+1,y) == '0' and legal_pos(square, i_to_s(x+1,y), side) :
        return False
    if get_board(x-1,y) == '0' and legal_pos(square, i_to_s(x-1,y), side) :
        return False
    if get_board(x+1,y+1) == '0' and legal_pos(square, i_to_s(x+1,y+1), side) :
        return False
    if get_board(x+1,y-1) == '0' and legal_pos(square, i_to_s(x+1,y-1), side) :
        return False
    if get_board(x,y+1) == '0' and legal_pos(square, i_to_s(x,y+1), side) :
        return False
    if get_board(x,y-1) == '0' and legal_pos(square, i_to_s(x,y-1), side) :
        return False
    if get_board(x-1,y+1) == '0' and legal_pos(square, i_to_s(x-1,y+1), side) :
        return False
    if get_board(x-1,y-1) == '0' and legal_pos(square, i_to_s(x-1,y-1), side) :
        return False
    if len(square_attacked(square,side)) == 3 : #If double check it is checkmate
        return True
    attacker_square = attackers[1][1:]
    attacker_piece = attackers[1][0]
    #Capture the attacking piece?
    a = square_attacked(attacker_square, side)
    if a[0]== True and a[1][0] != 'K':
        return False
    #Block Check king is on x,y, attacker on x1,y1
    if attacker_piece == 'B' or attacker_piece == 'Q':
        x_1 = ord(attacker_square[0])-97
        y_1 = ord(attacker_square[1])-49
        if(y>y_1 and x>x_1):                        #diagonal 1
            for i in range (1,abs(y-y_1)) :
                if square_attacked(i_to_s(x_1+i,y_1+i), side)[0]  : 
                    return False
        elif(y<y_1 and x>x_1):                      #diagonal 2
            for i in range (1,abs(y-y_1)) :
                if square_attacked(i_to_s(x_1+i,y_1-i), side)[0]  : 
                    return False
        elif(y<y_1 and x<x_1):                      #diagonal 3
            for i in range (1,abs(y-y_1)) :
               if square_attacked(i_to_s(x_1-i,y_1-i), side)[0]  : 
                    return False
        elif(y>y_1 and x<x_1):                      #diagonal 4
            for i in range (1,abs(y-y_1)) :
                if square_attacked(i_to_s(x_1-i,y_1+i), side)[0]  :
                    return False
                
    if attacker_piece == 'R' or attacker_piece == 'Q':
        if x_1 == x :
            for i in range (sign(y-y_1), y-y_1, sign(y-y_1)) :
                if square_attacked(i_to_s(x_1,y_1+i,side))[0] :
                    return False
        elif y_1 == y :
            for i in range (sign(x-x_1), x-x_1, sign(x-x_1)) :
                if square_attacked(i_to_s(x_1+i,y_1,side))[0] :
                    return False
    return True

def stalemate(turn) :
    if check(turn) :
        return False
    for i in range (8) :
        for j in range (8) :
            if board[i][j][0] == turn :
                continue
            attackers = square_attacked(i_to_s(i,j), turn)
            for k in range (1,len(attackers)) :
                if legal_pos(attackers[k][-2:], i_to_s(i,j),turn) :
                    return False
    return True
            
            
def Kside_castle(turn) :
    global castling_W
    global castling_B
    if turn == 'W' :       
        if castling_W[0] == 0 :
            return False
        if board[5][0] != '0' or board[6][0] != '0' :
            return False
        if square_attacked('f1','B')[0] or square_attacked('g1','B')[0] :
            return False
        if check(turn):
            return False
    elif turn == 'B' :       
        if castling_B[0] == 0 :
            return False
        if board[5][7] != '0' or board[6][7] != '0' :
            return False
        if square_attacked('f8','W')[0] or square_attacked('g8','W')[0] :
            return False
        if check(turn):
            return False
    return True

def Qside_castle(turn) :
    global castling_W
    global castling_B
    if turn == 'W' :       
        if castling_W[1] == 0 :
            return False
        if board[1][0] != '0' or board[2][0] != '0' or board[3][0] != '0' :
            return False
        if square_attacked('b1','B')[0] or square_attacked('c1','B')[0] or \
           square_attacked('d1','B')[0] :
            return False
        if check(turn):
            return False
    elif turn == 'B' :       
        if castling_B[0] == 0 :
            return False
        if board[1][7] != '0' or board[2][7] != '0' or board[3][7] != '0' :
            return False
        if square_attacked('b8','W')[0] or square_attacked('c8','W')[0] or \
           square_attacked('d8','W')[0] :
            return False
        if check(turn):
            return False
    return True

def get_castle_rights(turn):
    global castling_B
    global castling_W
    if turn == 'W' or turn == 'w':
        return castling_W
    elif turn == 'B' or turn == 'b' :
        return castling_B

def edit_castle_rights(a,b,c,d):
    global castling_B
    global castling_W
    castling_W = [a,b]
    castling_B =[c,d]
    
                        
def print_position():
    for i in range (8):
        for j in range (8):
            print(board[j][7-i], "\t", end=" ")
        print()
    print()
board = initial_position()



