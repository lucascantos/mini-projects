
martha = { # Frames are columns of sheet
    'file': 'src/assets/Martha.png',
    'type': 'sheet',
    'size': [32,32],
    'actions': {
        'idle':{
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
