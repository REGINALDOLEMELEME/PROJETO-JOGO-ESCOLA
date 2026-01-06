import random
from pygame import Rect

# =========================================================
# CONFIGURAÇÕES GERAIS
# =========================================================
WIDTH = 800
HEIGHT = 450
TITLE = "Desvendando Reino dos Dinossauros"

FPS = 60
FOOT_OFFSET = 42

SPRITE_W = 120
SPRITE_H = 120

HITBOX_W = 60
HITBOX_H = 70

GROUND_HEIGHT = 50
GROUND_Y = HEIGHT - GROUND_HEIGHT

GRAVITY = 0.6
JUMP_FORCE = -11

ENEMY_SEPARATION_DIST = 80
ENEMY_SEPARATION_FORCE = 0.4

MENU_CONTROLS_TEXT = [
    "CONTROLES",
    "",
    "←  →   Mover",
    "ESPACO   Pular",
]



# =========================================================
# ESTADOS DO JOGO
# =========================================================
STATE_MENU = "Menu"
STATE_GAME = "Jogo"
STATE_WIN = "Venceu"


# =========================================================
# ANIMAÇÃO
# =========================================================
class AnimatedSprite:
    def __init__(self, images, fps):
        self.images = images
        self.fps = fps
        self.frame = 0
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer >= FPS // self.fps:
            self.timer = 0
            self.frame = (self.frame + 1) % len(self.images)

    def image(self):
        return self.images[self.frame]


# =========================================================
# PLAYER
# =========================================================
class Player:
    def __init__(self):
        self.idle = AnimatedSprite(["hero_idle_0", "hero_idle_1"], 4)
        self.run = AnimatedSprite(["hero_run_0", "hero_run_1"], 8)
        self.reset()

    def reset(self):
        self.x = 100
        self.y = GROUND_Y - (SPRITE_H - FOOT_OFFSET)
        self.vy = 0
        self.speed = 4
        self.on_ground = True
        self.anim = self.idle

    def hitbox(self):
        return Rect(
            self.x + (SPRITE_W - HITBOX_W) / 2,
            self.y + SPRITE_H - HITBOX_H,
            HITBOX_W,
            HITBOX_H
        )

    def update(self):
        moving = False

        if keyboard.left:
            self.x -= self.speed
            moving = True
        if keyboard.right:
            self.x += self.speed
            moving = True

        self.x = max(0, min(WIDTH - SPRITE_W, self.x))

        if keyboard.space and self.on_ground:
            self.vy = JUMP_FORCE
            self.on_ground = False
            Game.play_sound("jump")

        self.vy += GRAVITY
        self.y += self.vy

        if  self.y + SPRITE_H - FOOT_OFFSET >= GROUND_Y:
            self.y = GROUND_Y - (SPRITE_H - FOOT_OFFSET)
            self.vy = 0
            self.on_ground = True

        self.anim = self.run if moving else self.idle
        self.anim.update()

    def draw(self):
        screen.blit(self.anim.image(), (self.x, self.y))


# =========================================================
# ENEMY
# =========================================================
class Enemy:
    def __init__(self, x):
        self.x = x
        self.y = GROUND_Y - (SPRITE_H - FOOT_OFFSET)

        self.base_speed = random.choice([-1.0, 1.0])
        self.velocity = self.base_speed

        self.anim = AnimatedSprite(["enemy_0", "enemy_1"], 2)
        self.alive = True

    def hitbox(self):
        return Rect(
            self.x + (SPRITE_W - HITBOX_W) / 2,
            self.y + SPRITE_H - HITBOX_H,
            HITBOX_W,
            HITBOX_H
        )

    def update(self, player, enemies):
        if not self.alive:
            return

        # ---------- INTENÇÃO (perseguir player) ----------
        dx = player.x - self.x

        if abs(dx) < 220:
            self.base_speed = 1.0 if dx > 0 else -1.0

        # ---------- SEPARAÇÃO ----------
        separation = 0
        for other in enemies:
            if other is self or not other.alive:
                continue

            dist = self.x - other.x
            if abs(dist) < ENEMY_SEPARATION_DIST:
                separation += ENEMY_SEPARATION_FORCE if dist > 0 else -ENEMY_SEPARATION_FORCE

        # ---------- VELOCIDADE FINAL ----------
        self.velocity = self.base_speed + separation

        # clamp (remove “corrida”)
        self.velocity = max(-1.6, min(1.6, self.velocity))

        self.x += self.velocity

        # ---------- LIMITES DE TELA ----------
        if self.x <= 0:
            self.x = 0
            self.base_speed = abs(self.base_speed)

        elif self.x >= WIDTH - SPRITE_W:
            self.x = WIDTH - SPRITE_W
            self.base_speed = -abs(self.base_speed)

        # ---------- ANIMAÇÃO ----------
        if abs(self.velocity) > 0.1:
            self.anim.update()

    def draw(self):
        if self.alive:
            screen.blit(self.anim.image(), (self.x, self.y))

# =========================================================
# UI
# =========================================================
class Button:
    def __init__(self, text, x, y, action):
        self.text = text
        self.rect = Rect((x, y), (260, 50))
        self.action = action

    def draw(self):
        screen.draw.filled_rect(self.rect, (70, 70, 70))
        screen.draw.text(
            self.text,
            center=self.rect.center,
            fontsize=32,
            color="white"
        )

    def click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()


# =========================================================
# GAME (CONTROLE CENTRAL)
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
    def start():
        Game.player.reset()
        Game.enemies = [Enemy(420), Enemy(650), Enemy(700)]
        Game.state = STATE_GAME
        if Game.sound_enabled:
            music.play("background")

    @staticmethod
    def die():
        Game.play_sound("hit")
        music.stop()
        Game.state = STATE_MENU

    @staticmethod
    def win():
        music.stop()
        Game.state = STATE_WIN

    @staticmethod
    def toggle_sound():
        Game.sound_enabled = not Game.sound_enabled
        if not Game.sound_enabled:
            music.stop()
        buttons[1].text = "Sound: ON" if Game.sound_enabled else "Sound: OFF"


# =========================================================
# BOTÕES
# =========================================================
buttons = [
    Button("Começar Jogo", 270, 160, Game.start),
    Button("Som/Música: ON", 270, 230, Game.toggle_sound),
    Button("Sair", 270, 300, quit),
]

win_button = Button("Voltar ao Menu", 270, 280, lambda: setattr(Game, "state", STATE_MENU))


# =========================================================
# LOOP PRINCIPAL
# =========================================================
def update():
    if Game.state != STATE_GAME:
        return

    Game.player.update()

    for enemy in Game.enemies:
        enemy.update(Game.player, Game.enemies)

        if enemy.alive and Game.player.hitbox().colliderect(enemy.hitbox()):
            if Game.player.vy > 0 and Game.player.y < enemy.y:
                enemy.alive = False
                Game.player.vy = -7
                Game.play_sound("enemy_die")
            else:
                Game.die()

    if all(not e.alive for e in Game.enemies):
        Game.win()


def draw():
    screen.clear()

    if Game.state == STATE_MENU:
        screen.draw.text("Reino dos Dinossauros", center=(WIDTH // 2, 90),
                         fontsize=52, color="white")
        
        draw_menu_controls()

        for b in buttons:
            b.draw()

    elif Game.state == STATE_GAME:
        screen.draw.filled_rect(
            Rect((0, GROUND_Y), (WIDTH, GROUND_HEIGHT)),
            (100, 200, 100)
        )
        Game.player.draw()
        for enemy in Game.enemies:
            enemy.draw()

        if not Game.sound_enabled:
            screen.draw.text("Som/Música: OFF", topright=(WIDTH - 20, 20),
                             fontsize=24, color="white")

    elif Game.state == STATE_WIN:
        screen.draw.text("Parabéns - Você venceu!", center=(WIDTH // 2, 160),
                         fontsize=56, color="yellow")
        win_button.draw()


def on_mouse_down(pos):
    if Game.state == STATE_MENU:
        for b in buttons:
            b.click(pos)
    elif Game.state == STATE_WIN:
        win_button.click(pos)

def draw_menu_controls():
    start_y = 200
    line_height = 28

    for i, line in enumerate(MENU_CONTROLS_TEXT):
        screen.draw.text(
            line,
            center=(WIDTH // 2, start_y + i * line_height),
            fontsize=26 if i == 0 else 22,
            color="white"
        )
