'''
We are taking the stuff from `status.py` and converting it into class files
'''
from .constants import MinecraftServer, BASE_URL, StatusResponse, VersionDict, PlayersDict, MOTDDict, ModsDict, PluginsDict, Player, Plugin, Mod
import requests
from dataclass import dataclass

@dataclass(frozen=True)
class JavaStatusResponse(StatusResponse):
    version: VersionDict | None
    players: PlayersDict | None
    motd: MOTDDict | None
    icon: str | None
    mods: ModsDict | None
    software: str | None
    plugins: PluginsDict | None

class JavaServer(MinecraftServer):
    def __init__(self, host: str, port: int = 25565, query: bool = True):
        super().__init__()
        self.host = host
        self.port = port
        self.query = query

        self.lastValidResponse: None | JavaStatusResponse = None

    def get_status() -> JavaStatusResponse:
        host = self.host
        port = self.port
        query = self.query
        res = requests.get(f"{BASE_URL}/status/java/{host}:{port}?query={query}")

        if res.status_code != 200:
            print("Seems something went wrong, here's some debug information!")
            print(f"BASE_URL: {BASE_URL},\nHOST: {host},\nPORT: {port},\nQUERY: {query}")

            if res.text.startswith("Not Found"):
                raise ValueError("Unable to find URL, most likely the `BASE_MCSTATUS_URL` environment variable is set to an incorrect value! (leave blank for default v2)")

            raise ValueError(f"You probably should report this on GITHUB!:\n{res.text}")

        rjson = res.json()
        if "icon" in rjson.keys():
            icon = rjson["icon"]
        else:
            icon = None

        if "motd" in rjson.keys():
            motd = MOTDDict(raw=rjson["motd"]["raw"], clean=rjson["motd"]["clean"], html=rjson["motd"]["html"])
        else:
            motd = None

        if "version" in rjson.keys():
            version = VersionDict(name_raw=rjson["version"]["name_raw"], name_clean=rjson["version"]["name_clean"], name_html=rjson["version"]["name_html"], protocol=rjson["version"]["protocol"])
        else:
            version = None

        if "players" in rjson.keys():
            plrList = []
            for plr in rjson["players"]["list"]:
                plrList.append(Player(plr["uuid"], plr["name_raw"], plr["name_clean"], plr["name_html"]))
            players = PlayersDict(online=rjson["players"]["online"], max=rjson["players"]["max"], list=plrList)
        else:
            players = None

        if "mods" in rjson.keys():
            modList = []
            for mod in rjson["mods"]:
                modList.append(Mod(name=mod["name"], version=mod["version"]))
            mods = ModsDict(modList)
        else:
            mods = None

        if "software" in rjson.keys():
            software = rjson["software"]
        else:
            software = None

        if "plugins" in rjson.keys():
            pluginList = []
            for plugin in rjson["mods"]:
                pluginList.append(Plugin(name=plugin["name"], version=plugin["version"]))
            plugins = PluginsDict(pluginList)
        else:
            plugins = None

        self.lastValidResponse = JavaStatusResponse(online=rjson["online"], host=rjson["host"], port=rjson["port"], eula_blocked=rjson["eula_blocked"], retrieved_at=rjson["retrieved_at"], expires_at=rjson["expires_at"], version=version, players=players, motd=motd, icon=icon, mods=mods, software=software, plugins=plugins)

        return self.lastValidResponse 


