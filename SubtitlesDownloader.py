import PySimpleGUI as psg
import SubliminalHandler as sh
import os.path

psg.theme('DarkGrey5')

layout = [
   [
      psg.Text(text='SEARCH', pad=(0,20), font=('Helvetica 16 bold'))
   ],
   [
      psg.Text('TV Show:', size=(8,1)),
      psg.InputText(size=(30,1),key='-NAME-',focus=True)
   ],
   [
      psg.Text('Season:', size=(8,1)),
      psg.InputText(size=(5,1),key='-SEASON-'),
      psg.Text('Episode:'),
      psg.InputText(size=(5,1),key='-EPISODE-'),
      # psg.Text('Provider:',size=8),
      # psg.OptionMenu([
      #    'ALL',
      #    'OpenSubtitles',
      #    'Addic7ed',
      #    'LegendasTV',
      #    'Podnapisi',
      #    'Shooter',
      #    'TheSubDB',
      #    'TvSubtitles',
      # ], default_value='OpenSubtitles',key='-PROVIDER-'),
      psg.Button('Search')
   ],
   [
      psg.Text('_'*30, pad=(0,10))
   ],
   [
      psg.Text('RESULTS',pad=(0,20), font=('Helvetica 16 bold'))
   ],
   [
      psg.Text('Fetching subtitles...',visible=False,key='-PROGRESS-',pad=(0,10),justification='center',expand_x=True),
   ],
   [
      psg.Table(
         headings=['Score','Provider','Title','Page link'],
         values=[],
         display_row_numbers=True,
         key='-RESULTS TABLE-',
         justification='left',
         visible=False,
         auto_size_columns=False,
         col_widths=[5,10,25,45],
         expand_x=True,
         enable_events=True
      )
   ],
   [
      psg.Text('_'*30, pad=(0,10))
   ],
   [
      psg.Text('DOWNLOAD',pad=(0,20), font=('Helvetica 16 bold'))
   ],
   [
      psg.In(key='-OUTPUT FOLDER-',size=(20,1),default_text='C:\\Users\\Shnrz\\Desktop'),
      psg.FolderBrowse('Choose folder'),
      psg.Button('Download')
   ],
   [
      psg.Button('Close')
   ],
   [
      psg.Text('',pad=(0,3))
   ]
]

window = psg.Window(
   'Subtitles Downloader',
   layout,
   use_custom_titlebar=True,
   resizable=True,
   margins=(50,50)
)
window.finalize()
window['-NAME-'].set_focus(force = False)

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

def UpdateResultsTable(subs_list):
   window['-PROGRESS-'].update(value='Compiling results...')
   table_rows = []
   for s in subs_list:
      table_rows.append([
         str(sh.GetSubScore(s)),
         s.provider_name,
         s.title,
         s.page_link
      ])
   window['-PROGRESS-'].update(visible=False,value='Fetching subtitles...')
   window['-RESULTS TABLE-'].update(values=table_rows, visible=True)

while True:
   event, values = window.read()

   if event == 'Search':
      print('Search button was pressed')
      print('Validating input values...')
      if ValidateInputs(values):
         print('Getting subs list...')
         window['-PROGRESS-'].update(visible=True)
         window['-RESULTS TABLE-'].update(visible=False)
         window.perform_long_operation(lambda: sh.GetSubsList(values), '-SUB LIST OBTAINED-')
      else:
         print('Inputs are wrong')
         psg.popup_error('Invalid values were input')

   elif event == '-SUB LIST OBTAINED-':
      global sub_results
      sub_results = values['-SUB LIST OBTAINED-']
      print('Updating results table...')
      window.perform_long_operation(lambda: UpdateResultsTable(sub_results), '-TABLE COMPILED-')

   elif event == '-RESULTS TABLE-':
      print(values['-RESULTS TABLE-'])
      global selected_subs
      selected_subs = sub_results[values[event][0]]

   elif event == 'Download':
      print('Download button was pressed')

      if values['-OUTPUT FOLDER-'] == None or values['-OUTPUT FOLDER-'] == '':
         psg.popup_error('Please select a destination folder.')
      elif len(values['-RESULTS TABLE-']) <= 0:
         psg.popup_error('Please click a row in the results table.')

      else:
         subs_path = values['-OUTPUT FOLDER-'] + '\\' + values['-NAME-'] + ' S' + values['-SEASON-'] + 'E' + values['-EPISODE-'] + '.en.srt'
         print('Downloading subs to: ' + subs_path + ' ...')
         sh.DownloadSubs(selected_subs, values['-OUTPUT FOLDER-'])
         if os.path.isfile(subs_path):
            psg.popup('Subtitles were successfully downloaded!')
         else:
            psg.popup_error('There was a problem downloading the subtitles.')

   elif event in (psg.WIN_CLOSED,'Close'):
      break

window.close()
