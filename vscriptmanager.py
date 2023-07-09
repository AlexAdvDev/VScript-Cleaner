import os
import shutil
import argparse

parser = argparse.ArgumentParser(description="Options for the VScript Manager", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-o")
args = parser.parse_args()
cfgfile = vars(args)

def main(option=None):
    cwd = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(cwd, "config.cfg")) as cfg:
        lines = cfg.readlines()
        for line in lines:
            line = line.replace(" ", "")
            if "fast" in line:
                sp = line.split("=")
                fast = bool(sp[1])
            if "searchForCfg" in line:
                sp = line.split("=")
                searchForCfg = bool(sp[1])

    option = cfgfile.get("o")
    if not option:
        print("Check config.cfg before using! This is crucial!")
    foundP2 = False
    if os.path.exists("C:\SteamLibrary\steamapps\common\Portal 2"):
        foundP2 = True
        P2Directory = "C:\SteamLibrary\steamapps\common\Portal 2"
    if os.path.exists("C:\Program Files\Steam\steamapps\common\Portal 2"):
        foundP2 = True
        P2Directory = "C:\Program Files\Steam\steamapps\common\Portal 2"
    if os.path.exists("C:\Program Files (x86)\Steam\steamapps\common\Portal 2"):
        foundP2 = True
        P2Directory = "C:\Program Files (x86)\Steam\steamapps\common\Portal 2"
    if not foundP2:
        if option:
            return
        P2Directory = input("Portal 2 not automatically found! Please enter your Portal 2 directory: ")
        if not os.path.exists(P2Directory):
            print("Incorrect path! Exiting...")
            return
    
    searchAreas = [os.path.join(P2Directory, "portal2_dlc3"), os.path.join(P2Directory, "portal2_dlc4")]
    searchAreas2 = ["cfg"]
    if not searchForCfg:
        searchAreas2.remove("cfg")

    if not option:
        option = input("Extract/Import: ")
    option = option.lower()

    if option == "extract":
        for area in searchAreas:
            if fast:
                search = os.scandir(area)
                cfgs = []
                for direc in search:
                    for area in searchAreas2:
                        if os.path.exists(os.path.join(direc, area)):
                            for root, dirs, files in os.walk(os.path.join(direc, area)):
                                for f in files:
                                    if f.lower().endswith(".cfg") and searchForCfg:
                                        cfgs.append(os.path.join(root, f))
            else:
                for area in searchAreas:
                    for root, dirs, files in os.walk(area):
                        for f in files:
                            if f.lower().endswith(".cfg") and searchForCfg:
                                cfgs.append(os.path.join(root, f))
            
        cwd = os.path.dirname(os.path.realpath(__file__))
        for dlc in searchAreas:
            if os.path.exists(os.path.join(dlc, "scripts", "vscripts")):
                shutil.move(os.path.join(dlc, "scripts", "vscripts"), os.path.join(cwd, "vscripts", os.path.basename(os.path.normpath(dlc))))

            for cfg in cfgs:
                with open(cfg) as f:
                    if "script" in f.read():
                        sp = cfg.split("\\")["cfg":]
                        shutil.move(cfg, os.path.join(cwd, "cfg", cfg.split("\\")["Portal 2" + 1], *sp))
        print("Extracted successfully.")
    elif option == "import":
        if os.path.exists(os.path.join(cwd, "vscripts")):
            for d in os.scandir(os.path.join(cwd, "vscripts")):
                shutil.move(d, os.path.join(P2Directory, os.path.basename(os.path.normpath(d)), "scripts", "vscripts"))
        if os.path.exists(os.path.join(cwd, "cfg")):
            for d in os.scandir(os.path.join(cwd, "cfg")):
                shutil.move(d, os.path.join(P2Directory, os.path.basename(os.path.normpath(d)), "cfg"))
        print("Imported successfully.")

if __name__ == '__main__':
    main()