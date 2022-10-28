import pygame
import random
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.power_ups.power_up import PowerUp
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, HEART, CLOUD, GAME_OVER, RESET
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.utils.text_utils import draw_message_component
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.score = 0
        self.death_count = 0
        self.highest_score = 0
        self.heart_count = 3
        self.clouds = []
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        self.game_speed = 20
        self.score = 0
        self.heart_count = 3
        while self.playing:
            self.events()
            self.update()
            self.draw()   

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.obstacle_manager.update(self)
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.update_score()
        self.power_up_manager.update(self.score, self.game_speed, self.player)

    def update_score(self):
        self.score += 1
        if self.score > self.highest_score:
            self.highest_score = self.score
        
        if self.score % 100 == 0:
            self.game_speed += 2

        self.draw_score()

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255)) #Também aceita código hexadecimal "#FFFFFF"
        self.draw_background()
        self.obstacle_manager.draw(self.screen)
        self.player.draw(self.screen)
        self.draw_power_up_time()
        self.draw_score()
        self.draw_heart()
        self.power_up_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_heart(self):
        for heart_pos in range(self.heart_count):
            self.screen.blit(HEART, (900 - (30 * heart_pos), 40))

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if len(self.clouds) <= 2:
            self.clouds.append(self.screen.blit(CLOUD, (random.randint(1000,2000), random.randint(100,300))))
        else:
            for cloud in self.clouds:
                if cloud.x < 0:
                    self.clouds.remove(cloud)
                else:
                    cloud.x -= 20
                self.screen.blit(CLOUD, (cloud.x, cloud.y))
                    
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        draw_message_component(f"Score: {self.score}", self.screen, font_color=(0,0,255), pos_x_center = 1000, pos_y_center = 50)

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                draw_message_component(f"{self.player.type.capitalize()} enabled for {time_to_show} seconds.",
                                        self.screen,
                                        font_color = (0,255,0),
                                        font_size = 18,
                                        pos_x_center = 500,
                                        pos_y_center = 40
                )
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_width = SCREEN_WIDTH//2
        half_screen_height = SCREEN_HEIGHT/2
        if self.death_count == 0:
            draw_message_component("Press any key to start", self.screen, pos_y_center = half_screen_height)
        else:
            draw_message_component("Press any key to restart", self.screen, pos_y_center = half_screen_height)

            draw_message_component(f"Deaths: {self.death_count}", self.screen, font_color=(255,0,0),pos_x_center = half_screen_width, pos_y_center = half_screen_height + 50)
            draw_message_component(f"Score: {self.score}", self.screen, font_color=(0,0,255), pos_x_center = half_screen_width, pos_y_center = half_screen_height + 100)
            draw_message_component(f"Highest score: {self.highest_score}", self.screen, font_color=(255,0,255), pos_x_center = half_screen_width, pos_y_center = half_screen_height + 150)

            self.screen.blit(ICON, (half_screen_width - 20, half_screen_height - 140))
            self.screen.blit(GAME_OVER, (half_screen_width - 175, 100))
            self.screen.blit(RESET, (half_screen_width - 50, half_screen_height + 200))

        pygame.display.update()
        self.handle_events_on_menu()