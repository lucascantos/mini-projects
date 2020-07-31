from pygame import Vector2

characters = {
    'martha': { # Frames are columns of sheet
        'file': 'src/assets/martha.png',
        'type': 'sheet',
        'size': [32,32],
        'actions': {
            'idle':{
                'example': '[0.83,0.5, 1], 12',
                'frame': 1,
                'duration': None,
                'rock': False,
            },
            'walk': {
                'frame': range(0,3),
                'duration': [12,6,12],
                'rock': True,
            },
            'attack': {
                'frame': range(3,6),
                'duration': [10,6,12],
                'rock': False,
            },
        }
    }
}

tileset = {
    'file': 'src/assets/Tileset.png',
    'type': 'sheet',
    'size': [32,32],
    'elements': {
        'land':{
            'position': [0, 2],
        },
        'water': {
            'position': [1, 2],
        },
        'dirt': {
            'position': [3, 2],
        },
        'tree': {
            'position': [1, 1],
        },
        'rock': {
            'position': [2, 1],
        }
    }
}