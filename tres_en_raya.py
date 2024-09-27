import pygame
import random


pygame.init()
screen = pygame.display.set_mode((450, 450))
pygame.display.set_caption("Tres en Raya")


fondo = pygame.image.load('TBL.png')
fondoA = pygame.image.load('DSL.png')
fondoB = pygame.image.load('DSL2.png')
fondoC = pygame.image.load('DSL3.png')
circulo = pygame.image.load('POLICE.png')
equis = pygame.image.load('CARAVAN.png')
indicador = pygame.image.load('INDICADOR.png')

fondoA = pygame.transform.scale(fondoA, (450, 450))
fondoB = pygame.transform.scale(fondoB, (450, 450))
fondoC = pygame.transform.scale(fondoC, (450, 450))
fondo = pygame.transform.scale(fondo, (450, 450))
circulo = pygame.transform.scale(circulo, (125, 125))
equis = pygame.transform.scale(equis, (125, 125))
indicador = pygame.transform.scale(indicador, (100, 100))


coor = [[(40, 50), (165, 50), (290, 50)],
        [(40, 175), (165, 175), (290, 175)],
        [(40, 300), (165, 300), (290, 300)]]
tablero = [['', '', ''],
           ['', '', ''],
           ['', '', '']]

COLOR_BOTON1 = (152, 186, 16)  
COLOR_BOTON2 = (14, 165, 176)
COLOR_BOTON3 = (176, 14, 132)
COLOR_TEXTO = (0, 0, 0)  
COLOR_TEMPORIZADOR = (178, 217, 68)  



fuente = pygame.font.Font(None, 40)
turno = 'X'  
game_over = False
clock = pygame.time.Clock()


tiempo_limite = 30000  
tiempo_restante = tiempo_limite



def graficar_board():
    screen.blit(fondo, (0, 0))
    for fila in range(3):
        for col in range(3):
            if tablero[fila][col] == 'X':
                dibujar_x(fila, col)
            elif tablero[fila][col] == 'O':
                dibujar_o(fila, col)

def dibujar_x(fila, col):
    screen.blit(equis, coor[fila][col])

def dibujar_o(fila, col):
    screen.blit(circulo, coor[fila][col])


def verificar_ganador():
    for i in range(3):
        if tablero[i][0] == tablero[i][1] == tablero[i][2] != '':
            return True
        if tablero[0][i] == tablero[1][i] == tablero[2][i] != '':
            return True
    if tablero[0][0] == tablero[1][1] == tablero[2][2] != '':
        return True
    if tablero[0][2] == tablero[1][1] == tablero[2][0] != '':
        return True
    return False

def verificar_empate():
    for fila in tablero:
        if '' in fila:
            return False
    return True

def mostrar_mensaje(texto, posicion_y=225):
    
    mensaje = fuente.render(texto, True, (255, 255, 255 ))  
    rect_mensaje = mensaje.get_rect(center=(225,  posicion_y))
    margen = 10
    
    rect_recuadro = rect_mensaje.inflate(margen * 2, margen * 2)
    color_recuadro = (16, 140, 186)  
    
    pygame.draw.rect(screen, color_recuadro, rect_recuadro, border_radius=5)  

    screen.blit(mensaje, rect_mensaje)  
    pygame.display.update()  
    pygame.time.wait(6000)  
    
def obtener_movimientos_validos():
    return [(fila, col) for fila in range(3) for col in range(3) if tablero[fila][col] == '']

def minimax(tablero, profundidad, es_maximizador, profundidad_maxima):
    if verificar_ganador():
        return -1 if es_maximizador else 1
    elif verificar_empate():
        return 0
    if profundidad >= profundidad_maxima:
        return 0  

    movimientos = obtener_movimientos_validos()
    if es_maximizador:
        mejor_puntaje = -float('inf')
        for fila, col in movimientos:
            tablero[fila][col] = 'O'
            puntaje = minimax(tablero, profundidad + 1, False, profundidad_maxima)
            tablero[fila][col] = ''
            mejor_puntaje = max(mejor_puntaje, puntaje)
        return mejor_puntaje
    else:
        mejor_puntaje = float('inf')
        for fila, col in movimientos:
            tablero[fila][col] = 'X'
            puntaje = minimax(tablero, profundidad + 1, True, profundidad_maxima)
            tablero[fila][col] = ''
            mejor_puntaje = min(mejor_puntaje, puntaje)
        return mejor_puntaje

def mejor_movimiento_ia(profundidad_maxima):
    mejor_puntaje = -float('inf')
    mejor_movimiento = None
    for fila, col in obtener_movimientos_validos():
        tablero[fila][col] = 'O'
        puntaje = minimax(tablero, 0, False, profundidad_maxima)
        tablero[fila][col] = ''
        if puntaje > mejor_puntaje:
            mejor_puntaje = puntaje
            mejor_movimiento = (fila, col)
    return mejor_movimiento


def seleccionar_quien_empieza():
    seleccionando = True
    while seleccionando:
        screen.fill((255, 255, 255))  
        screen.blit(fondoC, (0, 0))  
        mensaje1 = fuente.render("¿Quién empieza?", True, (0, 0, 0))
        mensaje2 = fuente.render("Presiona: X (jugador) o O (IA)", True, (0, 0, 0))
     
      
        rect_mensaje1 = mensaje1.get_rect(topleft=(90, 155))  
        rect_mensaje2 = mensaje2.get_rect(topleft=(25, 250))  
      
        margen = 10
        color_fondo_mensaje1 = (255, 255, 255)  
        color_fondo_mensaje2 = (161, 217, 68)  

        
        pygame.draw.rect(screen, color_fondo_mensaje1, rect_mensaje1.inflate(margen * 2, margen * 2),border_radius=5)  
        pygame.draw.rect(screen, color_fondo_mensaje2, rect_mensaje2.inflate(margen * 2, margen * 2),border_radius=5)  

        screen.blit(mensaje1, rect_mensaje1)
        screen.blit(mensaje2, rect_mensaje2)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    return 'X'  # Jugador empieza
                elif event.key == pygame.K_o:
                    return 'O'  # IA empieza

def crear_boton(texto, x, y, ancho, alto, color_fondo, color_texto):
    pygame.draw.rect(screen, color_fondo, (x, y, ancho, alto))
    texto_superficie = fuente.render(texto, True, color_texto)
    screen.blit(texto_superficie, (x + 10, y + 10))
     
 
def crear_boton(texto, x, y, ancho, alto, color_boton, color_texto, radio_bordes):
    boton_rect = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(screen, color_boton, boton_rect, border_radius=radio_bordes)
    
    texto_renderizado = fuente.render(texto, True, color_texto)
    texto_rect = texto_renderizado.get_rect(center=(x + ancho // 2, y + alto // 2))
    
    
    screen.blit(texto_renderizado, texto_rect)



def seleccionar_dificultad():
    seleccionando = True
    while seleccionando:
        screen.fill((255, 255, 255))  
        screen.blit(fondoB, (0, 0))  
        mensaje = fuente.render("Selecciona la dificultad", True, (0, 0, 0))
        screen.blit(mensaje, (70, 50))
        
        crear_boton("Básico", 50, 150, 150, 50,COLOR_BOTON1, COLOR_TEXTO, 5)
        crear_boton("Moderado", 250, 150, 150, 50,COLOR_BOTON2, COLOR_TEXTO, 5)
        crear_boton("Avanzado", 150, 250, 150, 50,COLOR_BOTON3, COLOR_TEXTO, 5)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 50 < x < 200 and 150 < y < 200:
                    return 0  
                elif 250 < x < 400 and 150 < y < 200:
                    return 3  
                elif 150 < x < 300 and 250 < y < 300:
                    return 7  
                
def mostrar_bienvenida():
    seleccionando = True
    while seleccionando:
        screen.fill((255, 255, 255))  
        screen.blit(fondoA, (0, 0))  
        mensaje = fuente.render("Bienvenido a Tres en Raya", True, (0, 0, 0))
        screen.blit(mensaje, (70, 50))
        
        
        crear_boton("Jugar", 150, 150, 150, 50, COLOR_BOTON1, COLOR_TEXTO, 5)
        crear_boton("Salir", 150, 250, 150, 50, COLOR_BOTON2, COLOR_TEXTO, 5)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 150 < x < 300 and 150 < y < 200:  
                    return True  
                    
                elif 150 < x < 300 and 250 < y < 300:  
                    pygame.quit()
                    return False                    
def reiniciar_juego():
    global tablero, turno, game_over, tiempo_restante, profundidad_maxima_ia
    tablero = [['', '', ''], ['', '', ''], ['', '', '']]
    game_over = False
    tiempo_restante = tiempo_limite
    profundidad_maxima_ia = seleccionar_dificultad()
    turno = seleccionar_quien_empieza()

corriendo = True
while corriendo:
    if mostrar_bienvenida():
        reiniciar_juego()
        while not game_over:
            clock.tick(30)
            if tiempo_restante > 0:
                tiempo_restante -= clock.get_time()  
                segundos_restantes = max(0, tiempo_restante // 1000)  

            if turno == 'X':
                if tiempo_restante <= 0:
                    mostrar_mensaje("¡Tiempo agotado!", posicion_y=200)
                    mostrar_mensaje(" La IA ha ganado.", posicion_y=250)
                    game_over = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    corriendo = False
                    game_over = True
                elif event.type == pygame.MOUSEBUTTONDOWN and turno == 'X':
                    mouseX, mouseY = event.pos
                    if (mouseX >= 40 and mouseX < 451) and (mouseY >= 50 and mouseY < 425):
                        fila = (mouseY - 50) // 125
                        col = (mouseX - 40) // 125
                        if tablero[fila][col] == '':
                            tablero[fila][col] = turno
                            fin_juego = verificar_ganador()
                            if fin_juego:
                                
                                graficar_board()  
                                pygame.display.update()  
                                pygame.time.wait(1000) 
                                
                                mostrar_mensaje(f"  Has ganado!!!")
                                game_over = True
                            elif verificar_empate():
                                graficar_board()  
                                pygame.display.update()  
                                pygame.time.wait(1000) 
                                mostrar_mensaje("¡Empate!")
                                game_over = True
                            else:
                                turno = 'O'
                                tiempo_restante = tiempo_limite  

            if turno == 'O' and not game_over:
                fila, col = mejor_movimiento_ia(profundidad_maxima_ia)
                tablero[fila][col] = 'O'
                fin_juego = verificar_ganador()
                if fin_juego:
                    graficar_board()  
                    pygame.display.update()  
                    pygame.time.wait(1000) 
                    mostrar_mensaje("¡La IA ha ganado!")
                    game_over = True
                elif verificar_empate():
                    graficar_board()  
                    pygame.display.update()  
                    pygame.time.wait(1000) 
                    mostrar_mensaje("¡Empate!")
                    game_over = True
                else:
                    turno = 'X'
                    tiempo_restante = tiempo_limite  
            
            graficar_board()
            if turno == 'X':
                texto_temporizador = fuente.render(f'Tiempo: {segundos_restantes}', True, COLOR_TEMPORIZADOR)
                screen.blit(texto_temporizador, (10, 10))
 
            mouseX, mouseY = pygame.mouse.get_pos()  
            screen.blit(indicador, (mouseX - 25, mouseY - 25))  

            texto_indicador = fuente.render("", True, (0, 0, 0))  
            screen.blit(texto_indicador, (mouseX - 50, mouseY + 30))  
            pygame.display.update()
       
    else:
    
        corriendo = False

pygame.quit()
