class sm_button:
    def __init__(self, WIDTH, HEIGHT, x, y, text, color, action=None):
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        if action:
            self.action = action

    def action(self):
        print("WARNING: Button has no action attached")
