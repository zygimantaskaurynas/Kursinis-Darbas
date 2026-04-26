import pygame
import csv
import random
from abc import ABC, abstractmethod

# 1. BAZINĖS KLASĖ (Abstrakcija)
class GameObject(ABC):
    def __init__(self, x, y, width, height, color):
        # Inkapsuliacija: _rect yra apsaugotas (protected) kintamasis
        self._rect = pygame.Rect(x, y, width, height)
        self.color = color

    @abstractmethod
    def update(self): 
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self._rect)

# 2. SUB-KLASĖS (Paveldėjimas ir Polimorfizmas)
class Paddle(GameObject):
    def __init__(self, x, y, color, up_keys, down_keys):
        super().__init__(x, y, 15, 90, color)
        self.initial_x, self.initial_y = x, y
        self.speed = 10
        self.keys = (up_keys[0] if isinstance(up_keys, list) else up_keys, 
                     down_keys[0] if isinstance(down_keys, list) else down_keys)

    def update(self):
        keys = pygame.key.get_pressed()
        direction = keys[self.keys[1]] - keys[self.keys[0]]
        self._rect.y = max(0, min(600 - self._rect.height, self._rect.y + direction * self.speed))

    def reset(self):
        self._rect.x = self.initial_x
        self._rect.y = self.initial_y
        self._rect.height = 90
        self.speed = 10

class Ball(GameObject):
    def __init__(self, x, y, color):
        super().__init__(x, y, 15, 15, color)
        self.speed_x = self.speed_y = 5
        self.is_golden = False

    def update(self):
        limit = 15 if self.is_golden else 10
        self.speed_x = max(-limit, min(limit, self.speed_x))
        self.speed_y = max(-limit, min(limit, self.speed_y))

        self._rect.x += self.speed_x
        self._rect.y += self.speed_y
        
        if self._rect.top <= 0 or self._rect.bottom >= 600:
            self.speed_y *= -1

    def reset(self):
        self.is_golden = False
        self._rect.size = (15, 15)
        self._rect.center = (400, 300)
        self.speed_x = 5 * (1 if self.speed_x < 0 else -1)
        self.speed_y = 5

class GoldenPoint(GameObject):
    def __init__(self):
        super().__init__(0, 0, 30, 30, (255, 215, 0))
        self.active = False

    def spawn(self):
        self._rect.topleft = (random.randint(200, 600), random.randint(100, 500))
        self.active = True

    def update(self): 
        pass

# 3. (Singleton ir State Patterns)
class GameManager:
    _instance = None

    # Singleton šablonas
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized: 
            return
            
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("OOP Ping Pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 50)
        
        self.ball = Ball(400, 300, (255, 255, 255))
        self.left_paddle = Paddle(20, 250, (0, 0, 255), pygame.K_w, pygame.K_s)
        self.right_paddle = Paddle(760, 250, (255, 0, 0), pygame.K_UP, pygame.K_DOWN)
        self.gp = GoldenPoint()
        
        self.scores = [0, 0] 
        self.state = "COUNTDOWN" # Būsenos (State) pradžia
        self.timer = pygame.time.get_ticks()
        self.gp_spawned = False
        self.last_hit_by = "left" # Numatytasis, kad išvengtume klaidų
        
        self.high_score = self.load_high_score()

        self._initialized = True

    def save_results(self):
        try:
            with open('scores.csv', 'a', newline='', encoding='utf-8') as f:
                csv.writer(f).writerow(["BLUE", self.scores[0], "RED", self.scores[1]])
        except:
            pass

    def load_high_score(self):
        max_diff = 0
        try:
            with open('scores.csv', 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 4:
                        try:
                            s1 = int(row[1])
                            s2 = int(row[3])
                            # abs() užtikrina, kad skirtumas visada būtų teigiamas - modulis
                            diff = abs(s1 - s2)
                            if diff > max_diff:
                                max_diff = diff
                        except ValueError:
                            pass
        except FileNotFoundError:
            pass
        return max_diff

    def run(self):
        while True:
            self.screen.fill((20, 20, 20))
            for e in pygame.event.get():
                if e.type == pygame.QUIT: 
                    return pygame.quit()

            now = pygame.time.get_ticks()

            
            # BŪSENA 1: COUNTDOWN
            
            if self.state == "COUNTDOWN":
                timepassed = (now - self.timer) // 1000
                timeshow = 3 - timepassed
                
                if timeshow <= 0:
                    self.state = "PLAYING"
                    self.timer = now
                else:
                    text = self.big_font.render(f"GAME STARTS IN: {timeshow}", True, (255, 255, 255))
                    self.screen.blit(text, text.get_rect(center=(400, 300)))

            
            # BŪSENA 2: PLAYING
            
            elif self.state == "PLAYING":
                # Polimorfizmas
                self.ball.update()
                self.left_paddle.update()
                self.right_paddle.update()

                # Raketės susidūrimai
                if self.ball._rect.colliderect(self.left_paddle._rect):
                    self.ball.speed_x *= -1.1
                    self.ball._rect.left = self.left_paddle._rect.right
                    self.last_hit_by = "left"
                
                if self.ball._rect.colliderect(self.right_paddle._rect):
                    self.ball.speed_x *= -1.1
                    self.ball._rect.right = self.right_paddle._rect.left
                    self.last_hit_by = "right"

                # Auksinis taškas - Atsiradimas
                if not self.gp_spawned and (now - self.timer > 8000):
                    self.gp.spawn()
                    self.gp_spawned = True

                # Auksinis taškas - 3 EFEKTAI
                if self.gp.active and self.ball._rect.colliderect(self.gp._rect):
                    self.gp.active = False
                    
                    # Nustatome, kas pataikė (hitter) ir kas ginasi (opponent)
                    if self.last_hit_by == "left":
                        hitter, opponent = self.left_paddle, self.right_paddle
                    else:
                        hitter, opponent = self.right_paddle, self.left_paddle

                    # Parenkamas atsitiktinis efektas iš 3 variantų
                    effect = random.choice([1, 2, 3])

                    if effect == 1:
                        # 1) Padidėja raketės greitis 2x (Tam, kuris atmušė)
                        hitter.speed *= 2
                    
                    elif effect == 2:
                        # 2) Priešininko raketė sumažėja 2x
                        opponent._rect.height //= 2
                    
                    elif effect == 3:
                        # 3) Kamuoliukas padidėja 2x, greitis 1.3x, taškai 2 vietoj 1
                        self.ball.is_golden = True
                        self.ball._rect.inflate(15, 15) # Padidina nuo 15 iki 30
                        self.ball.speed_x *= 1.3
                        self.ball.speed_y *= 1.3

                # Taškų skaičiavimas
                reward = 2 if self.ball.is_golden else 1
                
                if self.ball._rect.left <= 0:
                    self.scores[1] += reward
                    self.reset_round()
                
                if self.ball._rect.right >= 800:
                    self.scores[0] += reward
                    self.reset_round()

                # Laimėtojo tikrinimas
                if max(self.scores) >= 6:
                    self.save_results()
                    self.state = "GAME_OVER"

                # Piešimas ekrane
                self.ball.draw(self.screen)
                self.left_paddle.draw(self.screen)
                self.right_paddle.draw(self.screen)
                if self.gp.active: 
                    self.gp.draw(self.screen)
                
                score_text = self.font.render(f"{self.scores[0]} : {self.scores[1]}", True, (255, 255, 255))
                self.screen.blit(score_text, (370, 20))

            
            # BŪSENA 3: GAME OVER
            
            elif self.state == "GAME_OVER":
                winner = "BLUE PLAYER" if self.scores[0] >= 6 else "RED PLAYER"
                
                win_img = self.big_font.render(f"{winner} WON!", True, (255, 215, 0))
                self.screen.blit(win_img, win_img.get_rect(center=(400, 250)))
                
                res_text = f"Final Result: {self.scores[0]} - {self.scores[1]}"
                res_img = self.font.render(res_text, True, (255, 255, 255))
                self.screen.blit(res_img, res_img.get_rect(center=(400, 320)))

                hs_text = self.font.render(f"Max Diff: {self.high_score}", True, (255, 215, 0))
                self.screen.blit(hs_text, (20, 20))
                
            pygame.display.flip()
            self.clock.tick(60)

    def reset_round(self):
        self.ball.reset()
        self.left_paddle.reset()
        self.right_paddle.reset()
        self.gp.active = False
        self.gp_spawned = False
        self.timer = pygame.time.get_ticks()

if __name__ == "__main__":
    game = GameManager()
    game.run()
