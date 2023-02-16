import PySimpleGUI as psg
import subliminal as sub
import ProviderCredentials as cred
import babelfish as bf

psg.theme('DarkGrey5')

subtitles_results = []
table_headers = ['Score','Provider','Title','Page link']
table_data = []
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
      psg.Text('Fetching subtitles...',visible=False,key='-PROGRESS-',pad=(0,20)),
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

def GetSubScore(s):
   return sub.compute_score(s, vid)

def GetSubsList(values):
   window['-PROGRESS-'].update(visible=True)
   if (len(values['-SEASON-']) < 2):
      window['-SEASON-'].update('0' + values['-SEASON-'])
   if (len(values['-EPISODE-']) < 2):
      window['-EPISODE-'].update('0' + values['-EPISODE-'])
   global vid
   vid = sub.Video.fromname(values['-NAME-'] + ' S' + values['-SEASON-'] + 'E' + values['-EPISODE-'])
   subs_list = sub.list_subtitles([vid],{bf.Language('eng')})[vid]
   subs_list.sort(key=GetSubScore, reverse=True)
   return subs_list

def UpdateResultsTable(subs_list):
   window['-PROGRESS-'].update('Compiling results...')
   table_rows = []
   for s in subs_list:
      table_rows.append([
         str(GetSubScore(s)),
         type(s),
         s.title,
         s.page_link
      ])
   window['-PROGRESS-'].update(visible=False)
   window['-PROGRESS-'].update('Fetching subtitles...')
   window['-RESULTS TABLE-'].update(values=table_rows, visible=True)

while True:
   event, values = window.read()

   if event == 'Search':
      print('Search button was pressed')
      print('Validating input values...')
      if ValidateInputs(values):
         print('Getting subs list...')
         window.perform_long_operation(lambda: GetSubsList(values), '-SUB LIST OBTAINED-')
      else:
         print('Inputs are wrong')
         psg.popup_error('Invalid values were input')

   elif event == '-SUB LIST OBTAINED-':
      sub_results = values['-SUB LIST OBTAINED-']
      print('Updating results table...')
      window.perform_long_operation(lambda: UpdateResultsTable(sub_results), '-TABLE COMPILED-')

   elif event == 'Download':
      print('Download button was pressed')

   elif event in (psg.WIN_CLOSED,'Close'):
      break

window.close()
