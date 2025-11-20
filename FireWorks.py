import pygame
import random
import math

# --- ثابت‌ها ---
WIDTH, HEIGHT = 1000, 700  # ابعاد بزرگتر
FPS = 60
GRAVITY = 0.15  # نیروی گرانش (کم برای ماندگاری بیشتر)
AIR_RESISTANCE = 0.985 # مقاومت هوا

# --- رنگ‌ها ---
BLACK = (0, 0, 0)

# --- کلاس ستاره برای پس‌زمینه (بدون تغییر) ---
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(1, 3)
        self.initial_brightness = random.randint(100, 255) 
        self.brightness = self.initial_brightness
        self.twinkle_speed = random.uniform(0.01, 0.05) 
        self.twinkle_offset = random.uniform(0, math.pi * 2) 
        self.twinkling = random.choice([True, True, False])

    def update(self):
        if self.twinkling:
            twinkle_factor = (math.sin(pygame.time.get_ticks() * self.twinkle_speed + self.twinkle_offset) + 1) / 2
            self.brightness = int(self.initial_brightness * (0.5 + twinkle_factor * 0.5))
            self.brightness = max(10, self.brightness) 

    def draw(self, surface):
        pygame.draw.circle(surface, (self.brightness, self.brightness, self.brightness), (self.x, self.y), self.size)

# --- کلاس ذره (Particle) (با دنباله) ---
class Particle:
    def __init__(self, x, y, color, type='spark', parent_color=None):
        self.x = x
        self.y = y
        self.color = color
        self.initial_color = color
        self.type = type 
        self.parent_color = parent_color if parent_color else color

        # --- تعریف ویژگی‌های اولیه بر اساس نوع ذره ---
        if self.type == 'trail':
            self.vx = random.uniform(-0.5, 0.5)
            self.vy = random.uniform(1, 2)
            self.radius = random.uniform(1, 2)
            self.lifetime = random.randint(5, 15)  
            
        elif self.type == 'spark':
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            self.vx = speed * math.cos(angle)
            self.vy = speed * math.sin(angle)
            self.radius = random.uniform(1.5, 3.5)
            self.lifetime = random.randint(100, 180) 
            self.trail_history = [] # !!! اضافه شده برای دنباله !!!

        elif self.type == 'pop':
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.5, 2)
            self.vx = speed * math.cos(angle)
            self.vy = speed * math.sin(angle)
            self.radius = random.uniform(0.5, 1.5)
            self.lifetime = random.randint(15, 30)
        
        self.current_lifetime = self.lifetime

    def update(self):
        # اعمال فیزیک
        self.vy += GRAVITY
        self.vx *= AIR_RESISTANCE
        self.vy *= AIR_RESISTANCE
        self.x += self.vx
        self.y += self.vy
        
        self.current_lifetime -= 1
        
        # تغییر رنگ (فقط برای ذرات اصلی spark)
        if self.type == 'spark':
            ratio = self.current_lifetime / self.lifetime
            r, g, b = self.initial_color
            
            self.color = (
                int(r * ratio),
                int(g * ratio),
                int(b * ratio * 0.5) 
            )
            self.color = tuple(max(0, min(255, c)) for c in self.color)
            
            # !!! به‌روزرسانی تاریخچه دنباله !!!
            self.trail_history.append((self.x, self.y))
            self.trail_history = self.trail_history[-5:] # نگه داشتن 5 موقعیت آخر

        # اگر ذره دنباله باشد، شعاعش را کم می‌کنیم
        if self.type == 'trail':
             self.radius = max(0, self.radius - 0.05)


    def draw(self, surface):
        if self.current_lifetime > 0:
            alpha = int(255 * (self.current_lifetime / self.lifetime))
            radius = int(self.radius) if self.radius > 0 else 1
            
            # !!! رسم دنباله جزیی برای ذرات اصلی (Spark) !!!
            if self.type == 'spark':
                for i, pos in enumerate(self.trail_history):
                    # شفافیت کمتر برای ذرات قدیمی‌تر در دنباله
                    trail_alpha = int(alpha * (i / len(self.trail_history)) * 0.5) 
                    trail_radius = max(1, radius - 1)
                    trail_surface = pygame.Surface((trail_radius * 2, trail_radius * 2), pygame.SRCALPHA)
                    # رنگ دنباله کمی روشن‌تر
                    pygame.draw.circle(trail_surface, self.initial_color, (trail_radius, trail_radius), trail_radius)
                    trail_surface.set_alpha(trail_alpha)
                    surface.blit(trail_surface, (int(pos[0] - trail_radius), int(pos[1] - trail_radius)))

            # --- رسم خود ذره اصلی ---
            particle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, self.color, (radius, radius), radius)
            particle_surface.set_alpha(alpha)
            
            surface.blit(particle_surface, (int(self.x - radius), int(self.y - radius)))

# --- کلاس موشک (Rocket) (بدون تغییر) ---
class Rocket:
    def __init__(self):
        self.x = random.randint(WIDTH // 4, 3 * WIDTH // 4)
        self.y = HEIGHT
        self.vy = random.uniform(-10, -18)
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.trail_color = (self.color[0]//2, self.color[1]//2, self.color[2]//2) 
        self.exploded = False
        self.explosion_height = random.randint(HEIGHT // 3, HEIGHT // 2)
        self.trail_particles = [] 
        
        self.explosion_type = random.choice(['sphere', 'heart', 'crackling', 'shell', 'ring', 'trail']) 

    def update(self):
        if not self.exploded:
            self.y += self.vy
            self.vy += GRAVITY * 0.7 
            
            if random.random() < 0.3: 
                self.trail_particles.append(Particle(self.x, self.y + random.randint(5, 15), self.trail_color, type='trail'))

            active_trail_particles = []
            for p in self.trail_particles:
                p.update()
                if p.current_lifetime > 0: 
                    active_trail_particles.append(p)
            self.trail_particles = active_trail_particles

            if self.vy >= 0 or self.y <= self.explosion_height:
                self.exploded = True
                return self.explode()
        return []

    def explode(self):
        particles = []
        
        if self.explosion_type == 'sphere':
            num_particles = random.randint(150, 250)
            for _ in range(num_particles):
                particles.append(Particle(self.x, self.y, self.color, type='spark'))
                
        elif self.explosion_type == 'heart':
            num_particles = 200
            scale = 4  
            heart_color = (255, 50, 50) 
            
            for i in range(num_particles):
                t = random.uniform(0, 2 * math.pi) 
                
                heart_x = scale * 16 * (math.sin(t) ** 3)
                heart_y = -scale * (13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) 
                
                speed_factor = random.uniform(0.1, 0.2)
                
                p = Particle(self.x, self.y, heart_color, type='spark')
                p.vx = heart_x * speed_factor
                p.vy = heart_y * speed_factor 
                p.lifetime = random.randint(100, 150)
                particles.append(p)
                
        elif self.explosion_type == 'crackling':
            num_particles = random.randint(80, 120)
            for _ in range(num_particles):
                p = Particle(self.x, self.y, self.color, type='spark')
                p.lifetime = random.randint(30, 60)
                particles.append(p)
                
        elif self.explosion_type == 'shell':
            num_shells = random.randint(3, 5)
            shell_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
            random.shuffle(shell_colors)
            
            for i in range(num_shells):
                shell_angle = (2 * math.pi / num_shells) * i + random.uniform(-0.5, 0.5)
                shell_speed = random.uniform(2, 4)
                shell_color = shell_colors[i % len(shell_colors)]
                num_sparks = random.randint(30, 50)
                
                for _ in range(num_sparks):
                    p = Particle(self.x, self.y, shell_color, type='spark')
                    p.vx = shell_speed * math.cos(shell_angle) + random.uniform(-1, 1)
                    p.vy = shell_speed * math.sin(shell_angle) + random.uniform(-1, 1)
                    particles.append(p)

        elif self.explosion_type == 'ring':
            num_particles = random.randint(150, 250)
            center_speed = random.uniform(3, 5)
            for _ in range(num_particles):
                angle = random.uniform(0, 2 * math.pi)
                p = Particle(self.x, self.y, self.color, type='spark')
                p.vx = center_speed * math.cos(angle) + random.uniform(-0.5, 0.5)
                p.vy = center_speed * math.sin(angle) + random.uniform(-0.5, 0.5)
                particles.append(p)
                
        elif self.explosion_type == 'trail':
            num_particles = random.randint(100, 150)
            low_speed = random.uniform(0.5, 1.5)
            
            for _ in range(num_particles):
                angle = random.uniform(0, 2 * math.pi)
                p = Particle(self.x, self.y, self.color, type='spark')
                
                p.lifetime = random.randint(200, 300)
                p.radius = random.uniform(0.8, 1.5)
                
                p.vx = low_speed * math.cos(angle)
                p.vy = low_speed * math.sin(angle)
                particles.append(p)
            
        return particles

    def draw(self, surface):
        if not self.exploded:
            for p in self.trail_particles:
                p.draw(surface)
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 4)

# --- تابع اصلی ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Firework Simulation (دنباله ذرات)")
    clock = pygame.time.Clock()

    stars = [Star() for _ in range(100)] 
    rockets = []
    particles = []
    
    running = True
    while running:
        # --- ورودی‌ها ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                rockets.append(Rocket())

        # --- بروزرسانی ---
        if random.random() < 0.015: 
             rockets.append(Rocket())
             
        for star in stars:
            star.update()
        
        active_rockets = []
        for rocket in rockets:
            new_particles = rocket.update()
            particles.extend(new_particles)
            if not rocket.exploded:
                active_rockets.append(rocket)
        rockets = active_rockets

        active_particles = []
        new_glitter_particles = []
        for p in particles:
            p.update()
            if p.current_lifetime > 0:
                active_particles.append(p)
                
                if p.type == 'spark' and p.current_lifetime < p.lifetime * 0.4 and random.random() < 0.05:
                    if random.random() < 0.7: 
                        for _ in range(random.randint(2, 5)):
                            new_glitter_particles.append(Particle(p.x, p.y, (255, 200, 0), type='pop')) 
                            
                if p.type == 'spark' and random.random() < 0.01:
                     new_glitter_particles.append(Particle(p.x, p.y, (255, 255, 200), type='pop')) 
            
        particles = active_particles
        particles.extend(new_glitter_particles)
        
        # --- رندرینگ (رسم) ---
        
        # !!! استفاده از سطح محوکننده برای ایجاد دنباله بصری !!!
        fade_color = (0, 0, 0, 20) # رنگ سیاه با شفافیت کم
        fade_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        fade_surface.fill(fade_color)
        screen.blit(fade_surface, (0, 0))
        
        for star in stars:
            star.draw(screen)

        for rocket in rockets:
            rocket.draw(screen)

        for p in particles:
            p.draw(screen)

        pygame.display.flip() 
        clock.tick(FPS) 

    pygame.quit()

if __name__ == "__main__":
    main()
