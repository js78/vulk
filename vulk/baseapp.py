from abc import ABC, abstractmethod
from collections import namedtuple
import logging

from vulk.util import millis, time_since_millis
from vulk.context import VulkWindow, VulkContext
from vulk.event import QuitEventListener


class BaseApp(ABC):
    """App must inherit this class

    The App is responsible of creating the window and manage the life
    cycle of the program.
    """

    def __init__(self, name='Vulk', x=-1, y=-1, width=640, height=480,
                 fullscreen=False, resizable=True, decorated=True,
                 highdpi=False, debug=False):
        # pylint: disable=W0612,W0613
        '''Set initial configuration

        *Parameters:*

        - `name`: Name of the application
        - `x`: X position of the window
        - `y`: Y position of the window
        - `width`: Width of the window
        - `height`: Height of the window
        - `fullscreen`: Should the window be in fullscreen mode
        - `resizable`: Should the window be resizable
        - `decorated`: Should the window be decorated (button close)
        - `highdpi`: Enable highdpi mode if supported
        - `debug`: Enable debug mode (for development only)

        **Note: When full screen mode is enabled, you can set width and
                height to 0 to use the native resolution, otherwise the
                fullscreen resolution will be set to width/height.**
        '''
        c = {k: v for k, v in locals().items() if k != 'self'}
        self.configuration = namedtuple('AppConfiguration', c.keys())(**c)

        self.last_time = 0
        self._init_logger()
        self.context = None
        self.window = None
        self.event_listeners = []
        self.request_quit = False

    def _init_logger(self):
        logger = logging.getLogger()

        if self.configuration.debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.WARNING)

        formatter = logging.Formatter('%(asctime)s :: %(levelname)s '
                                      ':: %(message)s')
        steam_handler = logging.StreamHandler()
        steam_handler.setFormatter(formatter)
        steam_handler.setLevel(logging.DEBUG)
        logger.addHandler(steam_handler)

    def __enter__(self):
        '''Create window and Vulkan context'''
        self.window = VulkWindow()
        self.window.open(self.configuration)
        self.context = VulkContext()
        self.context.create(self.window, self.configuration)
        self.start()
        return self

    def __exit__(self, *args):
        '''Clean Vulkan resource'''
        self.end()
        self.window.close()

    def quit(self):
        '''Quit the App
        This function must be called to quit App
        '''
        self.request_quit = True

    def run(self):
        '''Start the game loop'''
        self.last_time = millis()

        while not self.request_quit:
            events = self.context.get_events()
            for event in events:
                for listener in self.event_listeners:
                    listener.handle(event)

            self.render(time_since_millis(self.last_time))
            self.last_time = millis()

    @abstractmethod
    def render(self, delta):
        '''Here your game loop.

        In this function, all your game is playing.

        *Parameters:*

        - delta: The delta time since the last frame in milliseconds
        '''
        return

    @abstractmethod
    def start(self):
        '''This function is called when your App starts'''
        self.event_listeners.append(QuitEventListener(self.quit))

    @abstractmethod
    def end(self):
        '''This function is called when your App ends'''
        return
