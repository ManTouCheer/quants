from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict
from typing import Type, Tuple, Any, Dict
import yaml

from base_class.sys_base_classes import EmailCfg, LogCfg


class BaseCfg(PydanticBaseSettingsSource):
    """
    获取配置文件中的数据
    :return:
    """

    def __init__(self, settings_cls: type[BaseSettings]):
        super().__init__(settings_cls)
        self.cfg_data: dict = {}
        self.init_data()

    def init_data(self):
        encoding = self.config.get('env_file_encoding')
        with open('config.yaml', 'r', encoding=encoding) as file:
            self.cfg_data = yaml.safe_load(file)

    def get_field_value(
            self, field: FieldInfo, field_name: str
    ) -> Tuple[Any, str, bool]:

        field_value = self.cfg_data.get(field_name)
        return field.annotation(**field_value), field_name, False

    def prepare_field_value(self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool) -> Any:
        return value

    def __call__(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}

        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(
                field, field_name
            )
            field_value = self.prepare_field_value(
                field_name, field, field_value, value_is_complex
            )
            if field_value is not None:
                d[field_key] = field_value

        return d


class Settings(BaseSettings):
    # numbers: List[int]
    model_config = SettingsConfigDict(env_file_encoding='utf-8')

    Email: EmailCfg
    Log: LogCfg

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: Type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            BaseCfg(settings_cls),
            env_settings,
            file_secret_settings,
        )


setting = Settings()
email_cfg = setting.Email
log_cfg = setting.Log
