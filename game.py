class Object:
    def __init__(self, xy, size):
        self.rect = Rect(xy, size)
    
    def collide_borders(self, object2):

        clipped_line = self.clipline(line)

        if clipped_line:
            # If clipped_line is not an empty tuple then the line
            # collides/overlaps with the rect. The returned value contains
            # the endpoints of the clipped line.
            start, end = clipped_line
            x1, y1 = start
            x2, y2 = end
        else:
            print("No clipping. The line is fully outside the rect.")


