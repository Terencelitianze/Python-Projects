add_library('minim')

stage = "menu"
nCol, nLin = 0, 0  # nº de linas e de colunas
tamanho = 50  # tamanho (largura e altura) das células do labirinto
direction = ""  # direção do pacman
espacamento = 2  # espaço livre entre células
vel = 1  # módulo da velocidade do pacman
margemV, margemH = 0, 0  # margem livre na vertical e na horizontal para assegurar que as células são quadrangulares
corObstaculos = color(0)  # cor de fundo dos obstáculos
corFronteira = color(0)
corBolas = color(255)
corPacman = color(255, 255, 0)
red = color(255, 0, 0)
red_vx, red_vy = 0, 0  # Velocidades do fantasma vermelho
blue = color(51, 204, 255)
blue_vx, blue_vy = 0, 0  # Velocidades do fantasma azul
pink = color(255, 162, 122)
pink_vx, pink_vy = 0, 0  # Velocidades do fantasma rosa
pink_pathCount = 0
orange = color(255, 204, 0)
orange_vx, orange_vy = 0, 0  # Velocidades do fantasma laranja
orange_pathCount = 0
path = []
wasHere = []
invert = False  # Evento do jogo em que os fantasmas mudam de direção
speed = False  # Evento que aumenta a velocidade do jogo
godmode = False  # Evento que torna o pacman invulneravel
text = []  # array da pontuação em String
scores = []  # array da pontuação em valores inteiros
leaderboard = []  # 5 melhores pontuações
numOnScreen = 0  # numero de bolas
numEaten = 0  # número de bolas comidas
score = 0  # pontuação do jogador
soundOn = True
pause = False
# Posicao e tamanho do Pacman
px, py, pRaio = 0, 0, 0
vx, vy = 0, 0
# Posição dos fantasmas
red_px, red_py = 0, 0  # Fantasma vermelho
blue_px, blue_py = 0, 0  # Fantasma azul
pink_px, pink_py = 0, 0  # Fantasma rosa
orange_px, orange_py = 0, 0  # Fantasma laranja

def setup():
    global nCol, nLin, margemV, margemH, px, py, pRaio
    global red_px, red_py, blue_px, blue_py, pink_px, pink_py, orange_px, orange_py
    global path, wasHere, leaderboard
    global minim, intro, chump, death, speedUp, god, ghosts, silence
    global crackmanFont, lotFont
    
    size(720, 520)
    background(1)
    frameRate(200)
    
    # Velocidade inicial do pacman e fantasmas
    global vx, vy, red_vx, red_vy, blue_vx, blue_vy, pink_vx, pink_vy, orange_vx, orange_vy
    vx = vy = red_vx = red_vy = blue_vx = blue_vy = pink_vx = pink_vy = orange_vx = orange_vy = 0
    
    # Tipo de letra
    crackmanFont = createFont("crackman.TTF", 18)
    lotFont = createFont("lot.otf", 18)
    
    # Ficheiros
    global text
    text = loadStrings("leaderboard.txt")
    
    # Música
    minim = Minim(this)
    intro = minim.loadFile("pacman_beginning.wav")
    minim.getLineOut().setGain(-12)
    chump = minim.loadFile("pacman_chomp.wav")
    minim.getLineOut().setGain(-20)
    death = minim.loadFile("pacman_death.wav")
    minim.getLineOut().setGain(-10)
    speedUp = minim.loadFile("pacman_speed.wav")
    minim.getLineOut().setGain(-12)
    god = minim.loadFile("pacman_eatfruit.wav")
    minim.getLineOut().setGain(-10)
    ghosts = minim.loadFile("pacman_ghosts.wav")
    minim.getLineOut().setGain(-12)
    silence = minim.loadFile("pacman_silence.wav")
    
    nCol = int(width / tamanho)
    nLin = int(height / tamanho)
    
    path = [[0 for _ in range(nCol + 2)] for _ in range(nLin + 2)]
    wasHere = [[False for _ in range(nCol + 2)] for _ in range(nLin + 2)]
    leaderboard = [0] * 5
    
    readFile()
    readLeaderboard()
    
    assert nCol >= 5 and nLin >= 5
    
    margemV = (width - nCol * tamanho) / 2.0
    margemH = (height - nLin * tamanho) / 2.0
    
    px, py = centroX(9), centroY(5)
    pRaio = 30
    
    global invert, speed, godmode
    invert = speed = godmode = False
    
    red_px, red_py = centroX(9), centroY(1)
    blue_px, blue_py = centroX(7), centroY(5)
    pink_px, pink_py = centroX(3), centroY(4)
    global pink_pathCount
    pink_pathCount = 0
    orange_px, orange_py = centroX(nCol), centroY(7)
    global orange_pathCount
    orange_pathCount = 0

def draw():
    global stage, px, py, score
    
    if stage == "menu":
        img1 = loadImage("menu_inicial_1_original.jpg")
        image(img1, 0, 0)
        img2 = loadImage("pacman_letras.png")
        image(img2, 40, 80)
        buttonHighlight()
    elif stage == "leaderboard":
        background(0, 0, 112)
        fill(255, 255, 0)
        textFont(crackmanFont)
        textSize(60)
        text("Top 5", 70, 100)
        textSize(40)
        for i in range(5):
            suffix = "st" if i == 0 else "nd" if i == 1 else "rd" if i == 2 else "th"
            text("{0}{1} Place: {2} points".format(i+1, suffix, leaderboard[i]), 100, 200 + i * 40)
        buttonHighlight()
    elif stage == "ready":
        background(0)
        fill(255, 255, 0)
        textSize(60)
        text("READY!", (width/2)-130, height/2)
        if not intro.isPlaying():
            stage = "game"
    elif stage == "game":
        background(0)
        global corObstaculos, corFronteira, corBolas, corPacman
        
        if not invert:
            corObstaculos = color(50, 0, 200)
            corFronteira = color(80, 60, 200)
            corBolas = color(255)
        else:
            corObstaculos = color(255, 69, 0)
            corFronteira = color(255, 0, 0)
        
        if not speed:
            frameRate(200)
        else:
            if not godmode:
                corPacman = color(0, 255, 0)
            frameRate(350)
            if not speedUp.isPlaying():
                speed = False
        
        if godmode and speed:
            corPacman = color(255, 128, 0)
        elif not godmode and not speed:
            corPacman = color(255, 255, 0)
        
        if not godmode:
            if god.isPlaying():
                god.pause()
            detectGhost()
        else:
            if speed:
                corPacman = color(255, 0, 255)
            if not god.isPlaying():
                god.loop()
        
        if not silence.isPlaying():
            godmode = False
        
        desenharLabirinto()
        definePath()
        desenharPontos()
        printSpecials()
        desenharPacman()
        desenhaFantasmas()
        ghostPath()
        checkEvent()
        
        px = (px + width) % width
        keyPressed()
        detectWall()
        
        global numOnScreen, numEaten
        numOnScreen = ballCount()
        eatBall()
        numEaten = 90 - numOnScreen
        score = numEaten
        
        if not intro.isPlaying():
            sound()
        
        victoryCheck()
    elif stage == "death":
        background(0)
        textFont(lotFont)
        fill(255, 0, 0)
        textSize(80)
        text("GAME OVER", (width/2)-260, height/2)
        textFont(crackmanFont)
        fill(255, 255, 0)
        textSize(40)
        text("Score: {0}".format(numEaten), (width/2)-250, (height/2)+120)
        if isHighscore():
            fill(0, 255, 0)
            textSize(30)
            text("You've reached the leaderboard!", (width/2)-330, (height/2)+50)
        buttonHighlight()
        writeToFile()
    elif stage == "victory":
        chump.mute()
        ghosts.mute()
        background(0)
        textFont(lotFont)
        fill(0, 255, 0)
        textSize(60)
        text("VICTORY!", (width/2)-170, height/2)
        textFont(crackmanFont)
        fill(255, 255, 0)
        textSize(40)
        text("Score: {0}".format(score), (width/2)-250, (height/2)+100)
        textFont(lotFont)
        buttonHighlight()
        writeToFile()
    elif stage == "pause":
        noLoop()
        textFont(lotFont)
        fill(255, 255, 0)
        textSize(40)
        text("Paused", centroX(6)-8, centroY(4)+14)

def mousePressed():
    global stage
    if stage == "menu":
        if 90 < mouseX < 230 and 285 < mouseY < 330:
            stage = "ready"
            intro.play()
        elif 90 < mouseX < 400 and 335 < mouseY < 380:
            stage = "leaderboard"
        elif 90 < mouseX < 210 and 385 < mouseY < 430:
            exit()
    elif stage == "leaderboard":
        if 290 < mouseX < 400 and 410 < mouseY < 460:
            stage = "menu"
    elif stage in ["death", "victory"]:
        if 200 < mouseX < 500 and 410 < mouseY < 450:
            global direction
            direction = "right"
            setup()
            intro.play()
            stage = "ready"
        elif 200 < mouseX < 500 and 460 < mouseY < 490:
            exit()

def buttonHighlight():
    if stage == "menu":
        textFont(lotFont)
        if 90 < mouseX < 230 and 285 < mouseY < 330:
            fill(0, 247, 255)
            textSize(50)
            text("Play", 80, 320)
        else:
            fill(255, 255, 0)
            textSize(40)
            text("Play", 80, 320)
        
        if 90 < mouseX < 400 and 335 < mouseY < 380:
            fill(0, 247, 255)
            textSize(50)
            text("Leaderboard", 80, 370)
        else:
            fill(255, 255, 0)
            textSize(40)
            text("Leaderboard", 80, 370)
        
        if 90 < mouseX < 210 and 385 < mouseY < 430:
            fill(0, 247, 255)
            textSize(50)
            text("Exit", 80, 420)
        else:
            fill(255, 255, 0)
            textSize(40)
            text("Exit", 80, 420)
    elif stage == "leaderboard":
        if 290 < mouseX < 400 and 410 < mouseY < 460:
            fill(0, 247, 255)
            textSize(50)
            text("Back", 300, 450)
        else:
            fill(255, 255, 0)
            textSize(40)
            text("Back", 300, 450)
    elif stage in ["death", "victory"]:
        textFont(lotFont)
        if 200 < mouseX < 500 and 410 < mouseY < 450:
            fill(0, 247, 255)
            textSize(50)
            text("Play again", 230, 440)
        else:
            fill(255, 255, 0)
            textSize(40)
            text("Play again", 230, 440)
        
        if 200 < mouseX < 500 and 460 < mouseY < 490:
            fill(0, 247, 255)
            textSize(50)
            text("Exit", 300, 490)
        else:
            fill(255, 255, 0)
            textSize(40)
            text("Exit", 300, 480)

def desenharPacman():
    fill(corPacman)
    pushMatrix()
    translate(px + vx, py - vy)
    if direction == "left":
        rotate(PI)
    elif direction == "down":
        rotate(HALF_PI)
    elif direction == "up":
        rotate(PI + HALF_PI)
    
    if vx != 0 or vy != 0:
        arc(0, 0, pRaio, pRaio, map((millis() % 350), 50, 300, 0, 0.52), map((millis() % 350), 50, 300, TWO_PI, 5.76))
    else:
        arc(0, 0, pRaio, pRaio, QUARTER_PI, (7*PI/4))
    popMatrix()

def desenharLabirinto():
    fill(0)
    stroke(corFronteira)
    strokeWeight(espacamento)
    rect(margemH, margemV, width - 2*margemH, height - 2*margemV)
    fill(0)
    noStroke()
    rect(0, centroY(6)-25, 25, 50)
    stroke(corFronteira)
    line(centroX(0), centroY(6)-25, centroX(1)-25, centroY(6)-25)
    line(centroX(0), centroY(6)+25, centroX(1)-25, centroY(6)+25)
    noStroke()
    rect(centroX(nCol)-25, centroY(6)-25, 25, 50)
    stroke(corFronteira)
    line(centroX(nCol), centroY(6)-25, centroX(nCol+1)-25, centroY(6)-25)
    line(centroX(nCol), centroY(6)+25, centroX(nCol+1)-25, centroY(6)+25)
    
    fill(corObstaculos)
    rect(centroX(1), centroY(1), tamanho*3, tamanho)
    rect(centroX(6), centroY(1), tamanho*3, tamanho)
    rect(centroX(1), centroY(3), tamanho, tamanho*3)
    rect(centroX(3), centroY(3), tamanho*3, tamanho)
    rect(centroX(7), centroY(3), tamanho, tamanho*3)
    rect(centroX(9), centroY(3), tamanho*3, tamanho)
    rect(centroX(4), centroY(5), tamanho*3, tamanho)
    rect(centroX(1), centroY(7), tamanho*3, tamanho)
    rect(centroX(5), centroY(7), tamanho*3, tamanho)
    rect(centroX(9), centroY(7), tamanho*3, tamanho)
    rect(centroX(3), centroY(8), tamanho, tamanho*2)
    rect(centroX(9), centroY(8), tamanho, tamanho*2)

def desenharPontos():
    fill(corBolas)
    noStroke()
    for i in range(1, nCol+1):
        for j in range(1, nLin+1):
            if path[j][i] == 1:
                ellipse(centroX(i), centroY(j), 10, 10)

def printSpecials():
    fill(255, 0, 0)
    noStroke()
    ellipse(centroX(1), centroY(1), 20, 20)
    ellipse(centroX(nCol), centroY(1), 20, 20)
    ellipse(centroX(1), centroY(nLin), 20, 20)
    ellipse(centroX(nCol), centroY(nLin), 20, 20)

def desenhaFantasmas():
    global red_px, red_py, blue_px, blue_py, pink_px, pink_py, orange_px, orange_py
    
    # Fantasma vermelho
    fill(red)
    ellipse(red_px, red_py, 30, 30)
    
    # Fantasma azul
    fill(blue)
    ellipse(blue_px, blue_py, 30, 30)
    
    # Fantasma rosa
    fill(pink)
    ellipse(pink_px, pink_py, 30, 30)
    
    # Fantasma laranja
    fill(orange)
    ellipse(orange_px, orange_py, 30, 30)

def ghostPath():
    global red_px, red_py, blue_px, blue_py, pink_px, pink_py, orange_px, orange_py
    global red_vx, red_vy, blue_vx, blue_vy, pink_vx, pink_vy, orange_vx, orange_vy
    global pink_pathCount, orange_pathCount
    
    # Movimento do fantasma vermelho
    if frameCount % 60 == 0:
        red_vx, red_vy = random(-1, 1), random(-1, 1)
    
    red_px += red_vx
    red_py += red_vy
    
    # Movimento do fantasma azul
    if frameCount % 120 == 0:
        blue_vx, blue_vy = random(-1, 1), random(-1, 1)
    
    blue_px += blue_vx
    blue_py += blue_vy
    
    # Movimento do fantasma rosa
    if pink_pathCount == 0 or frameCount % 180 == 0:
        pink_vx, pink_vy = random(-1, 1), random(-1, 1)
        pink_pathCount = int(random(50, 150))
    
    pink_px += pink_vx
    pink_py += pink_vy
    pink_pathCount -= 1
    
    # Movimento do fantasma laranja
    if orange_pathCount == 0 or frameCount % 240 == 0:
        orange_vx, orange_vy = random(-1, 1), random(-1, 1)
        orange_pathCount = int(random(30, 100))
    
    orange_px += orange_vx
    orange_py += orange_vy
    orange_pathCount -= 1

def checkEvent():
    global invert, speed, godmode
    
    if frameCount % 1800 == 0:  # A cada 30 segundos
        invert = True
    elif frameCount % 1800 == 300:  # 5 segundos depois
        invert = False
    
    if frameCount % 3600 == 0:  # A cada 1 minuto
        speed = True
        speedUp.play()
    
    if frameCount % 5400 == 0:  # A cada 1.5 minutos
        godmode = True
        silence.play()

def keyPressed():
    global direction, vx, vy, pause, stage
    
    if key == CODED:
        if keyCode == LEFT:
            direction = "left"
            vx, vy = -vel, 0
        elif keyCode == RIGHT:
            direction = "right"
            vx, vy = vel, 0
        elif keyCode == UP:
            direction = "up"
            vx, vy = 0, vel
        elif keyCode == DOWN:
            direction = "down"
            vx, vy = 0, -vel
    elif key == 'p' or key == 'P':
        pause = not pause
        if pause:
            stage = "pause"
            noLoop()
        else:
            stage = "game"
            loop()

def detectWall():
    global px, py, vx, vy
    
    nextX = px + vx
    nextY = py - vy
    
    col = int((nextX - margemH) / tamanho)
    lin = int((nextY - margemV) / tamanho)
    
    if path[lin][col] == 0:
        vx = vy = 0

def ballCount():
    count = 0
    for i in range(1, nCol+1):
        for j in range(1, nLin+1):
            if path[j][i] == 1:
                count += 1
    return count

def eatBall():
    global px, py, numEaten
    
    col = int((px - margemH) / tamanho)
    lin = int((py - margemV) / tamanho)
    
    if path[lin][col] == 1:
        path[lin][col] = 2
        numEaten += 1
        if soundOn:
            chump.play()

def sound():
    global soundOn
    
    if not chump.isPlaying() and not ghosts.isPlaying():
        ghosts.loop()

def victoryCheck():
    global stage
    
    if numEaten == 90:
        stage = "victory"

def isHighscore():
    return score > min(leaderboard)

def writeToFile():
    global leaderboard, scores
    
    if isHighscore():
        leaderboard.append(score)
        leaderboard.sort(reverse=True)
        leaderboard = leaderboard[:5]
        
        with open("leaderboard.txt", "w") as f:
            for score in leaderboard:
                f.write(str(score) + "\n")

def readLeaderboard():
    global leaderboard
    
    with open("leaderboard.txt", "r") as f:
        leaderboard = [int(line.strip()) for line in f]
    
    leaderboard.sort(reverse=True)
    leaderboard = leaderboard[:5]

def readFile():
    global path
    
    with open("labirinto.txt", "r") as f:
        for i, line in enumerate(f):
            for j, char in enumerate(line.strip()):
                path[i+1][j+1] = int(char)

def centroX(col):
    return margemH + (col - 0.5) * tamanho

def centroY(lin):
    return height - (margemV + (lin - 0.5) * tamanho)

def detectGhost():
    global stage
    
    if (abs(px - red_px) < pRaio and abs(py - red_py) < pRaio) or \
       (abs(px - blue_px) < pRaio and abs(py - blue_py) < pRaio) or \
       (abs(px - pink_px) < pRaio and abs(py - pink_py) < pRaio) or \
       (abs(px - orange_px) < pRaio and abs(py - orange_py) < pRaio):
        stage = "death"
        death.play()

def definePath():
    global path
    
    for i in range(1, nLin+1):
        for j in range(1, nCol+1):
            if path[i][j] == 0:
                fill(corObstaculos)
                rect(centroX(j) - tamanho/2, centroY(i) - tamanho/2, tamanho, tamanho)
