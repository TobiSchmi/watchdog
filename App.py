import yaml

from WatchMe import WatchMe

try:
    with open("watchconfig.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
except:
    print("watchconfig.yml not found -> exiting...")
    exit()

def main():
    for idx in range(len(cfg["watch"]["folders"])):
        path = cfg["watch"]["folders"][idx]
        cardcolor = cfg["watch"]["foldercolor"][idx]
        interval = cfg["interval"]["seconds"]
        webhook = cfg["webhook"]["link"]
        WatchMe(path, interval, webhook, cardcolor).startWatch()

if __name__ == "__main__":
   main()