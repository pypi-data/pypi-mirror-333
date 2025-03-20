from dataclasses import dataclass
from webcommander.sdlize.wc_base_dto import *


@dataclass(kw_only=True)
class RequestTokenDTO(WCBaseDTO):
    webCommanderUrl: str
    authString: str
    grantType: str
    redirectUri: str
    clientId: str
    clientSecret: str


@dataclass(kw_only=True)
class RefreshTokenDTO(WCBaseDTO):
    grantType: str = "refresh_token"
    refreshToken: str
    clientId: str
    clientSecret: str
    redirectUri: str


@dataclass(kw_only=True)
class TokenResponseDTO(WCBaseDTO):
    accessToken: str = None
    refreshToken: str = None
    expiresIn: int = None
