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
