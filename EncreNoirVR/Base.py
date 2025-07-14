import sys
import time
import itertools

def loading_animation(duration=5, interval=0.1):
    """
    Affiche une animation de chargement dans la console.
    
    Args:
        duration (float): durée totale de l'animation en secondes.
        interval (float): intervalle entre chaque rafraîchissement en secondes.
    """
    spinner = itertools.cycle(['─', '\\', '|', '/'])
    end_time = time.time() + duration
    while time.time() < end_time:
        sys.stdout.write(f'\rChargement {next(spinner)}')
        sys.stdout.flush()
        time.sleep(interval)
    sys.stdout.write('\rChargement terminé !\n')

if __name__ == "__main__":
    # Lance l'animation de chargement pendant 5 secondes
    loading_animation(duration=5, interval=0.1)