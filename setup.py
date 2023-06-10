"""Fichier d'installation de notre script salut.py."""

from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "Pykarun",
    version = "0.9",
    description = "Jeu créé sous pygame par Sidane Alp dans le cadre d'un projet en ISN. Il a été de base en groupe avec Amine mais il ne participe plus au projet désormais",
    executables = [Executable("Pykarun.py")],
)