from pydantic import BaseModel


class EmailLogCfg(BaseModel):
    user_name: str
    password: str
    server: str
    port: int

