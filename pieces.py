import pygame
import os

SPRITE_DIR = os.path.join(os.path.dirname(__file__), "pieces")
_cache = {}

def _load(name):
    if name not in _cache:
        _cache[name] = pygame.image.load(os.path.join(SPRITE_DIR, name)).convert_alpha()
    return _cache[name]
class Pieces:

    #WhitePiece
    B = pygame.image.load("pieces/wB.png")
    H = pygame.image.load("pieces/wH.png")
    K = pygame.image.load("pieces/wK.png")
    P = pygame.image.load("pieces/wP.png")
    Q = pygame.image.load("pieces/wQ.png")
    R = pygame.image.load("pieces/wR.png")

    #BlackPieces
    b = pygame.image.load("pieces/bB.png")
    h = pygame.image.load("pieces/bH.png")
    k = pygame.image.load("pieces/bK.png")
    p = pygame.image.load("pieces/bP.png")
    q = pygame.image.load("pieces/bQ.png")
    r = pygame.image.load("pieces/bR.png")

    def __init__(self, pawn_name: str, team: int = 2):
        self.code = pawn_name
        self.team = team

    def getImage(pawnName):
        d = {"B":Pieces.B,"N":Pieces.H,"K":Pieces.K,"P":Pieces.P,"Q":Pieces.Q,"QR":Pieces.R,"KR":Pieces.R,
             "b":Pieces.b,"n":Pieces.h,"k":Pieces.k,"p":Pieces.p,"q":Pieces.q,"kr":Pieces.r,"qr":Pieces.r}
        return d[pawnName]

