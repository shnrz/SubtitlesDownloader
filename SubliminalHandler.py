import subliminal as sub
import babelfish as bf

def GetSubScore(s):
   return sub.compute_score(s, vid)

def GetSubsList(values):
   global vid
   vid = sub.Video.fromname(values['-NAME-'] + ' S' + values['-SEASON-'] + 'E' + values['-EPISODE-'])
   subs_list = sub.list_subtitles([vid], {bf.Language('eng')})[vid]
   subs_list.sort(key=GetSubScore, reverse=True)
   return subs_list

def DownloadSubs(subtitle,dest_path):
   sub.download_subtitles([subtitle])
   sub.save_subtitles(vid,[subtitle],directory=dest_path)
