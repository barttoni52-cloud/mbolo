#!/usr/bin/env python3
"""
Télécharge les photos Google Places dans ~/Downloads/photos/
Lance : python3 ~/Downloads/download_photos.py
"""
import json,os,sys,urllib.request,time

DOWNLOADS=os.path.expanduser("~/Downloads")
JSON_PATH=os.path.join(DOWNLOADS,"libreville_photos_google.json")
PHOTOS_DIR=os.path.join(DOWNLOADS,"photos")

GRN="\033[92m";YLW="\033[93m";RED="\033[91m";BLD="\033[1m";RST="\033[0m"

if not os.path.exists(JSON_PATH):
    print(f"{RED}❌ libreville_photos_google.json introuvable{RST}")
    print("Lance d'abord : python3 ~/Downloads/fetch_libreville_photos.py")
    sys.exit(1)

with open(JSON_PATH,encoding="utf-8") as f: data=json.load(f)

os.makedirs(PHOTOS_DIR,exist_ok=True)

def norm(s):
    for a,b in [("'",""),("-",""),(" ",""),("é","e"),("è","e"),("ê","e"),("â","a"),("î","i"),("ô","o"),("û","u"),("ù","u"),("à","a")]:
        s=s.lower().replace(a,b)
    return s

# Table id → nom
ID_MAP={
    "h01":"Radisson Blu Okoume Palace","h02":"Park Inn by Radisson",
    "h03":"ONOMO Hotel Libreville","h04":"Hotel Le Cristal",
    "h05":"Hotel LEET Dorian","h06":"Residence Oceane",
    "h07":"Hotel Hibiscus","h08":"Residence Hoteliere du Phare",
    "r01":"Le Lokua","r02":"Le Phare du Large","r03":"La Piazza",
    "r04":"BANTU Restaurant","r05":"Beach Club","r06":"La Voile Rouge",
    "r07":"Restaurant LYNNS","r08":"Lamaia Lounge Restaurant",
    "r09":"Restaurant Mystic Bantu","r10":"Le Palais Gourmet",
    "r11":"Restaurant Le Mississipi","r12":"L Ella","r13":"L Emir",
    "r14":"Exotica Restaurant","r15":"Le Topaz","r16":"Le QG",
    "r17":"Wapety","r18":"Restaurant U Piscadore","r19":"Le Bateau Ivre",
    "r20":"Idiora Restaurant Bar","r21":"Okoume Restaurant Lounge",
    "r22":"L Assiette d Or","r23":"Euphoria Libreville","r24":"Amaya Restaurant",
    "r25":"Olatano","r26":"La Palette Restaurant","r27":"Le Baobab",
    "r28":"Chez Marcelline","r29":"Chez Marie qui fau chaud",
    "r30":"Restaurant Senegalais","r31":"Corisco Chica chez Katia",
    "r32":"Papa Union","r33":"Illico Restaurant","r34":"Le New Palmas",
    "r35":"Le Bon Coin de Louis chez Ali","r36":"Nouveau Petit Chalut",
    "r37":"Le Bar a Bouillon Ogasso","r38":"Sky Life","r39":"River Lodge",
    "r40":"Restaurant La Polinette",
    "b01":"Le No Stress","b02":"Le Bijou Beach","b03":"Waiybar",
    "b04":"The Spot","b05":"Hype Bar Lounge","b06":"Yoka Sports Bar",
    "b07":"The Lantern","b08":"Blu Bar","b09":"The Black Moon",
    "b10":"Hama Bar","b11":"Le Kyels Bar Food","b12":"Murmure Lounge",
    "b13":"Lollipop Bar","b14":"Bar Guinness","b15":"Le Baril Authentic Bar",
    "b16":"Le Yoss","b17":"Best Vibes","b18":"Bar Lounge PN",
    "b19":"Wai Bar Radisson","b20":"Bar du Rond-point Avorbam",
    "b21":"Le Bar de Glass","b22":"La Montee Quaben",
    "b23":"Bar Cite des Ailes","b24":"Bar Owendo",
    "b25":"Calypso","b26":"Batterie IV Bar",
}

idx={norm(k):v for k,v in data.items()}
def find(nom):
    n=norm(nom)
    if n in idx: return idx[n]
    for k,v in idx.items():
        if n in k or k in n: return v
    return None

local_map={}
ok=0;err=0

print(f"\n{BLD}Téléchargement des photos dans {PHOTOS_DIR}{RST}\n")

for lid,nom in ID_MAP.items():
    r=find(nom)
    if not r or not r.get("photos"): continue
    photos=r["photos"][:3]
    local_map[lid]=[]
    for j,url in enumerate(photos):
        fname=f"{lid}_{j+1}.jpg"
        fpath=os.path.join(PHOTOS_DIR,fname)
        if os.path.exists(fpath):
            local_map[lid].append("photos/"+fname)
            ok+=1
            continue
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
            with urllib.request.urlopen(req,timeout=15) as resp:
                content=resp.read()
            if len(content)>5000:
                with open(fpath,"wb") as f: f.write(content)
                local_map[lid].append("photos/"+fname)
                print(f"  {GRN}✓{RST} {nom[:35]:<35} → {fname}")
                ok+=1
            else:
                print(f"  {YLW}~{RST} {nom[:35]:<35} → image trop petite, ignorée")
                err+=1
        except Exception as e:
            print(f"  {RED}✗{RST} {nom[:35]:<35} → {str(e)[:40]}")
            err+=1
        time.sleep(0.3)

# Sauvegarder la map locale
map_path=os.path.join(DOWNLOADS,"photos_local_map.json")
with open(map_path,"w",encoding="utf-8") as f:
    json.dump(local_map,f,ensure_ascii=False,indent=2)

print(f"\n{BLD}{'='*50}")
print(f"  ✅ {ok} photos téléchargées")
print(f"  ❌ {err} erreurs")
print(f"  📁 Dossier : {PHOTOS_DIR}")
print(f"  📄 Map : {map_path}")
print(f"{'='*50}{RST}")
print(f"\n{YLW}Étape suivante :{RST}")
print(f"  python3 ~/Downloads/mbolo_inject_local.py")
print()
