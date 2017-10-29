from cowtermcolor import *;

_INFO  = Color(BLUE);
_DEBUG = Color(GREEN);
_WARN  = Color(YELLOW);
_ERROR = Color(RED);

class log:
    @staticmethod
    def I(fmt, *args):
        _print(_INFO("(INFO):"), fmt, *args);

    @staticmethod
    def D(fmt, *args):
        _print(_DEBUG("(DEBUG):"), fmt, *args);

    @staticmethod
    def W(fmt, *args):
        _print(_WARN("(WARN):"), fmt, *args);

    @staticmethod
    def E(fmt, *args):
        _print(_ERROR("(ERROR):"), fmt, *args);

def _print(prefix, fmt, *args):
    if(args is None):
        print prefix + fmt;

    print prefix + fmt.format(*args);


