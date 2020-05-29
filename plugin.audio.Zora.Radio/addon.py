import sys
import os
import urllib
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import logging
from operator import itemgetter

def show_tags():
  tag_handle = int(sys.argv[1])
  xbmcplugin.setContent(tag_handle, 'tags')

  for tag in tags:
    iconPath = os.path.join(home, 'logos', tag['icon'])
    li = xbmcgui.ListItem(tag['name'], iconImage=iconPath)
    url = sys.argv[0] + '?tag=' + str(tag['id'])
    xbmcplugin.addDirectoryItem(handle=tag_handle, url=url, listitem=li, isFolder=True)

  xbmcplugin.endOfDirectory(tag_handle)


def show_streams(tag):
  stream_handle = int(sys.argv[1])
  xbmcplugin.setContent(stream_handle, 'streams')
  logging.warning('TAG show_streams!!!! %s', tag)
  for stream in streams[str(tag)]:
    logging.debug('STREAM HERE!!! %s', stream['name'])
    iconPath = os.path.join(home, 'logos', stream['icon'])
    li = xbmcgui.ListItem(stream['name'], iconImage=iconPath)
    xbmcplugin.addDirectoryItem(handle=stream_handle, url=stream['url'], listitem=li)

  xbmcplugin.endOfDirectory(stream_handle)


def get_params():
  """
  Retrieves the current existing parameters from XBMC.
  """
  param = []
  paramstring = sys.argv[2]
  if len(paramstring) >= 2:
    params = sys.argv[2]
    cleanedparams = params.replace('?', '')
    if params[len(params) - 1] == '/':
      params = params[0:len(params) - 2]
    pairsofparams = cleanedparams.split('&')
    param = {}
    for i in range(len(pairsofparams)):
      splitparams = {}
      splitparams = pairsofparams[i].split('=')
      if (len(splitparams)) == 2:
        param[splitparams[0]] = splitparams[1]
  return param


def lower_getter(field):
  def _getter(obj):
    return obj[field].lower()

  return _getter


addon = xbmcaddon.Addon()
home = xbmc.translatePath(addon.getAddonInfo('path'))

tags = [
  {
    'name': 'Radio',
    'id': 'Radio',
    'icon': 'radio.png'
  }, {
    'name': 'Hessen',
    'id': 'Hessen',
    'icon': 'hessen.png'
  }
]


Radio = [{
  'name': 'Radio Paloma',
  'url': 'http://www.surfmusik.de/m3u/radio-paloma-100-deutscher-schlager,10838.m3u',
  'icon': 'Radio Paloma.png',
  'disabled': False
}, {
  'name': '89.0 RTL',
  'url': 'http://sites.89.0rtl.de/live/streamhigh.m3u',
  'icon': '89.0 RTL.png',
  'disabled': False
}, {
  'name': 'You FM',
  'url': 'http://metafiles.gl-systemhaus.de/hr/youfm_2.m3u',
  'icon': 'You FM.png',
  'disabled': False
}, {
  'name': 'Planet Radio',
  'url': 'http://streams.planetradio.de/planetradio/mp3/hqlivestream.m3u',
  'icon': 'Planet Radio.png',
  'disabled': False
}]


Hessen = [{
  'name': 'hr3',
  'url': 'http://metafiles.gl-systemhaus.de/hr/hr3_2.m3u',
  'icon': 'hr3.png',
  'disabled': False
}, {
  'name': 'hr4',
  'url': 'http://metafiles.gl-systemhaus.de/hr/hr4_2.m3u',
  'icon': 'hr4.png',
  'disabled': False
}, {
  'name': 'Radio Teddy',
  'url': 'http://streamtdy.ir-media-tec.com/live/mp3-128/web/play.m3u',
  'icon': 'radio teddy.png',
  'disabled': False
}, {
  'name': 'FFH Hessen',
  'url': 'http://streams.ffh.de/radioffh/mp3/hqlivestream.m3u',
  'icon': 'FFH Hessen.png',
  'disabled': False
}]


streams = {
  'Radio': sorted((i for i in Radio if not i.get('disabled', False)), key=lower_getter('name')),
  'Hessen': sorted((i for i in Hessen if not i.get('disabled', False)), key=lower_getter('name')),
  # 'Radio': sorted(Radio, key=lower_getter('name')),
  # 'Hessen': sorted(Hessen, key=lower_getter('name')),
}

PARAMS = get_params()
TAG = None
logging.warning('PARAMS!!!! %s', PARAMS)

try:
  TAG = PARAMS['tag']
except:
  pass

logging.warning('ARGS!!!! sys.argv %s', sys.argv)

if TAG == None:
  show_tags()
else:
  show_streams(TAG)
