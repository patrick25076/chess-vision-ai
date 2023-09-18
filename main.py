import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)
from dotenv import load_dotenv
import utils
import cv2 
import numpy as np
import pandas as pd
import time
from roboflow import Roboflow
import matplotlib.pyplot as plt
import numpy as np
import chess
from stockfish import Stockfish
import chess.svg
from cairosvg import svg2png

load_dotenv()

ROBOFLOW_API_KEY=os.getenv('ROBOFLOW_API_KEY') # -> your roboflow API key
STOCKFISH_PATH=os.getenv('STOCKFISH_PATH')  # -> your stockfish-path
IMAGE_PATH=r"data\94.jpeg" # -> your IMAGE PATH

label_id_to_class={
    8:'K',
    12:'R',
    11:'Q',
    7:'B',
    10:'P',
    9:'N',
    1:'b',
    3:'n',
    5:'q',
    4:'p',
    2:'k',
    6:'r'
}

stockfish=Stockfish(STOCKFISH_PATH)

def predict(path):
    """Predict the pieces on the chessboard using Roboflow pretrained model
       link: https://universe.roboflow.com/mywork-45pbb/chessv1-ghvlw

    Parameters:
    path (str) -- path to the rectified chessboard
    
    Returns:
    predictions (list) -- predictions containing all the pieces detected
    """

    rf = Roboflow(api_key=ROBOFLOW_API_KEY)
    project = rf.workspace().project("chessv1-ghvlw")
    model = project.version(3).model
    predictions=model.predict(path, confidence=70, overlap=60).json()
    predictions=predictions['predictions']
    model.predict(path, confidence=50, overlap=50).save("prediction.jpg")
    return predictions

def assign(predictions,squares):
    """Assigning the predictions bounding boxes to each square

    Parameters:
    predictions (list) -- predictions from Roboflow model
    squares (list) -- list with all 4 corner of all 64 squares
    
    Returns:
    sorted_dict (dict) -- dictionary containing the square associated with the piece detected in it
    """

    dict_={}
    for prediction in predictions:
        x , y ,_,_, piece = prediction['x'] , prediction['y'] , prediction['width'] , prediction['height'] , int(prediction['class'])
        for i,square in enumerate(squares.items()):
            tl , _ , _ ,br =square[1]
            min_x=tl[0]
            min_y=tl[1]
            max_x=br[0]
            max_y=br[1]
            if min_x<=x and max_x>=x and min_y<=y and max_y>=y:
                dict_[i+1]=label_id_to_class[piece]
                continue
    sorted_dict = dict(sorted(dict_.items()))
    return sorted_dict
            
def dict_to_fen(dictionary_of_pieces , white_moves):
    """Converting the dictionary with pieces and their square positions to FEN notation

    Parameters:
    dictionary_of_pieces (dict) -- dictionary of pieces and their square positions
    white_moves (bool) -- True if white moves , False if black moves

    Returns:
    fen (str) -- FEN notation of the chessboard
    link (str) -- Lichess link to analyze the game from that position
    """

    fen=''
    c=0
    for i in range(1,65):
        if i in dictionary_of_pieces.keys():
            if c>0:
                fen+=str(c)
            fen+=dictionary_of_pieces[i]
            c=0
        else:
            c=c+1
        if i%8==0:
            if c>0:
                fen+=str(c)
            c=0
            fen+=('/')
    fen=fen[:-1]
    if white_moves==True:
        fen_link=fen+"%20w"
        fen+=' w - - 0 1'
    else:
        fen_link=fen+r"%20b"
        fen+=' b - - 0 1'
    link='https://lichess.org/analysis/standard/'+fen_link
    return fen, link

def position_to_png(fen):
    """
    Convert FEN position to PNG image
    """

    board=chess.Board(fen=fen)
    boardsvg = chess.svg.board(board=board)
    outputfile = open('digital_board.svg', "w")
    outputfile.write(boardsvg)
    outputfile.close()
    svg2png(url='digital_board.svg' , write_to="output.png")

def get_best_move(fen):
    """Get the best move from Stockfish Engine

    Parameters:
    fen (str) - FEN notation of the chessboard

    Returns:
    best_move (str) -- The best move from the FEN position
    """
    
    stockfish.set_fen_position(fen)
    return stockfish.get_best_move()


if __name__ == "__main__":
    image=cv2.imread(IMAGE_PATH)
    squares,rectified_chessboard ,corners=utils.square_detection(image , False)
    path=utils.save_to_path('image','rectified_chessboard',rectified_chessboard)
    predictions=predict(path)
    img=cv2.imread(path)
    dict_=assign(predictions,squares)
    print(dict_)
    fen , link=dict_to_fen(dict_ , False)
    best_move=get_best_move(fen)
    position_to_png(fen)
    print(link)
    print(best_move) 
    digital_chessboard=cv2.imread('output.png')
    cv2.imshow('Digital_Table', digital_chessboard)
    cv2.waitKey(0)
    cv2.destroyAllWindows()





