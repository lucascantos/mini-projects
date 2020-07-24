import pygame

class Bodypart(pygame.sprite.Sprite):
    def __init__(self):
        pass

class Eyes(Bodypart):
    def __init__(self):
        pass

class Mouth(Bodypart):
    def __init__(self):
        pass

class Face(Bodypart):
    def __init__(self):
        self.eyes = Eyes()
        self.mouth = Mouth()
class Feature(Bodypart):
    def __init__(self):
        pass

class Head(Bodypart):
    def __init__(self):
        self.face = Face()
        self.top_feature = Feature()
        self.side_feature = Feature()

class Race(Bodypart):
    def __init__(self):
        pass

my_character = {
    'head': 0,
    'body': 0,
    'eyes': 0,
    'mouth': 1,
    'head_features': [None, None],
}