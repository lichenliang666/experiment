import arcade

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "My Arcade Project")

    def on_draw(self):
        self.clear()
        arcade.draw_text("Hello Arcade!", 100, 100, arcade.color.WHITE, 24)

if __name__ == "__main__":
    game = MyGame()
    arcade.run()
