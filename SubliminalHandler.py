import subliminal as sub
import babelfish as bf

def GetSubScore(s):
   return sub.compute_score(s, vid)

def GetSubsList(values):
   global vid
   vid = sub.Video.fromname(values['-NAME-'] + ' S' + values['-SEASON-'] + 'E' + values['-EPISODE-'])
   subs_list = sub.list_subtitles([vid],{bf.Language('eng')})[vid]
   subs_list.sort(key=GetSubScore, reverse=True)
   return subs_list

def DownloadSubs(sub,dest_path):
   sub.download_subtitles([sub])
   sub.save_subtitles(vid,[sub],directory=dest_path)

credentials = {
   'OpenSubtitles': {'username': 'shnrz','password':'4663216'},
   'Addic7ed': {'username': 'shnrz','password':'YStm4tMimj9Gfz'}
}

def get_username(provider):
   if provider in credentials:
      prov_entry = credentials.get(provider)
      return prov_entry.get('username')
   else:
      return None

def get_password(provider):
   if provider in credentials:
      prov_entry = credentials.get(provider)
      return prov_entry.get('password')
   else:
      return None
