import inspect, sys, zhmiscellany, keyboard
from PIL import ImageGrab
global get_pos_cooldown
def adding(a, b):
    return a + b

def get_pos(key='f10', kill=False):
    def _get_pos(key):
        while True:
            keyboard.wait(key)
            image = ImageGrab.grab()
            x, y = zhmiscellany.misc.get_mouse_xy()
            rgb = image.getpixel((x, y))
            color = f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"
            reset = "\033[0m"
            print(f"Coordinates: ({x}, {y}), RGB: {rgb} {color}████████{reset}")
            if kill:
                print('killing process')
                zhmiscellany.misc.die()
    zhmiscellany.processing.start_daemon(target=_get_pos, args=(key,))

    
class k:
    pass

current_module = sys.modules[__name__]
for name, func in inspect.getmembers(current_module, inspect.isfunction):
    if not name.startswith('_'):
        setattr(k, name, func)

if '__main__' in sys.modules:
    sys.modules['__main__'].__dict__['k'] = k
