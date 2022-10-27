import pygame

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager


FONT_STYLE = "freesansbold.ttf"

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
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()

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

    def update_score(self):
        self.score += 1
        if self.score > self.highest_score:
            self.highest_score = self.score
        
        if self.score % 100 == 0:
            self.game_speed += 2

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255)) #Também aceita código hexadecimal "#FFFFFF"
        self.draw_background()
        self.obstacle_manager.draw(self.screen)
        self.player.draw(self.screen)
        self.draw_score()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_score(self):
        self.format_text(pygame.font.Font(FONT_STYLE, 22), f"Score: {self.score}", True, (0,0,0), (1000, 50))

    def format_text(self, font, text, antialias, text_color, center):
        render_text = font.render(text, antialias, text_color)
        text_rect = render_text.get_rect()
        text_rect.center = center
        self.screen.blit(render_text , text_rect)

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.game_speed = 20
                self.score = 0
                self.run()

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        half_screen_width = SCREEN_WIDTH//2
        half_screen_height = SCREEN_HEIGHT/2
        if self.death_count == 0:
            self.format_text(pygame.font.Font(FONT_STYLE, 22),"Press any key to start", True, (0,0,0), (half_screen_width, half_screen_height))
        else:
            
            self.format_text(pygame.font.Font(FONT_STYLE, 22),"Press any key to restart", True, (0,0,0), (half_screen_width, half_screen_height))
            self.format_text(pygame.font.Font(FONT_STYLE, 22),f"Deaths: {self.death_count}", True, (0,0,0), (half_screen_width, half_screen_height+50))
            self.format_text(pygame.font.Font(FONT_STYLE, 22),f"Score: {self.score}", True, (0,0,0), (half_screen_width, half_screen_height+100))
            self.format_text(pygame.font.Font(FONT_STYLE, 22),f"Highest Score: {self.highest_score}", True, (0,0,0), (half_screen_width, half_screen_height+150))

            self.screen.blit(ICON, (half_screen_width - 20, half_screen_height - 140))
        pygame.display.update()
        self.handle_events_on_menu()