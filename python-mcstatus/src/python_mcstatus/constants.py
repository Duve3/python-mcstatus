# a file to define constants in the project
from dataclasses import dataclass
BASE_URL: str = 'https://api.mcstatus.io/v2'


@dataclass(frozen=True)
class BedrockVersion:
    name: str
    protocol: int


@dataclass(frozen=True)
class BedrockPlayers:
    online: int
    max: int


@dataclass(frozen=True)
class StatusResponse:
    online: bool
    host: str
    port: int
    eula_blocked: bool
    retrieved_at: int
    expires_at: int


@dataclass(frozen=True)
class VersionDict:
    name_raw: str
    name_clean: str
    name_html: str
    protocol: int


@dataclass(frozen=True)
class Player:
    uuid: str
    name_raw: str
    name_clean: str
    name_html: str

    def __getitem__(self, name):
        return vars(self)[name]


@dataclass(frozen=True)
class PlayersDict:
    online: int
    max: int
    list: list[Player]


@dataclass(frozen=True)
class MOTDDict:
    raw: str
    clean: str
    html: str


@dataclass(frozen=True)
class Mod:
    name: str
    version: str


@dataclass(frozen=True)
class ModsDict:
    list: list[Mod]


@dataclass(frozen=True)
class Plugin:
    name: str
    version: str


@dataclass(frozen=True)
class PluginsDict:
    list: list[Plugin]
