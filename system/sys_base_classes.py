from pydantic import BaseModel


class EmailCfg(BaseModel):
    user_name: str
    password: str
    server: str
    port: int

class LogCfg(BaseModel):
    level: str
    save_path: str

