# the file for the actual status code, this is basically just the python version of the node-mcstatus library.
from __future__ import annotations
from .constants import BASE_URL, StatusResponse, VersionDict, PlayersDict, MOTDDict, ModsDict, PluginsDict, BedrockVersion, BedrockPlayers, Player, Plugin, Mod
import requests
from dataclasses import dataclass


@dataclass(frozen=True)
class JavaStatusResponse(StatusResponse):
    version: VersionDict | None
    players: PlayersDict | None
    motd: MOTDDict | None
    icon: str | None
    mods: ModsDict | None
    software: str | None
    plugins: PluginsDict | None


@dataclass(frozen=True)
class BedrockStatusResponse(StatusResponse):
    version: BedrockVersion | None
    players: BedrockPlayers | None
    motd: MOTDDict | None
    gamemode: str | None
    server_id: str | None
    edition: str | str


def statusJava(host: str, port: int = 25565, query: bool = True) -> JavaStatusResponse:
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

    return JavaStatusResponse(online=rjson["online"], host=rjson["host"], port=rjson["port"], eula_blocked=rjson["eula_blocked"], retrieved_at=rjson["retrieved_at"], expires_at=rjson["expires_at"], version=version, players=players, motd=motd, icon=icon, mods=mods, software=software, plugins=plugins)


def statusBedrock(host: str, port: int = 19132) -> BedrockStatusResponse:
    res = requests.get(f"{BASE_URL}/status/bedrock/{host}:{port}")

    if res.status_code != 200:
        raise ValueError(res.text)  # It's very vague about errors because the node-mcstatus library does the exact same thing.

    rjson = res.json()

    if "version" in rjson.keys():
        version = BedrockVersion(name=rjson["version"]["name"], protocol=rjson["version"]["protocol"])
    else:
        version = None

    if "players" in rjson.keys():
        players = BedrockPlayers(online=rjson["players"]["online"], max=rjson["players"]["max"])
    else:
        players = None

    if "motd" in rjson.keys():
        motd = MOTDDict(raw=rjson["motd"]["raw"], clean=rjson["motd"]["clean"], html=rjson["motd"]["html"])
    else:
        motd = None

    if "gamemode" in rjson.keys():
        gamemode = rjson["gamemode"]
    else:
        gamemode = None

    if "server_id" in rjson.keys():
        server_id = rjson["server_id"]
    else:
        server_id = None
    return BedrockStatusResponse(online=rjson["online"], host=rjson["host"], port=rjson["port"], eula_blocked=rjson["eula_blocked"], retrieved_at=rjson["retrieved_at"], expires_at=rjson["expires_at"], version=version, players=players, motd=motd, gamemode=gamemode, server_id=server_id, edition=rjson["edition"])
