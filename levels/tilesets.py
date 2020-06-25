def get_dicts(name):
    image_rows = {
            'p1_run_right': ((29,0), 2),  # rect, image count
            'p2_run_right': ((29,4), 2)
    }
    images = {
         'p1_idle': [(20,0)],# list of tuples
         'p2_idle': [(20,3)],
         'grass_tile': [(4,5)],
         'star_img': [(17,4)]
        }
    lvl_img = {
        'player1': {
            'run_left': 'p1_run_left',
            'run_right': 'p1_run_right',
            'idle': 'p1_idle'
            },
        'player2': {
            'run_left': 'p2_run_left',
            'run_right': 'p2_run_right',
            'idle': 'p2_idle'
            },
        'grass': {
            'ground_tile': 'grass_tile'
            },
        'bonus': {
            'star': 'star_img'
    }
        }

    if name == 'img':
        return images
    elif name == 'rows':
        return image_rows
    elif name == 'level':
        return lvl_img
