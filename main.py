import random
from pygame import Rect

# =========================================================
# GENERAL CONFIG
# =========================================================
WIDTH = 800
HEIGHT = 450
TITLE = "Dinosaur Kingdom"

FPS = 60

SPRITE_WIDTH = 120
SPRITE_HEIGHT = 120

HITBOX_WIDTH = 60
HITBOX_HEIGHT = 70

GROUND_HEIGHT = 50
GROUND_Y = HEIGHT - GROUND_HEIGHT

GRAVITY = 0.6
JUMP_FORCE = -11

PLAYER_FOOT_OFFSET = 42
ENEMY_FOOT_OFFSET = 62

ENEMY_SEPARATION_DISTANCE = 80
ENEMY_SEPARATION_FORCE = 0.4

COLOR_GRAY = (70, 70, 70)
COLOR_GREEN = (60, 160, 60)
COLOR_RED = (160, 60, 60)


# =========================================================
# GAME STATES
# =========================================================
STATE_MENU = 0
STATE_PLAYING = 1
STATE_WIN = 2
STATE_GAME_OVER = 3


# =========================================================
# ANIMATION
# =========================================================
class AnimatedSprite:
    def __init__(self, images, fps):
        self.images = images
        self.fps = fps
        self.frame_index = 0
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer >= FPS // self.fps:
            self.timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.images)

    def get_image(self):
        return self.images[self.frame_index]


# =========================================================
# PLAYER
# =========================================================
class Player:
    def __init__(self):
        self.idle_animation = AnimatedSprite(
            ["hero_idle_0", "hero_idle_1"], 4
        )
        self.run_animation = AnimatedSprite(
            ["hero_run_0", "hero_run_1"], 8
        )
        self.reset()

    def reset(self):
        self.x = 100
        self.y = GROUND_Y - (SPRITE_HEIGHT - PLAYER_FOOT_OFFSET)
        self.velocity_y = 0
        self.speed = 4
        self.on_ground = True
        self.current_animation = self.idle_animation

    def get_hitbox(self):
        return Rect(
            self.x + (SPRITE_WIDTH - HITBOX_WIDTH) / 2,
            self.y + SPRITE_HEIGHT - HITBOX_HEIGHT,
            HITBOX_WIDTH,
            HITBOX_HEIGHT
        )

    def update(self):
        is_moving = False

        if keyboard.left:
            self.x -= self.speed
            is_moving = True
        if keyboard.right:
            self.x += self.speed
            is_moving = True

        self.x = max(0, min(WIDTH - SPRITE_WIDTH, self.x))

        if keyboard.space and self.on_ground:
            self.velocity_y = JUMP_FORCE
            self.on_ground = False
            Game.play_sound("jump")

        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        if self.y + SPRITE_HEIGHT - PLAYER_FOOT_OFFSET >= GROUND_Y:
            self.y = GROUND_Y - (SPRITE_HEIGHT - PLAYER_FOOT_OFFSET)
            self.velocity_y = 0
            self.on_ground = True

        self.current_animation = (
            self.run_animation if is_moving else self.idle_animation
        )
        self.current_animation.update()

    def draw(self):
        screen.blit(self.current_animation.get_image(), (self.x, self.y))


# =========================================================
# ENEMY
# =========================================================
class Enemy:
    def __init__(self, x):
        self.x = x
        self.y = GROUND_Y - (SPRITE_HEIGHT - ENEMY_FOOT_OFFSET)

        self.base_speed = random.choice([-1.0, 1.0])
        self.velocity = self.base_speed

        self.animation = AnimatedSprite(["enemy_0", "enemy_1"], 2)
        self.is_alive = True

    def get_hitbox(self):
        return Rect(
            self.x + (SPRITE_WIDTH - HITBOX_WIDTH) / 2,
            self.y + SPRITE_HEIGHT - HITBOX_HEIGHT,
            HITBOX_WIDTH,
            HITBOX_HEIGHT
        )

    def update(self, player, enemies):
        if not self.is_alive:
            return

        distance_x = player.x - self.x
        if abs(distance_x) < 220:
            self.base_speed = 1.0 if distance_x > 0 else -1.0

        separation_force = 0
        for other in enemies:
            if other is self or not other.is_alive:
                continue

            delta = self.x - other.x
            if abs(delta) < ENEMY_SEPARATION_DISTANCE:
                separation_force += (
                    ENEMY_SEPARATION_FORCE if delta > 0 else -ENEMY_SEPARATION_FORCE
                )

        self.velocity = self.base_speed + separation_force
        self.velocity = max(-1.6, min(1.6, self.velocity))
        self.x += self.velocity

        if self.x <= 0 or self.x >= WIDTH - SPRITE_WIDTH:
            self.base_speed *= -1

        if abs(self.velocity) > 0.1:
            self.animation.update()

    def draw(self):
        if self.is_alive:
            screen.blit(self.animation.get_image(), (self.x, self.y))


# =========================================================
# UI
# =========================================================
class Button:
    def __init__(self, text, x, y, action, color=COLOR_GRAY):
        self.text = text
        self.rect = Rect((x, y), (260, 50))
        self.action = action
        self.color = color

    def draw(self):
        screen.draw.filled_rect(self.rect, self.color)
        screen.draw.text(
            self.text,
            center=self.rect.center,
            fontsize=32,
            color="white"
        )

    def handle_click(self, position):
        if self.rect.collidepoint(position):
            self.action()


# =========================================================
# GAME CONTROLLER
# =========================================================
class Game:
    state = STATE_MENU
    sound_enabled = True

    player = Player()
    enemies = []

    @staticmethod
    def play_sound(name):
        if Game.sound_enabled:
            getattr(sounds, name).play()

    @staticmethod
    def start_game():
        Game.player.reset()
        Game.enemies = [Enemy(420), Enemy(650), Enemy(720)]
        Game.state = STATE_PLAYING
        if Game.sound_enabled:
            music.play("background")

    @staticmethod
    def player_died():
        Game.play_sound("hit")
        music.stop()
        Game.state = STATE_GAME_OVER

    @staticmethod
    def win_game():
        music.stop()
        Game.state = STATE_WIN

    @staticmethod
    def toggle_sound():
        Game.sound_enabled = not Game.sound_enabled

        if not Game.sound_enabled:
            music.stop()

        sound_button.text = (
            "Sound: ON" if Game.sound_enabled else "Sound: OFF"
        )
        sound_button.color = (
            COLOR_GREEN if Game.sound_enabled else COLOR_RED
        )


# =========================================================
# BUTTONS
# =========================================================
sound_button = Button(
    "Sound: ON",
    270,
    230,
    Game.toggle_sound,
    COLOR_GREEN
)

buttons = [
    Button("Start Game", 270, 160, Game.start_game),
    sound_button,
    Button("Exit", 270, 300, quit),
]

win_button = Button(
    "Back to Menu", 270, 280, lambda: setattr(Game, "state", STATE_MENU)
)


# =========================================================
# MAIN LOOP
# =========================================================
def update():
    if Game.state != STATE_PLAYING:
        return

    Game.player.update()

    for enemy in Game.enemies:
        enemy.update(Game.player, Game.enemies)

        if enemy.is_alive and Game.player.get_hitbox().colliderect(enemy.get_hitbox()):
            if Game.player.velocity_y > 0 and Game.player.y < enemy.y:
                enemy.is_alive = False
                Game.player.velocity_y = -7
                Game.play_sound("enemy_die")
            else:
                Game.player_died()

    if all(not enemy.is_alive for enemy in Game.enemies):
        Game.win_game()


def draw():
    screen.clear()

    if Game.state == STATE_MENU:
        screen.draw.text(
            "Reino dos Dinossauros",
            center=(WIDTH // 2, 90),
            fontsize=52,
            color="white"
        )
        for button in buttons:
            button.draw()

    elif Game.state == STATE_PLAYING:
        screen.draw.filled_rect(
            Rect((0, GROUND_Y), (WIDTH, GROUND_HEIGHT)),
            (100, 200, 100)
        )
        Game.player.draw()
        for enemy in Game.enemies:
            enemy.draw()

    elif Game.state == STATE_WIN:
        screen.draw.text(
            "Parab\u00e9ns! Voc\u00ea venceu!",
            center=(WIDTH // 2, 160),
            fontsize=56,
            color="yellow"
        )
        win_button.draw()

    elif Game.state == STATE_GAME_OVER:
        screen.draw.text(
            "Voc\u00ea perdeu!",
            center=(WIDTH // 2, 160),
            fontsize=56,
            color="red"
        )
        win_button.draw()


def on_mouse_down(pos):
    if Game.state == STATE_MENU:
        for button in buttons:
            button.handle_click(pos)
    elif Game.state == STATE_WIN or Game.state == STATE_GAME_OVER:
        win_button.handle_click(pos)
