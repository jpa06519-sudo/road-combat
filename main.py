import pygame
import random
import sys
import array
import math

# --- INICIALIZACIÓN ---
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Colores Arcade / Neon
NEGRO = (10, 10, 15)
GRIS_ASFALTO = (40, 40, 48)
BLANCO = (255, 255, 255)
AMARILLO = (255, 215, 0)
ROJO = (240, 40, 40)
AZUL = (40, 120, 255)
VERDE = (40, 220, 100)
NARANJA = (255, 120, 0)
MORADO = (160, 40, 240)
CIAN = (0, 230, 240)
ROSA_NEON = (255, 20, 147)

ANCHO = 400
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("ROAD COMBAT: JOSS CREATIONS EDITION")
reloj = pygame.time.Clock()

# --- DATOS DE AUTOS Y PROGRESO ---
monedas_totales = 0
auto_seleccionado = 0
volumen_global = 0.8

AUTOS_TIENDA = [
    {"nombre": "Rojo Novato", "color": ROJO, "vel": 5, "precio": 0, "comprado": True, "tipo_poder": "misil"},
    {"nombre": "Azul Escudo", "color": AZUL, "vel": 6, "precio": 850, "comprado": False, "tipo_poder": "escudo"},
    {"nombre": "Eco Magneto", "color": VERDE, "vel": 6, "precio": 2200, "comprado": False, "tipo_poder": "onda"},
    {"nombre": "Fuego Infernal", "color": NARANJA, "vel": 7, "precio": 4500, "comprado": False, "tipo_poder": "fuego"},
    {"nombre": "Laser Caos", "color": MORADO, "vel": 7, "precio": 8000, "comprado": False, "tipo_poder": "laser"},
    {"nombre": "Rayo Cian", "color": CIAN, "vel": 8, "precio": 14000, "comprado": False, "tipo_poder": "plasma"},
    {"nombre": "Escudo Dorado", "color": AMARILLO, "vel": 8, "precio": 22000, "comprado": False, "tipo_poder": "oro_escudo"},
    {"nombre": "Caza V-Diagonal", "color": (200, 200, 220), "vel": 8, "precio": 32000, "comprado": False, "tipo_poder": "diagonal"},
    {"nombre": "Titan Titanium", "color": (90, 90, 105), "vel": 9, "precio": 45000, "comprado": False, "tipo_poder": "pesado"},
    {"nombre": "GOD RIDER", "color": (255, 255, 255), "vel": 10, "precio": 0, "comprado": False, "tipo_poder": "god", "secreto": True}
]

# --- AUDIO ---
def generar_sonido(tipo):
    sample_rate = 22050
    duracion = 0.1 if tipo in ["moneda", "disparo", "dino"] else 0.35
    n_samples = int(sample_rate * duracion)
    buf = array.array('h', [0] * (n_samples * 2))
    
    for i in range(n_samples):
        if tipo == "moneda":
            val = int(math.sin(2 * math.pi * 900 * (i / sample_rate)) * 8000 * (1 - i / n_samples))
        elif tipo == "disparo":
            val = int(math.sin(2 * math.pi * (1400 - i * 3) * (i / sample_rate)) * 9000 * (1 - i / n_samples))
        elif tipo == "dino":
            freq = 1200 if (i / n_samples) < 0.5 else 1600
            val = int(math.sin(2 * math.pi * freq * (i / sample_rate)) * 9000)
        else:
            val = int((random.random() * 2 - 1) * 32767 * (1 - i / n_samples))
        buf[i * 2] = val
        buf[i * 2 + 1] = val
    snd = pygame.mixer.Sound(buffer=buf)
    snd.set_volume(volumen_global)
    return snd

def actualizar_volumen():
    sonido_choque.set_volume(volumen_global)
    sonido_moneda.set_volume(volumen_global)
    sonido_disparo.set_volume(volumen_global)
    sonido_dino.set_volume(volumen_global)

sonido_choque = generar_sonido("choque")
sonido_moneda = generar_sonido("moneda")
sonido_disparo = generar_sonido("disparo")
sonido_dino = generar_sonido("dino")

# --- SPRITES ---
def crear_imagen_auto(color_cuerpo, invertido=False, es_god=False):
    surf = pygame.Surface((40, 70), pygame.SRCALPHA)
    pygame.draw.rect(surf, (10, 10, 10), (2, 8, 8, 15), border_radius=3)
    pygame.draw.rect(surf, (10, 10, 10), (30, 8, 8, 15), border_radius=3)
    pygame.draw.rect(surf, (10, 10, 10), (2, 47, 8, 15), border_radius=3)
    pygame.draw.rect(surf, (10, 10, 10), (30, 47, 8, 15), border_radius=3)
    
    c_cuerpo = color_cuerpo if not es_god else ROSA_NEON
    pygame.draw.rect(surf, c_cuerpo, (6, 4, 28, 62), border_radius=6)
    
    if es_god:
        pygame.draw.rect(surf, AMARILLO, (6, 4, 28, 62), width=3, border_radius=6)
        pygame.draw.polygon(surf, CIAN, [(20, 10), (10, 35), (30, 35)])
    else:
        pygame.draw.rect(surf, (180, 240, 255), (10, 20, 20, 14), border_radius=2)
        pygame.draw.rect(surf, (180, 240, 255), (10, 42, 20, 8), border_radius=2)
        
    pygame.draw.rect(surf, AMARILLO, (8, 4, 6, 4), border_radius=1)
    pygame.draw.rect(surf, AMARILLO, (26, 4, 6, 4), border_radius=1)
    if invertido:
        surf = pygame.transform.rotate(surf, 180)
    return surf

def crear_imagen_jefe(tipo):
    surf = pygame.Surface((110, 120), pygame.SRCALPHA)
    if tipo == 0:
        pygame.draw.rect(surf, (50, 50, 55), (10, 10, 90, 100), border_radius=8)
        pygame.draw.rect(surf, ROJO, (15, 0, 80, 120), border_radius=10)
        pygame.draw.rect(surf, (20, 20, 20), (25, 20, 60, 25), border_radius=3)
        pygame.draw.rect(surf, AMARILLO, (20, 110, 15, 8))
        pygame.draw.rect(surf, AMARILLO, (75, 110, 15, 8))
    elif tipo == 1:
        puntos = [(55, 120), (0, 30), (30, 0), (80, 0), (110, 30)]
        pygame.draw.polygon(surf, MORADO, puntos)
        pygame.draw.polygon(surf, CIAN, puntos, 3)
        pygame.draw.circle(surf, ROSA_NEON, (55, 45), 18)
    elif tipo == 2:
        pygame.draw.rect(surf, (40, 50, 40), (10, 10, 90, 100), border_radius=5)
        pygame.draw.rect(surf, (70, 85, 65), (25, 25, 60, 70), border_radius=5)
        pygame.draw.rect(surf, (20, 20, 20), (50, 90, 10, 30))
        pygame.draw.rect(surf, NARANJA, (30, 5, 12, 6))
        pygame.draw.rect(surf, NARANJA, (68, 5, 12, 6))
    elif tipo == 3:
        pygame.draw.rect(surf, AMARILLO, (20, 10, 70, 105), border_radius=15)
        pygame.draw.rect(surf, NEGRO, (30, 25, 50, 35), border_radius=5)
        pygame.draw.line(surf, CIAN, (55, 0), (55, 120), 5)
    elif tipo == 4:
        pygame.draw.rect(surf, NARANJA, (10, 20, 90, 80), border_radius=6)
        pygame.draw.rect(surf, ROJO, (30, 0, 50, 115), border_radius=4)
        pygame.draw.circle(surf, AMARILLO, (55, 50), 16)
        pygame.draw.circle(surf, NEGRO, (55, 50), 8)
    elif tipo == 5: 
        pygame.draw.polygon(surf, AZUL, [(55, 0), (0, 70), (20, 115), (90, 115), (110, 70)])
        pygame.draw.polygon(surf, CIAN, [(55, 15), (15, 70), (30, 100), (80, 100), (95, 70)], 3)
        pygame.draw.rect(surf, BLANCO, (45, 40, 20, 35), border_radius=4)
    elif tipo == 6: 
        pygame.draw.rect(surf, (20, 80, 30), (5, 15, 100, 90), border_radius=12)
        pygame.draw.rect(surf, VERDE, (20, 5, 70, 110), border_radius=6)
        pygame.draw.circle(surf, AMARILLO, (35, 45), 10)
        pygame.draw.circle(surf, AMARILLO, (75, 45), 10)
    else:  
        pygame.draw.polygon(surf, BLANCO, [(55, 0), (0, 50), (30, 120), (80, 120), (110, 50)])
        pygame.draw.polygon(surf, AMARILLO, [(55, 10), (10, 50), (35, 110), (75, 110), (100, 50)], 4)
        pygame.draw.circle(surf, CIAN, (55, 60), 18)
        pygame.draw.circle(surf, ROSA_NEON, (55, 60), 8)

    return surf

img_barril = pygame.Surface((35, 45), pygame.SRCALPHA)
pygame.draw.rect(img_barril, NARANJA, (0, 0, 35, 45), border_radius=8)
pygame.draw.rect(img_barril, NEGRO, (0, 10, 35, 5))
pygame.draw.rect(img_barril, NEGRO, (0, 30, 35, 5))

img_moneda = pygame.Surface((24, 24), pygame.SRCALPHA)
pygame.draw.circle(img_moneda, AMARILLO, (12, 12), 12)
pygame.draw.circle(img_moneda, (255, 245, 160), (12, 12), 8)

# --- CLASES ---
class Jugador(pygame.sprite.Sprite):
    def __init__(self, color, velocidad, es_god=False, tiene_escudo=False):
        super().__init__()
        self.color = color
        self.es_god = es_god
        self.tiene_escudo = tiene_escudo or es_god
        self.actualizar_imagen()
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 30
        self.velocidad = velocidad

    def actualizar_imagen(self):
        base = crear_imagen_auto(self.color, es_god=self.es_god)
        if self.tiene_escudo:
            surf = pygame.Surface((60, 90), pygame.SRCALPHA)
            surf.blit(base, (10, 10))
            pygame.draw.ellipse(surf, CIAN, (0, 0, 60, 90), 3)
            self.image = surf
        else:
            self.image = base

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidad
        
        if self.rect.left < 50:
            self.rect.left = 50
        if self.rect.right > ANCHO - 50:
            self.rect.right = ANCHO - 50

class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y, tipo, dx=0, dy=-14, enemigo=False):
        super().__init__()
        self.tipo = tipo
        self.velocidad_y = dy
        self.velocidad_x = dx
        self.enemigo = enemigo
        
        if enemigo:
            self.image = pygame.Surface((10, 24), pygame.SRCALPHA)
            pygame.draw.rect(self.image, ROJO, (0, 0, 10, 24), border_radius=4)
            pygame.draw.rect(self.image, AMARILLO, (2, 2, 6, 20), border_radius=2)
        elif tipo == "misil" or tipo == "escudo":
            self.image = pygame.Surface((8, 20), pygame.SRCALPHA)
            pygame.draw.rect(self.image, ROJO, (0, 0, 8, 20), border_radius=4)
        elif tipo == "onda":
            self.image = pygame.Surface((40, 14), pygame.SRCALPHA)
            pygame.draw.ellipse(self.image, VERDE, (0, 0, 40, 14))
            self.velocidad_y = -10
        elif tipo == "fuego":
            self.image = pygame.Surface((18, 24), pygame.SRCALPHA)
            pygame.draw.ellipse(self.image, NARANJA, (0, 0, 18, 24))
            pygame.draw.ellipse(self.image, AMARILLO, (4, 4, 10, 16))
            self.velocidad_y = -16
        elif tipo == "laser":
            self.image = pygame.Surface((6, 40), pygame.SRCALPHA)
            pygame.draw.rect(self.image, MORADO, (0, 0, 6, 40), border_radius=3)
            self.velocidad_y = -20
        elif tipo == "plasma":
            self.image = pygame.Surface((12, 22), pygame.SRCALPHA)
            pygame.draw.rect(self.image, CIAN, (0, 0, 12, 22), border_radius=6)
        elif tipo == "oro_escudo":
            self.image = pygame.Surface((22, 22), pygame.SRCALPHA)
            pygame.draw.circle(self.image, AMARILLO, (11, 11), 11)
            self.velocidad_y = -12
        elif tipo == "diagonal" or tipo == "god":
            self.image = pygame.Surface((10, 20), pygame.SRCALPHA)
            color_p = CIAN if tipo == "diagonal" else ROSA_NEON
            pygame.draw.rect(self.image, color_p, (0, 0, 10, 20), border_radius=4)
            self.velocidad_y = -15
        elif tipo == "pesado":
            self.image = pygame.Surface((26, 26), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (100, 100, 110), (0, 0, 26, 26), border_radius=4)
            self.velocidad_y = -9

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y

    def update(self):
        self.rect.y += self.velocidad_y
        self.rect.x += self.velocidad_x
        if self.rect.bottom < 0 or self.rect.top > ALTO or self.rect.right < 0 or self.rect.left > ANCHO:
            self.kill()

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.reiniciar()

    def reiniciar(self):
        self.tipo = random.choice(["auto", "barril"])
        if self.tipo == "auto":
            self.image = crear_imagen_auto(AZUL, invertido=True)
        else:
            self.image = img_barril
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(60, ANCHO - 90)
        self.rect.y = random.randrange(-350, -80)
        self.velocidad = random.randrange(4, 7)

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.top > ALTO:
            self.reiniciar()

class MonedaItem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = img_moneda
        self.rect = self.image.get_rect()
        self.reiniciar()

    def reiniciar(self):
        self.rect.x = random.randrange(60, ANCHO - 80)
        self.rect.y = random.randrange(-400, -100)
        self.velocidad = 5

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.top > ALTO:
            self.reiniciar()

class Jefe(pygame.sprite.Sprite):
    def __init__(self, numero_jefe):
        super().__init__()
        self.num = numero_jefe
        self.tipo_diseno = (numero_jefe - 1) % 8
        self.image = crear_imagen_jefe(self.tipo_diseno)
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.y = -130
        
        self.velocidad_base = 3.5 + (0.5 * (self.tipo_diseno == 6))
        self.velocidad_x = self.velocidad_base
        self.vida_maxima = 30 + (numero_jefe * 8)
        self.vida = self.vida_maxima
        
        self.ultimo_disparo = pygame.time.get_ticks()
        self.tiempo_dash = pygame.time.get_ticks()
        self.en_dash = False

    def update(self):
        if self.rect.y < 40:
            self.rect.y += 2
            return

        ahora = pygame.time.get_ticks()

        if self.tipo_diseno == 7:
            if not self.en_dash and ahora - self.tiempo_dash > 7000:
                self.en_dash = True
                self.tiempo_dash = ahora
                self.velocidad_x = 11 * (1 if self.velocidad_x > 0 else -1)
            elif self.en_dash and ahora - self.tiempo_dash > 2500:
                self.en_dash = False
                self.tiempo_dash = ahora
                self.velocidad_x = self.velocidad_base * (1 if self.velocidad_x > 0 else -1)

        self.rect.x += self.velocidad_x
        if self.rect.right >= ANCHO - 50:
            self.rect.right = ANCHO - 50
            self.velocidad_x = -abs(self.velocidad_x)
        elif self.rect.left <= 50:
            self.rect.left = 50
            self.velocidad_x = abs(self.velocidad_x)

    def disparar(self):
        ahora = pygame.time.get_ticks()
        if self.tipo_diseno in [5, 6, 7]:
            cadencia = 2000 if self.tipo_diseno == 5 else (1400 if self.tipo_diseno == 6 else 900)
            if ahora - self.ultimo_disparo > cadencia:
                self.ultimo_disparo = ahora
                vel_balas = 5 if self.tipo_diseno == 5 else (8 if self.tipo_diseno == 6 else 11)
                return Proyectil(self.rect.centerx, self.rect.bottom, "misil", dy=vel_balas, enemigo=True)
        return None

# --- PANTALLA DE ENTRADA (SPLASH SCREEN) ---
def pantalla_splash():
    fuente_sub = pygame.font.SysFont("Segoe UI", 16, bold=True)
    fuente_brand = pygame.font.SysFont("Impact", 32)
    tiempo_inicio = pygame.time.get_ticks()
    
    while pygame.time.get_ticks() - tiempo_inicio < 2500:
        pantalla.fill(NEGRO)
        progreso = (pygame.time.get_ticks() - tiempo_inicio) / 2500
        alpha = int(255 * math.sin(progreso * math.pi))
        
        pygame.draw.polygon(pantalla, CIAN, [(ANCHO//2, 180), (ANCHO//2 - 40, 250), (ANCHO//2 + 40, 250)], 4)
        pygame.draw.circle(pantalla, ROSA_NEON, (ANCHO//2, 225), 15)
        
        txt_sub = fuente_sub.render("PRESENTED BY", True, (150, 150, 170))
        txt_brand = fuente_brand.render("JOSS CREATIONS", True, AMARILLO)
        
        txt_brand.set_alpha(alpha)
        txt_sub.set_alpha(alpha)
        
        pantalla.blit(txt_sub, (ANCHO//2 - txt_sub.get_width()//2, 280))
        pantalla.blit(txt_brand, (ANCHO//2 - txt_brand.get_width()//2, 310))
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

# --- MENÚ DE PAUSA Y CONFIGURACIÓN ---
def menu_pausa():
    global volumen_global
    fuente_t = pygame.font.SysFont("Impact", 32)
    fuente_s = pygame.font.SysFont("Segoe UI", 16, bold=True)
    
    while True:
        sombra = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        sombra.fill((0, 0, 0, 180))
        pantalla.blit(sombra, (0, 0))

        pygame.draw.rect(pantalla, (20, 20, 30), (40, 150, ANCHO - 80, 300), border_radius=12)
        pygame.draw.rect(pantalla, CIAN, (40, 150, ANCHO - 80, 300), 2, border_radius=12)

        txt_p = fuente_t.render("PAUSA", True, AMARILLO)
        pantalla.blit(txt_p, (ANCHO//2 - txt_p.get_width()//2, 170))

        vol_pct = int(volumen_global * 100)
        pantalla.blit(fuente_s.render(f"VOLUMEN: < {vol_pct}% >", True, BLANCO), (60, 240))
        pygame.draw.rect(pantalla, (50, 50, 60), (60, 270, 280, 15), border_radius=5)
        pygame.draw.rect(pantalla, VERDE, (60, 270, int(2.8 * vol_pct), 15), border_radius=5)

        pantalla.blit(fuente_s.render("[ESC / P]  Continuar", True, ROSA_NEON), (60, 320))
        pantalla.blit(fuente_s.render("[Q]        Salir al Menú", True, ROJO), (60, 360))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE, pygame.K_p]:
                    return "continuar"
                if event.key == pygame.K_q:
                    return "menu"
                if event.key == pygame.K_LEFT:
                    volumen_global = max(0.0, volumen_global - 0.1)
                    actualizar_volumen()
                if event.key == pygame.K_RIGHT:
                    volumen_global = min(1.0, volumen_global + 0.1)
                    actualizar_volumen()

# --- MENÚ PRINCIPAL Y TIENDA ---
def mostrar_menu():
    global monedas_totales
    fuente_t1 = pygame.font.SysFont("Impact", 36)
    fuente_t2 = pygame.font.SysFont("Impact", 36)
    fuente_s = pygame.font.SysFont("Segoe UI", 16, bold=True)
    
    estrellas = [(random.randint(0, ANCHO), random.randint(0, ALTO)) for _ in range(40)]
    img_demo = crear_imagen_auto(ROSA_NEON)

    while True:
        pantalla.fill(NEGRO)

        for ex, ey in estrellas:
            pygame.draw.circle(pantalla, (180, 180, 220), (ex, ey), 1)

        puntos_pista = [(ANCHO//2 - 20, 120), (ANCHO//2 + 20, 120), (ANCHO + 80, ALTO), (-80, ALTO)]
        pygame.draw.polygon(pantalla, (25, 20, 35), puntos_pista)

        pygame.draw.line(pantalla, ROSA_NEON, (ANCHO//2 - 20, 120), (-80, ALTO), 4)
        pygame.draw.line(pantalla, ROSA_NEON, (ANCHO//2 + 20, 120), (ANCHO + 80, ALTO), 4)

        auto_escalado = pygame.transform.scale(img_demo, (70, 120))
        pantalla.blit(auto_escalado, (ANCHO//2 - 35, 340))

        txt_sombra = fuente_t1.render("ROAD COMBAT", True, MORADO)
        txt_titulo = fuente_t2.render("ROAD COMBAT", True, CIAN)
        pantalla.blit(txt_sombra, (ANCHO//2 - txt_sombra.get_width()//2 + 3, 43))
        pantalla.blit(txt_titulo, (ANCHO//2 - txt_titulo.get_width()//2, 40))

        pygame.draw.rect(pantalla, (20, 20, 30), (40, 460, ANCHO - 80, 115), border_radius=10)
        pygame.draw.rect(pantalla, CIAN, (40, 460, ANCHO - 80, 115), 2, border_radius=10)

        pantalla.blit(fuente_s.render("[ENTER]  INICIAR CARRERA", True, AMARILLO), (55, 475))
        pantalla.blit(fuente_s.render("[G]      GARAJE DE AUTOS", True, BLANCO), (55, 505))
        pantalla.blit(fuente_s.render(f"MONEDAS: ${monedas_totales}", True, VERDE), (55, 535))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_g:
                    mostrar_tienda()

def mostrar_tienda():
    global monedas_totales, auto_seleccionado
    fuente = pygame.font.SysFont("Segoe UI", 15, bold=True)
    idx = auto_seleccionado

    while True:
        pantalla.fill((20, 20, 30))
        auto = AUTOS_TIENDA[idx]

        pantalla.blit(fuente.render(f"GARAJE ({idx+1}/{len(AUTOS_TIENDA)})", True, AMARILLO), (ANCHO//2 - 50, 20))
        pantalla.blit(fuente.render(f"Tus Monedas: ${monedas_totales}", True, VERDE), (40, 55))

        es_god = auto.get("secreto", False)
        img_prev = crear_imagen_auto(auto["color"], es_god=es_god)
        pantalla.blit(pygame.transform.scale(img_prev, (85, 140)), (ANCHO//2 - 42, 90))

        pantalla.blit(fuente.render(f"Nombre: {auto['nombre']}", True, BLANCO), (40, 250))
        pantalla.blit(fuente.render(f"Velocidad: {auto['vel']}", True, BLANCO), (40, 280))
        pantalla.blit(fuente.render(f"Poder: {auto['tipo_poder'].upper()}", True, CIAN), (40, 310))

        if es_god:
            estado = "DESBLOQUEADO" if auto["comprado"] else "DERROTA AL JEFE #8 PARA USAR"
            col_est = VERDE if auto["comprado"] else ROJO
        else:
            estado = "EQUIPADO" if idx == auto_seleccionado else ("COMPRADO" if auto["comprado"] else f"PRECIO: ${auto['precio']}")
            col_est = ROSA_NEON if auto["comprado"] else AMARILLO

        pantalla.blit(fuente.render(f"Estado: {estado}", True, col_est), (40, 340))
        pantalla.blit(fuente.render("< / > Cambiar | [E] Seleccionar", True, BLANCO), (10, 510))
        pantalla.blit(fuente.render("[ESC] Volver al menú", True, BLANCO), (10, 535))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_RIGHT:
                    idx = (idx + 1) % len(AUTOS_TIENDA)
                if event.key == pygame.K_LEFT:
                    idx = (idx - 1) % len(AUTOS_TIENDA)
                if event.key == pygame.K_e:
                    if auto["comprado"]:
                        auto_seleccionado = idx
                    elif not es_god and monedas_totales >= auto["precio"]:
                        monedas_totales -= auto["precio"]
                        auto["comprado"] = True
                        auto_seleccionado = idx

# --- BUCLE DE CARRERA ---
def carrera():
    global monedas_totales
    datos_auto = AUTOS_TIENDA[auto_seleccionado]

    todos_los_sprites = pygame.sprite.Group()
    obstaculos = pygame.sprite.Group()
    monedas_grupo = pygame.sprite.Group()
    misiles_grupo = pygame.sprite.Group()
    balas_enemigas = pygame.sprite.Group()

    es_god = datos_auto.get("secreto", False)
    tiene_escudo_inicial = datos_auto["tipo_poder"] in ["escudo", "oro_escudo"]
    jugador = Jugador(datos_auto["color"], datos_auto["vel"], es_god=es_god, tiene_escudo=tiene_escudo_inicial)
    todos_los_sprites.add(jugador)

    for _ in range(3):
        obs = Obstaculo()
        todos_los_sprites.add(obs)
        obstaculos.add(obs)

    for _ in range(2):
        mon = MonedaItem()
        todos_los_sprites.add(mon)
        monedas_grupo.add(mon)

    jefe = None
    modo_jefe = False
    distancia_ultimo_jefe = 0
    conteo_jefes = 0
    siguiente_hito_1000 = 1000

    puntuacion = 0
    monedas_partida = 0
    linea_y = 0
    fuente = pygame.font.SysFont("Segoe UI", 18, bold=True)
    chocado = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if chocado and event.key == pygame.K_RETURN:
                    return
                if not chocado and event.key in [pygame.K_ESCAPE, pygame.K_p]:
                    res = menu_pausa()
                    if res == "menu":
                        return
                if not chocado and event.key == pygame.K_SPACE:
                    tp = datos_auto["tipo_poder"]
                    if tp == "diagonal":
                        m1 = Proyectil(jugador.rect.centerx, jugador.rect.top, tp, dx=-4)
                        m2 = Proyectil(jugador.rect.centerx, jugador.rect.top, tp, dx=4)
                        todos_los_sprites.add(m1, m2)
                        misiles_grupo.add(m1, m2)
                    elif tp == "god":
                        m1 = Proyectil(jugador.rect.centerx, jugador.rect.top, tp, dx=0)
                        m2 = Proyectil(jugador.rect.centerx, jugador.rect.top, tp, dx=-5)
                        m3 = Proyectil(jugador.rect.centerx, jugador.rect.top, tp, dx=5)
                        todos_los_sprites.add(m1, m2, m3)
                        misiles_grupo.add(m1, m2, m3)
                    else:
                        misil = Proyectil(jugador.rect.centerx, jugador.rect.top, tp)
                        todos_los_sprites.add(misil)
                        misiles_grupo.add(misil)
                    sonido_disparo.play()

        if not chocado:
            todos_los_sprites.update()
            puntuacion += 1

            if puntuacion >= siguiente_hito_1000:
                sonido_dino.play()
                siguiente_hito_1000 += 1000

            linea_y += 6
            if linea_y >= 40: linea_y = 0

            if (puntuacion - distancia_ultimo_jefe >= 3500) and not modo_jefe:
                modo_jefe = True
                conteo_jefes += 1
                for obs in obstaculos:
                    obs.kill()
                jefe = Jefe(conteo_jefes)
                todos_los_sprites.add(jefe)

            if modo_jefe and jefe and jefe.alive():
                bala = jefe.disparar()
                if bala:
                    todos_los_sprites.add(bala)
                    balas_enemigas.add(bala)

            for misil in misiles_grupo:
                impactos = pygame.sprite.spritecollide(misil, obstaculos, False)
                for obs in impactos:
                    if datos_auto["tipo_poder"] != "laser":
                        misil.kill()
                    obs.reiniciar()

            if modo_jefe and jefe and jefe.alive():
                impactos_jefe = pygame.sprite.spritecollide(jefe, misiles_grupo, True)
                for _ in impactos_jefe:
                    jefe.vida -= 1
                    if jefe.vida <= 0:
                        jefe.kill()
                        jefe = None
                        modo_jefe = False
                        distancia_ultimo_jefe = puntuacion
                        sonido_choque.play()
                        monedas_totales += 500
                        monedas_partida += 500
                        
                        if conteo_jefes >= 8:
                            AUTOS_TIENDA[-1]["comprado"] = True
                        
                        for _ in range(3):
                            obs = Obstaculo()
                            todos_los_sprites.add(obs)
                            obstaculos.add(obs)

            for m in monedas_grupo:
                if datos_auto["tipo_poder"] in ["onda", "god"]:
                    if math.hypot(jugador.rect.centerx - m.rect.centerx, jugador.rect.centery - m.rect.centery) < 130:
                        m.rect.x += 6 if m.rect.centerx < jugador.rect.centerx else -6
                        m.rect.y += 6 if m.rect.centery < jugador.rect.centery else -6

            col_monedas = pygame.sprite.spritecollide(jugador, monedas_grupo, False)
            for m in col_monedas:
                monedas_partida += 15
                monedas_totales += 15
                sonido_moneda.play()
                m.reiniciar()

            choque_obs = pygame.sprite.spritecollide(jugador, obstaculos, False)
            choque_balas = pygame.sprite.spritecollide(jugador, balas_enemigas, True)
            choque_jefe = (jefe and jefe.alive() and pygame.sprite.collide_rect(jugador, jefe))

            if choque_obs or choque_balas or choque_jefe:
                if jugador.tiene_escudo and not es_god:
                    jugador.tiene_escudo = False
                    jugador.actualizar_imagen()
                    sonido_choque.play()
                    for obs in choque_obs:
                        obs.reiniciar()
                elif not es_god:
                    sonido_choque.play()
                    chocado = True

        pantalla.fill(GRIS_ASFALTO)
        pygame.draw.rect(pantalla, (30, 140, 30), (0, 0, 50, ALTO))
        pygame.draw.rect(pantalla, (30, 140, 30), (ANCHO - 50, 0, 50, ALTO))
        pygame.draw.rect(pantalla, BLANCO, (45, 0, 5, ALTO))
        pygame.draw.rect(pantalla, BLANCO, (ANCHO - 50, 0, 5, ALTO))

        for y in range(-40 + int(linea_y), ALTO, 40):
            pygame.draw.rect(pantalla, AMARILLO, (ANCHO // 2 - 4, y, 8, 20))

        todos_los_sprites.draw(pantalla)

        if modo_jefe and jefe and jefe.alive():
            pygame.draw.rect(pantalla, NEGRO, (70, 15, ANCHO - 140, 20), border_radius=4)
            ancho_vida = int((ANCHO - 144) * (jefe.vida / jefe.vida_maxima))
            pygame.draw.rect(pantalla, ROJO, (72, 17, max(0, ancho_vida), 16), border_radius=3)
            pantalla.blit(fuente.render(f"¡JEFE #{conteo_jefes}!", True, BLANCO), (ANCHO//2 - 45, 38))

        pantalla.blit(fuente.render(f"DISTANCIA: {puntuacion}", True, BLANCO), (60, 10))
        pantalla.blit(fuente.render(f"MONEDAS: ${monedas_partida}", True, AMARILLO), (60, 30))

        if chocado:
            pygame.draw.rect(pantalla, NEGRO, (30, ALTO//2 - 60, ANCHO - 60, 120), border_radius=10)
            pantalla.blit(fuente.render("¡DESTRUIDO!", True, ROJO), (ANCHO//2 - 50, ALTO//2 - 40))
            pantalla.blit(fuente.render("ENTER: Volver al menú", True, BLANCO), (ANCHO//2 - 95, ALTO//2 + 10))

        pygame.display.flip()
        reloj.tick(60)

# --- BUCLE PRINCIPAL ---
pantalla_splash()
while True:
    mostrar_menu()
    carrera()