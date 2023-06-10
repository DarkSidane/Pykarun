import pygame
import math 
import copy
from random import choice

pygame.init() #Initialisation de pygame

SIZE = WIDTH, HEIGHT = 800 , 620  # Largeur et hauteur de la fenêtre
BACKGROUND_COLOR = pygame.Color('white') #Couleur d'arrière plan
POS_SOL_Y = 405 
FPS = 75
LO = 75

SCORE = 0
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PIKATOMBE = False #Acesseur disant si Pikachu tombe ou pas
SON = True
BOING = False

"Les sons"
sound_pikachu = pygame.mixer.Sound("files/Sounds/Pikachuuu.wav")
sound_pika = pygame.mixer.Sound("files/Sounds/Pika Pika.wav")
sound_agonies = [pygame.mixer.Sound("files/Sounds/Agonie 1.wav"),pygame.mixer.Sound("files/Sounds/Agonie 2.wav"), pygame.mixer.Sound("files/Sounds/Agonie 1.wav"),pygame.mixer.Sound("files/Sounds/Agonie 3.wav"),pygame.mixer.Sound("files/Sounds/Agonie 4.wav")]
sound_vitesse = pygame.mixer.Sound("files/Sounds/Vitesse.wav")
sound_boing = pygame.mixer.Sound("files/Sounds/Boing.wav")
sound_nani = pygame.mixer.Sound("files/Sounds/Nani.wav")


class Pikachu(pygame.sprite.Sprite): # Pikachu héritant de la classe Sprite venant du module pygame.sprite
    def __init__(self): 
        global BOING
        BOING = True
        super(Pikachu, self).__init__() #"Collage" des attributs et méthode de la classe Sprite de Pygame

        self.images = []  #Image qu'on va utiliser pour l'animation
        self.imagesRunG = []
        self.imagesRunD = []
        self.imagesStop = []
        self.image = pygame.image.load("files/Images/Pikachu.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()  , self.image.get_height()  ))

        # Pour ajouter de nouvelle image suffit de rajouter des images dans la liste "self.images"
        self.imagesStop.append(self.image.subsurface(0,0,38 ,40 ))
        self.imagesStop.append(self.image.subsurface(38 ,0,40 ,40 )) #Ajoute un par un image
        self.imagesStop.append(self.image.subsurface(77 ,0 ,40 ,40 ))
        self.imagesStop.append(self.image.subsurface(117 ,0 ,38 ,40 ))
        self.imagesStop.append(self.image.subsurface(155 ,0,37 ,40 )) 
        self.imagesStop.append(self.image.subsurface(117 ,0,38 ,40 ))
        self.imagesStop.append(self.image.subsurface(77 ,0,40 ,40 ))
        self.imagesStop.append(self.image.subsurface(38 ,0 ,40 ,40 ))
        self.imagesStop.append(self.image.subsurface(0,0,38 ,40 ))

        #Rebelote
        self.imagesRunG.append(self.image.subsurface(0,42 ,47 ,36 ))
        self.imagesRunG.append(self.image.subsurface(47 ,42 ,47 ,36 ))
        self.imagesRunG.append(self.image.subsurface(94 ,41 ,45 ,37 ))
        self.imagesRunG.append(self.image.subsurface(139 ,41 ,44 ,37 ))
        self.imagesRunG.append(self.image.subsurface(184 ,42 ,46 ,36 ))
        self.imagesRunG.append(self.image.subsurface(230 ,42 ,46 ,36 ))

        for e in self.imagesRunG :
            self.imagesRunD.append(pygame.transform.flip(e, True, False))

        self.index = 0

        self.criDeGuerre = False # Quand Pika va trop vite
        self.stopCri = False
        self.pykaHurle = True

        self.coefR = 10 
        self.coefAnimation = 6 # Coefficient pour ralentir animation Pikachu, ne jamais mettre égal à 0

        
        self.images = self.imagesStop

        self.image = self.images[self.index] # Image affiché à l'écran

        POS_SOL_Y = 405  #Hauteur du sol relatif à Pikachu, mis à jour 
        self.rect = pygame.Rect(20 , POS_SOL_Y, 50 , 50 ) #Positon X, Y, largeur, hauteur

        self.statut = "stop"
        self.enTrainDeSauter = False
        self.jump = True

        self.posX = 0

    def update(self):
        """Met à jour notre Pikachu, sur ses images, sa position...
        Fonction répétée plein de fois """

        #Choix des sprites d'animation
        if not self.enTrainDeSauter :
            if self.statut == "stop" :
                self.images = self.imagesRunD 
                self.coefAnimation = 6
                if self.rect.y != POS_SOL_Y :
                    self.enTrainDeSauter = True
                    self.jump = False
                if not(pygame.mixer.get_busy()) :
                    if SON : 
                        if self.criDeGuerre :
                            sound_vitesse.play()
                            self.criDeGuerre = False
                            self.stopCri = True
                        else :
                            sound_pika.play()
            elif self.statut == "saut" :
                self.enTrainDeSauter = True
                self.rect.y -= 5 # Seule solution que j'ai trouvé pour faire décoller le personnage et remplir la condition @1
                self.jump = True
                self.coefAnimation = 20
                if SON : sound_pikachu.play()
        else :
            if self.rect.y == POS_SOL_Y : #condition @1 : personnage arrête de sauter quand il ré-atterit au sol
                self.enTrainDeSauter = False
            else :
                if self.rect.y >= 280  and self.jump :
                    self.rect.y -= 5
                else :
                    self.jump = False
                    if self.rect.y <= (POS_SOL_Y - 30) :
                        self.rect.y += 5
                    elif self.rect.y <= POS_SOL_Y :
                        self.rect.y += 1
                    else : 
                        self.rect.y += 10
        if (SCORE >= 90000) and not(self.stopCri): 
            self.criDeGuerre = True
        # Changement de sprites
        if (self.coefR % self.coefAnimation) == 0 : # Plus % 5 est grand plus PIka est ralenti
            self.index += 1
        self.coefR += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

        if self.checkTomber() and self.pykaHurle :
            self.criAgonie()
            self.pykaHurle = False
    def changeStatut(self, stat) :
        "Accesseur permettant de changer la valeur de self.statut"
        self.statut = stat
    def checkGameOver(self) :
        if self.rect.y >= 650  :
            return True
        else : 
            return False
    def checkTomber(self) :
        global PIKATOMBE
        if self.rect.y > 405 :
            PIKATOMBE = True
            return True
        else : 
            PIKATOMBE = False
            return False
    def criAgonie(self) :
        pygame.mixer.stop()
        if SON : choice(sound_agonies).play()

class Tuile() :
    def __init__(self, screen, chemin, pos = 0, etat = "plaine") :
        self.image = pygame.image.load(chemin).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width()  , self.image.get_height()))
        self.x = pos
        self.screen = screen
        self.etat = etat
    def update(self) :
        self.screen.blit(self.image, [self.x, 0])
        if not(PIKATOMBE) :
            self.x -= 5
        return self.x
    def arrive(self) :
        self.x = WIDTH #Pos fen
    def get_etat(self) :
        return self.etat
class MecaTuile() :
    def __init__(self, *args) :
        "Il faut mettre au moins deux tuiles en argument pout que cela fonctionne ! "

        self.positionAbsolueX = 20 

        self.mesTuiles = [] 
        for tuile in args :
            self.mesTuiles.append(tuile)
        # Tuiles affichées à l'écran
        self.tuile1 = copy.copy(self.mesTuiles[0]) # dit la tuile actif
        self.x1 = 0
        self.tuile2 = copy.copy(self.mesTuiles[1]) # soit la tuile qui attend d'être affiché
        self.x2 = 900  # Largeur de la fenêtre

        self.typeCurrentTuile = "plaine"
        self.chronoPiege = 0
        self.topchrono = False

        self.tuile1Attente = False
    def update(self) :
        global SCORE

        self.x1 = self.tuile1.update()
        self.x2 = self.tuile2.update()
        if self.x1 <= (-WIDTH ):
            del(self.tuile1)
            self.tuile1 = copy.copy(choice(self.mesTuiles)) 
            if self.tuile2.get_etat() == self.mesTuiles[1].get_etat() :
                self.typeCurrentTuile = "piege"
            else : 
                self.typeCurrentTuile = "plaine"
            self.tuile1.arrive()
        elif self.x2 <= (-WIDTH ):
            del(self.tuile2)
            self.tuile2 = copy.copy(choice(self.mesTuiles))
            if self.tuile1.get_etat() == self.mesTuiles[1].get_etat() :
                self.typeCurrentTuile = "piege"
            else : 
                self.typeCurrentTuile = "plaine"
            self.tuile2.arrive()
        #Maj de la pos
        self.positionAbsolueX += 10
        SCORE += 10
        self.changeSol()
    def changeSol(self) :
        "Change la position Y du sol selon l'état en cours"
        global POS_SOL_Y

        if (self.typeCurrentTuile == "piege") : 
            if self.chronoPiege >= 160 : 
                self.chronoPiege = 0
            self.topchrono = True
            if (self.chronoPiege >= 52) and (self.chronoPiege <=80) :
                POS_SOL_Y = 640 
            else : 
                POS_SOL_Y = 405 

        else : 
            POS_SOL_Y = 405 
            self.topchrono = False
            self.chronoPiege = 0
        if self.topchrono :
            self.chronoPiege += 1
class EcranDeDemarrage() :
    def __init__(self) :
        self.font = pygame.font.Font('files/Polices/KuchenHollow.ttf', 128)
        self.font1 = pygame.font.Font("files/Polices/Kid Games.ttf", 32)
        self.font2 = pygame.font.Font("files/Polices/Kid Games.ttf", 16)

        self.text = self.font.render("Pykarun Le Jeu", True, (255, 255, 0))
        self.appuie = self.font1.render("APPUYER SUR ESPACE", True, WHITE)

        self.credit = self.font2.render("FAIT PAR SIDANE POUR LE PROJET DE ISN", True, WHITE)
        self.rectCredit = self.credit.get_rect()
        self.rectCredit.center = 400, 160

        self.textRect = self.text.get_rect() 
        self.textRect.center = (400 , 100 )

        self.appuieRect = self.appuie.get_rect()
        self.appuieRect.center = (400 , 500 )

        self.image1 = pygame.image.load('files/Images/pikachus.jpg')
    def update(self, screen) :
        "Appuyer sur la touche espace pour lancer le jeu"
        screen.fill((0, 0, 0, 0.5))
        screen.blit(self.image1, (0, 0, 640, 800))
        screen.blit(self.text, self.textRect)
        screen.blit(self.appuie, self.appuieRect)
        screen.blit(self.credit, self.rectCredit)
class EcranGameOver() :
    def __init__(self) :
        self.font = pygame.font.Font("files/Polices/Kid Games.ttf", 64)
        self.text = self.font.render("GAME OVER", True, WHITE) 
        self.textRect = self.text.get_rect()
        self.textRect.center = (400 , 100)

        self.font1 = pygame.font.Font("files/Polices/Kid Games.ttf", 16)
        self.textScore = self.font1.render("VOTRE SCORE EST DE 00000 POINTS !", True, WHITE)
        self.scoreRect = self.textScore.get_rect()
        self.scoreRect.center = (400 , 575 )

        self.image = pygame.image.load("files/Images/deadPikachu.png").convert_alpha()

        self.imageEpicWin = pygame.image.load("files/Images/Nani.png").convert_alpha()
        self.win = True
        self.fontEpic = pygame.font.Font("files/Polices/Manga Bold.otf", 32)
        self.textEpic = self.fontEpic.render("INCROYABLE VOTRE SCORE EST DE 000000 POINTS !", True, WHITE)
        self.epicRect = self.textEpic.get_rect()
        self.epicRect.center = (420 , 175)

        self.retry = self.font1.render("APPUYER SUR ESPACE POUR REESSAYER", True, WHITE)
        self.retryRect = self.retry.get_rect()
        self.retryRect.center = (400, 600)
    def reprendreJeu(self) :
        global SCORE 
        SCORE = 0
        win = False
    def update(self, screen) :
        global BOING

        if not(pygame.mixer.get_busy()) and SON :
            if BOING : 
                sound_boing.play()
                BOING = False
        screen.fill((255,0,0))
        
        screen.blit(self.text, self.textRect)
        if (SCORE >= 100000):
            screen.blit(self.imageEpicWin, (300 , 200 , self.imageEpicWin.get_width() , self.imageEpicWin.get_height()))
            if self.win :
                pygame.mixer.stop()
                sound_nani.play()
                self.win = False
            self.textEpic = self.fontEpic.render("INCROYABLE VOTRE SCORE EST DE "+ str(SCORE) + " POINTS !", True, WHITE)
            screen.blit(self.textEpic, self.epicRect)
        else :
            screen.blit(self.image, (300 , 200 , self.image.get_width() , self.image.get_height()))
            self.textScore = self.font1.render("VOTRE SCORE EST DE "+ str(SCORE) + " POINTS !", True, WHITE)
            screen.blit(self.textScore, self.scoreRect)
        
        screen.blit(self.retry, self.retryRect)
class ElementsDeJeu() :
    def __init__(self) :
        #Initialisation  du score
        self.fontScore = pygame.font.Font("files/Polices/American Signs.otf", 32)
        self.score = self.fontScore.render("0 points", True, WHITE)
        self.scoreRect = self.score.get_rect() 
        self.scoreRect.center = (650 , 25 )

        self.sonLogo = pygame.image.load("files/Images/unmute.png").convert_alpha()
        self.sonRect = self.sonLogo.get_rect()
        self.sonRect.center = (50, 50)

    def updateinGame(self, screen) :
        self.score = self.fontScore.render(str(SCORE) + " points", True, WHITE)
        screen.blit(self.score, self.scoreRect)
    def update(self, screen) :
        screen.blit(self.sonLogo, self.sonRect)
    def get_rectSon(self) :
        return self.sonRect
    def changeSon(self) :
        global SON
        if SON : 
            self.sonLogo = pygame.image.load("files/Images/mute.png").convert_alpha()
            SON = False
        else : 
            self.sonLogo = pygame.image.load("files/Images/unmute.png").convert_alpha()
            SON = True

def main() :
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Pykarun : Le jeu") #Titre du jeu

    aminePika = Pikachu()
    ecranDemarrer = EcranDeDemarrage()
    ecranGameOver = EcranGameOver()
    elements = ElementsDeJeu()

    tuil1 = Tuile(screen, "files/Images/Plaine.png")

    tuil2 = Tuile(screen, "files/Images/Piege.png", WIDTH, "piege")
    tuiles = MecaTuile(tuil1, tuil2)
    my_group = pygame.sprite.Group(aminePika)
    clock = pygame.time.Clock()
    stat = "stop"
    demarrage = False


    #Gestionnaire des événements
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_RIGHT :
                    stat = "droite"
                elif event.key == pygame.K_LEFT :
                    stat = "gauche"
                elif event.key == pygame.K_SPACE :
                    stat = "saut"
            elif event.type == pygame.MOUSEBUTTONUP :
                if event.button == 1 : # Click gauche
                    if elements.get_rectSon().collidepoint(event.pos) :
                        elements.changeSon()

            else :
                stat = "stop"
        if aminePika.checkGameOver() :
            if not(pygame.mixer.get_busy()) :
                ecranGameOver.update(screen)
                if stat == "saut" :
                    ecranGameOver.reprendreJeu()
                    aminePika.__init__()
                    tuiles.__init__(tuil1, tuil2)
                    stat = "stop"
            stat = "game over"
        if (stat != "saut") and not(demarrage) :
            ecranDemarrer.update(screen)
        elif stat != "game over":
            if not demarrage :
                demarrage = True
                stat = "stop"

            "Mise à jour des tuiles"
            tuiles.update()

            "Mise à jour sprites "
            aminePika.changeStatut(stat)
            my_group.update()
            my_group.draw(screen)
            #Mise à jour des éléments 
            elements.updateinGame(screen)


        "Mise à jour de pygame"
        elements.update(screen)
        "Mise à jour difficulté"
        FPS = (SCORE * 0.00125) + 75
        pygame.display.update()
        clock.tick(FPS) # FPS MAX
main()