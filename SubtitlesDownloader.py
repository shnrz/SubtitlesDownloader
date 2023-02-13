import PySimpleGUI as psg
import subliminal as sub
import ProviderCredentials as cred

psg.theme('DarkGrey5')

subtitles_results = []
table_headers = ['Provider','Name']
table_data = [
   ['OpenSubtitles',  'Subtitles 1'],
   ['OpenSubtitles',  'Subtitles 2'],
   ['Addic7ed',       'Subtitles 3'],
   ['Podnapisi',      'Subtitles 4']
]
layout = [
   [
      psg.Text(text='SEARCH PARAMETERS', pad=(0,20), font=('Helvetica 16 bold'))
   ],
   [
      psg.Text('TV Show:', size=(8,1)),
      psg.InputText(size=(30,1),key='-NAME-'),
      psg.Text('Season:'),
      psg.InputText(size=(5,1),key='-SEASON-'),
      psg.Text('Episode:'),
      psg.InputText(size=(5,1),key='-EPISODE-')
   ],
   [
      # psg.Text('TVDB Id:',size=(10,1)),
      # psg.InputText(size=(10,1),key='-ID-'),
      psg.Text('Provider:',size=8),
      psg.OptionMenu([
         'ALL',
         'OpenSubtitles',
         'Addic7ed',
         'LegendasTV',
         'Podnapisi',
         'Shooter',
         'TheSubDB',
         'TvSubtitles',
      ], default_value='OpenSubtitles',key='-PROVIDER-'),
      psg.Button('Search')
   ],
   [
      psg.Text('_'*30, pad=(0,10))
   ],
   [
      psg.Text('SEARCH RESULTS',pad=(0,20), font=('Helvetica 16 bold'))
   ],
   [
      psg.Table(headings=table_headers,values=table_data,display_row_numbers=True,key='-RESULTS TABLE-',auto_size_columns=True,justification='center',visible=False)
   ],
   [
      psg.Button('Download'),
      psg.Button('Close')
   ],
   [
      psg.Text('',pad=(0,3))
   ]
]

window = psg.Window(
   'Subtitles Downloader',
   layout,
   use_custom_titlebar=True)

def ValidateInputs(values):
   inputs_list = [
      #'-ID-',
      '-NAME-',
      '-SEASON-',
      '-EPISODE-'
   ]
   all_good = True
   for input in inputs_list:
      if not values[input]:
         print('DEBUG ERROR: You did not enter a ' + input + '!')
         all_good = False
   return all_good

def DoSearch(values):
   if (len(values['-SEASON-']) < 2):
      window['-SEASON-'].update('0' + values['-SEASON-'])
   if (len(values['-EPISODE-']) < 2):
      window['-EPISODE-'].update('0' + values['-EPISODE-'])
   vid = sub.Video.fromname(values['-NAME-'] + ' S' + values['-SEASON-'] + 'E' + values['-EPISODE-'])
   print(vid)

while True:
   event, values = window.read()
   if event == 'Search':
      print('Search button was pressed')
      if ValidateInputs(values):
         DoSearch(values)
      else:
         print('Inputs are wrong')
   elif event == 'Download':
      print('Download button was pressed')
   elif event in (psg.WIN_CLOSED,'Close'):
      break

window.close()
