from webcommander.http.wc_rest_processor import WCRestProcessor
from webcommander.webcommander.common.dto.settings_dto import SettingsListDTO
from webcommander.webcommander.settings.settings_api_url import SettingsApiUrl


class Settings(WCRestProcessor):

    def info(self) -> SettingsListDTO:
        response = self.get(url=SettingsApiUrl.SETTINGS, response_obj=SettingsListDTO())
        return response
