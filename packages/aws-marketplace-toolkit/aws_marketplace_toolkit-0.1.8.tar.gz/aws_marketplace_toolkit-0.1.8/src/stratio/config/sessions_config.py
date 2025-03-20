# src/stratio/api/config/sessions_config.py
from typing import Optional

from pydantic import BaseModel

from stratio.api.session import ApiSession, CredentialsApiSession, ProfileApiSession


class ProfileSessionConfig(BaseModel):
    name: str

    def to_profile_api_session(self) -> ProfileApiSession:
        return ProfileApiSession(profile_name=self.name)


class CredentialsSessionConfig(BaseModel):
    key_id: str
    secret_key: str
    account_id: str
    region: Optional[str] = None

    def to_credentials_api_session(self) -> CredentialsApiSession:
        return CredentialsApiSession(
            key_id=self.key_id,
            secret_key=self.secret_key,
            account_id=self.account_id,
            region_name=self.region,
        )


class SessionConfig(BaseModel):
    profile: Optional[ProfileSessionConfig] = None
    credentials: Optional[CredentialsSessionConfig] = None

    def to_api_session(self) -> Optional[ApiSession]:
        if self.profile:
            return self.profile.to_profile_api_session()
        elif self.credentials:
            return self.credentials.to_credentials_api_session()
        return None


class SessionsConfig(BaseModel):
    root: Optional[SessionConfig] = None
    automations: Optional[SessionConfig] = None
    seller: Optional[SessionConfig] = None
    shared: Optional[SessionConfig] = None
