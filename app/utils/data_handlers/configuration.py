from typing import List, Optional
from sqlalchemy.orm import Session

from app.models import User, Configuration
from app.schemas import ConfigurationCreate
from app.utils.data_handlers.base import BaseDataHandler


class ConfigurationDataHandler(BaseDataHandler):
    """
    Class with useful methods regarding the configuration model
    """

    def __init__(self, db: Session, user: User = None) -> None:
        super().__init__(db)
        self.user: User = user

    @property
    def get_all_configs(self) -> List[Configuration]:
        return self.db.query(Configuration).all()

    @property
    def get_active_config(self) -> Optional[Configuration]:
        return (
            self.db.query(Configuration).filter(Configuration.is_active == True).first()
        )

    def create_configuration(self, configuration: ConfigurationCreate) -> Configuration:
        config = Configuration(
            lenght=configuration.lenght,
            numbers=configuration.numbers,
            lowercase_chars=configuration.lowercase_chars,
            uppercase_chars=configuration.uppercase_chars,
            special_symbols=configuration.special_symbols,
            is_active=configuration.is_active,
            user_id=self.user.id,
        )
        self.db.add(config)
        self.db.commit()
        self.db.refresh(config)

        # update the remaining configs with is_active = False
        if config.is_active is True:
            self._update_remaining_is_active_configs(config.id)
        return config

    def get_config_by_id(self, id: int) -> Optional[Configuration]:
        return self.db.query(Configuration).filter(Configuration.id == id).first()

    def delete_configuration_by_id(self, configuration_id: int) -> bool:
        if self.get_config_by_id(configuration_id):
            self.db.query(Configuration).filter(
                Configuration.id == configuration_id
            ).delete()
            self.db.commit()
            return True
        return False

    def update_configuration_by_id(self, configuration_id: int, payload: dict) -> bool:
        if config := self.get_config_by_id(configuration_id):
            self.db.query(Configuration).filter(
                Configuration.id == configuration_id
            ).update(payload)
            self.db.commit()
            self.db.refresh(config)

            # update the remaining configs with is_active = False
            if payload.get("is_active") is True:
                self._update_remaining_is_active_configs(config.id)
            return config
        return False

    def _update_remaining_is_active_configs(self, configuration_id: int) -> None:
        self.db.query(Configuration).filter(
            Configuration.id != configuration_id, Configuration.is_active == True
        ).update({"is_active": False})
        self.db.commit()
