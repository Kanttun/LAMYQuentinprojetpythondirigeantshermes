from selenium.webdriver.common.actions.interaction import Pause
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from fake_useragent import UserAgent
import time

options = Options()
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option(
    'prefs', {'profile.managed_default_content_settings.media_stream': 2}
)
options.add_argument('--start-maximized')
options.add_argument('--disable-infobars')
#options.add_argument('--disable-extensions')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1200')
options.add_argument('--start-fullscreen')
options.add_argument('--mute-audio')
options.add_extension('./ublock.crx')
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument('--disable-notifications')
options.add_argument(
    '--disable-features=PreloadMediaEngagementData,MediaEngagementBypassAutoplayPolicies'
)
options.add_argument('--autoplay-policy=user-required')
ua = UserAgent()
user_agent = ua.random
options.add_argument(f"user-agent={user_agent}")

monpilote = webdriver.Chrome(options=options)
print('Chrome démarré')

monpilote.get('https://finance.hermes.com/fr/direction-du-groupe/')

monbouton = WebDriverWait(monpilote, timeout=10).until(expected_conditions.element_to_be_clickable((By.XPATH,'//*[@id="didomi-notice-agree-button"]')))
monbouton.click()


listZoneDirigeant = WebDriverWait(monpilote, timeout=3).until(expected_conditions.presence_of_all_elements_located ((By.XPATH, '//*[@id="main-content"]/div/section[4]/div/div/div[*]/div[2]/p[1]')))      

print('Dirigeants', len(listZoneDirigeant))

listZonePoste = WebDriverWait(monpilote, timeout=3).until(expected_conditions.presence_of_all_elements_located ((By.XPATH, '//*[@id="main-content"]/div/section[4]/div/div/div[*]/div[2]/p[2]')))


a = []
a.append( ['NomDirigeant'] )
for x in listZoneDirigeant:
  nom = x.text
  print(nom)
  if nom !="":  
    r = [ nom ]
    a.append( r )

b = []
b.append( ['Poste'] )
for x in listZonePoste :
  poste = x.text
  print(poste)
  if poste !="":  
    r = [ poste ]
    b.append( r )

resultat = []

for i in range( len(a)):
    nom = a[i][0]
    poste = b[i][0]
    resultat.append( [nom, poste] )

import csv
fichier = open( "listedirigeantetpostehermes.csv" , "w" )
écrivain = csv.writer( fichier , delimiter="," )
écrivain.writerows(resultat)
fichier.close()

input('Pause')
