import pandas as pd 
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

positions_info = {
    'operational': {
        'positions': 8,
        'hours': 8,
        'rest': 12,     
        'start': 7,   
        },
    'nowcasting': {
        'positions': 2,
        'daily_min': 1,
        'hours': 12,
        'rest': 24,
        'start': 7,     
    },
    'nowcasting_night': {
        'positions': 2,
        'hours': 12,
        'rest': 24,  
        'start': 19,   
    },
    'tv':{
        'positions': 1,
        'hours': 8,
        'rest': 12,
        'start': 7,
    }}

employee = {
    'lucas': {
        'position': ['nowcasting'],
        'start': 7,
    },
    'maria': {
        'position': ['nowcasting'],
        'start': 19,
    },
    'joão': {
        'position': ['nowcasting_night'],
        'start': 7,
        'training': True
    },
    'bob': {
        'position': ['nowcasting_night'],
        'start': 19,
        'weekend': False
    }
}

class position(object):
    def __init__(self, daterange):
        self.shift_columns = daterange
        self.shift = np.ones(len(self.shift_columns))

    def shift_12h(self):
        for day in range(len(self.shift_columns)):
            if day%2==0:
                self.shift[day]=0

    def shift_8h(self):   
        for day in range(len(self.shift_columns)):
            if self.shift_columns[day].weekday() >=5:
                self.shift[day]=0

    def add_weekend(self, day_index):
        self.shift[day_index] = 1



def get_weekends(daterange):
    weekends = []
    for day in range(len(daterange)):
        if daterange[day].weekday() >=5:
            weekends.append(day)
    return weekends

first_day = datetime.today().replace(day=20)
last_day = first_day + relativedelta(months=+1)
shift_columns = pd.date_range(first_day, last_day, freq='D')

# get weekend's indexes
weekend_indexes = get_weekends(shift_columns) 
# loop
for i in range(positions_info['nowcasting']['positions']):
    shifts = []
    new_position = position(shift_columns)
    new_position.shift_8h()



# End loop


month = pd.DataFrame(shifts)



print(month)