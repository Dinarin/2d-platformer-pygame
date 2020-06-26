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
         'star_img': [(16,3)],
         'floating_snow': [(1,2)],
         'snow_tile': [(3,2)],
         'red_gem': [(17,9)]
        }
    player_img = {
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
    tileset = {
        'grass': {
            'ground_tile': 'grass_tile',
            'floating_tile': 'snow_tile',
            'bonus': 'star_img'
            },
        'snow': {
            'floating_tile': 'floating_snow',
            'ground_tile': 'snow_tile',
            'bonus': 'red_gem'
            }
}

    if name == 'img':
        return images
    elif name == 'rows':
        return image_rows
    elif name == 'level':
        return lvl_img
