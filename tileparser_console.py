#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function, division
from merge_tiles import BingMerger, VERSION, get_available_layers

layers = get_available_layers()
STEP = 1

def step(fn):
    def wrapped(*args):
        print('%s.' % STEP, '-'*77)
        return fn(*args)
    return wrapped

@step
def input_service():
    print('Choose service for downloading tiles:')
    list_layers = list(layers)
    for e, l in enumerate(list_layers):
        print('  %s - %s' % (e, l))
    selected = raw_input('> ')
    try:
        if selected.isdigit():
            service_no = int(selected)
            assert service_no <= len(layers)
            return layers[list_layers[service_no]]
        elif selected in list_layers:
            return layers[selected]
        raise Exception()
    except Exception:
        print('Service not valid! Try again')
        return input_service()

@step
def input_zoom():
    print('Enter the zoom-level [0 - 21]:')
    try:
        zoom_level = int(raw_input('> '))
        assert 0 <= zoom_level <= 22
        return zoom_level
    except Exception:
        print('Error when entering the zoom-level! Try again')
        return input_zoom()

@step
def input_latlon(message):
    print(message)
    try:
        xy_input = map(float, raw_input('> ').rstrip().split())
        if len(xy_input) == 2:
            lat, lon = xy_input
        elif len(xy_input) == 6:
            l = lambda g, m, s: g+(m/60.0)+(s/3600.0)
            lat = l(*xy_input[:-3])
            lon = l(*xy_input[-3:])
        else:
            raise Exception()
        print(lat, lon)
        assert abs(lat) <= 90
        assert abs(lon) <= 180
        return lat, lon
    except Exception:
        print('!'*80)
        print('Error when entering the coordinates! Try again')
        return input_latlon(message)

if __name__ == '__main__':
    message = """
    \r================================================================================
    \r====================         TILE MAPS PARSER v{}           ===================
    \r================================================================================
    """.format(VERSION)
    print(message)
    lower_left_text = """Enter the coordinates of the lower left corner:
    Format: gg.gggg or gg mm ss
    Example:
      51.31688 103.16162
      51 19 0.76 103 9 41.83
     _______
    |       |
    |       |
    #_______|
    """
    upper_right_text = """Enter the coordinates of the upper right corner:
    Format: gg.gggg or gg mm ss
    Example:
      56.09655 110.34667
      56 5 47.6 110 20 48.04
     _______
    |       #
    |       |
    |_______|
    """
    service = input_service()
    STEP += 1
    lat_min, lon_min = input_latlon(lower_left_text)
    STEP += 1
    lat_max, lon_max = input_latlon(upper_right_text)
    STEP += 1
    zoom_level = input_zoom()
    tile = service(zoom=zoom_level, bbox=(lat_min, lon_min, lat_max, lon_max), threads=15)
    print('='*80)
    count = tile.download()
    tile.merge_tiles()
    print('Press Enter to exit.')
    raw_input()
