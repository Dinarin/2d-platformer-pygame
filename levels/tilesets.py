def get_dicts(name):
    image_rows = {
            'p1_run_right': ((28,0), 2),  # rect, image count
            'p2_run_right': ((28,3), 2)
    }
    images = {
         'p1_idle': [(19,0)],# list of tuples
         'p2_idle': [(19,3)],
         'grass_tile': [(3,4)],
         'floating_grass': [(1,4)],
         'star_img': [(16,3)]
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
        'ground_tile': {
            'grass': 'grass_tile'
            },
        'floating_tile': {
            'grass': 'floating_grass'
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
