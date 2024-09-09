'''
We are taking the stuff from `status.py` and converting it into class files
'''
from .constants import MinecraftServer, BASE_URL, StatusResponse, VersionDict, PlayersDict, MOTDDict, ModsDict, PluginsDict, Player, Plugin, Mod
import requests
from dataclass import dataclass

@dataclass(frozen=True)
class BedrockStatusResponse(StatusResponse):
    version: BedrockVersion | None
    players: BedrockPlayers | None
    motd: MOTDDict | None
    gamemode: str | None
    server_id: str | None
    edition: str | str

class BedrockServer(MinecraftServer):
    def __init__(self, host: str, port: int = 19132):
        super().__init__()
        self.host = host
        self.port = port

        self.lastValidResponse: None | BedrockStatusResponse = None

    def get_status() -> JavaStatusResponse:
        host = self.host
        port = self.port
        res = requests.get(f"{BASE_URL}/status/bedrock/{host}:{port}")

        if res.status_code != 200:  # very few errors are handled, due to a lack of knowledge
            print("Seems something went wrong, here's some debug information!")
            print(f"BASE_URL: {BASE_URL},\nHOST: {host},\nPORT: {port}")

            if res.text.startswith("Not Found"):
                raise ValueError("Unable to find URL, most likely the `BASE_MCSTATUS_URL` environment variable is set to an incorrect value! (leave blank for default v2)")

            raise ValueError(f"You probably should report this on GITHUB!:\n{res.text}")

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

        self.lastValidResponse = BedrockStatusResponse(online=rjson["online"], host=rjson["host"], port=rjson["port"], eula_blocked=rjson["eula_blocked"], retrieved_at=rjson["retrieved_at"], expires_at=rjson["expires_at"], version=version, players=players, motd=motd, gamemode=gamemode, server_id=server_id, edition=rjson["edition"])
    
        return self.lastValidResponse 


