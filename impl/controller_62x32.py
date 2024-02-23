import os, inspect, sys, math, time, configparser, argparse
from PIL import Image

from apps_v2 import spotify_player_32 as spotify_player
# from apps_v2 import weather
from modules import spotify_module


def main():
    config = configparser.ConfigParser()
    parsed_configs = config.read('../config.ini')

    if len(parsed_configs) == 0:
        print("no config file found")
        sys.exit()

    canvas_width = config.getint('System', 'canvas_width', fallback=64)
    canvas_height = config.getint('System', 'canvas_height', fallback=32)

    # get arguments
    parser = argparse.ArgumentParser(
                    prog = 'RpiSpotifyMatrixDisplay',
                    description = 'Displays album art of currently playing song on an LED matrix')

    parser.add_argument('-f', '--fullscreen', action='store_true', help='Always display album art in fullscreen')
    parser.add_argument('-e', '--emulated', action='store_true', help='Run in a matrix emulator')
    args = parser.parse_args()

    is_emulated = args.emulated
    is_full_screen_always = args.fullscreen

    # switch matrix library import if emulated
    if is_emulated:
        from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions
    else:
        from rgbmatrix import RGBMatrix, RGBMatrixOptions

    # get config
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    sys.path.append(currentdir+"/rpi-rgb-led-matrix/bindings/python")


    # connect to Spotify and create display image
    modules = { 'spotify' : spotify_module.SpotifyModule(config) }
    app_list = [ spotify_player.SpotifyScreen(config, modules, is_full_screen_always) ]

    # weather
    # modules = { 'weather' : weather_module.WeatherModule(config) }
    # app_list = [ weather.WeatherScreen(config, modules, is_full_screen_always) ]

    # setup matrix
    options = RGBMatrixOptions()
    options.hardware_mapping = config.get('Matrix', 'hardware_mapping', fallback='regular')
    # options.rows = 32
    # options.cols = 64
    options.rows = canvas_height
    options.cols = canvas_width
    options.brightness = 100 if is_emulated else config.getint('Matrix', 'brightness', fallback=100)
    options.gpio_slowdown = config.getint('Matrix', 'gpio_slowdown', fallback=1)
    options.limit_refresh_rate_hz = config.getint('Matrix', 'limit_refresh_rate_hz', fallback=150)
    options.drop_privileges = False
    matrix = RGBMatrix(options = options)

    # timeout on no playback
    shutdown_delay = config.getint('Matrix', 'shutdown_delay', fallback=600)
    # when no playback, blank_screen shows
    black_screen = Image.new("RGB", (canvas_width, canvas_height), (0,0,0))
    # stores last acive time for playback timeout
    last_active_time = math.floor(time.time())

    # generate image
    while(True):
        frame, is_playing = app_list[0].generate()
        current_time = math.floor(time.time())

        if frame is not None:
            if is_playing:
                last_active_time = math.floor(time.time())
            elif current_time - last_active_time >= shutdown_delay:
                # TODO: if not playing, show the weather or something.
                frame = black_screen
        else:
            frame = black_screen

        matrix.SetImage(frame)
        # time.sleep(0.08)
        time.sleep(5)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted with Ctrl-C')
        sys.exit(0)
