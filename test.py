import unittest
import pygame
from PONG import Ball, GameManager 

class TestPingPong(unittest.TestCase):
    
    def setUp(self):
        pygame.init()
        self.ball = Ball(100, 100, (255, 255, 255))

    def test_ball_reset_position(self):
        #1 TESTAS: Tikriname, ar reset() funkcija grąžina kamuolį tiksliai į centrą.
        self.ball._rect.x = 999 
        self.ball._rect.y = 999
        self.ball.speed_x = 50
        self.ball.is_golden = True
        
        self.ball.reset()
        
        # Tikriname ar nutiko kas ir turėjo nutikt
        self.assertEqual(self.ball._rect.center, (400, 300))
        self.assertFalse(self.ball.is_golden)

    def test_ball_speed_limits(self):
        #2 TESTAS: Tikriname, ar veikia kamuoliuko greičio limitai update() metode.
        # Nustatome pernelyg didelį greitį
        self.ball.speed_x = 100
        self.ball.speed_y = -100
        self.ball.is_golden = False # Standartinis limitas yra 12!
        
        # Leidžiame kamuoliukui "pajudėti" ir pritaikyti limitus
        self.ball.update()
        
        # Greitis privalo būti apribotas iki
        self.assertEqual(self.ball.speed_x, 10)
        self.assertEqual(self.ball.speed_y, -10)

    def test_singleton_game_manager(self):
        #3 TESTAS: Tikriname, ar GameManager veikia pagal Singleton dizaino šabloną.
        game_instance_1 = GameManager()
        game_instance_2 = GameManager()
        
        # assertIs patikrina, ar abu kintamieji atmintyje yra tas pats objektas
        self.assertIs(game_instance_1, game_instance_2)

if __name__ == '__main__':
    unittest.main()
