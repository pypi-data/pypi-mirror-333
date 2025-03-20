import logging
import os
from typing import cast

from bson import ObjectId
from mm_mongo import MongoCollection, MongoConnection
from mm_std import (
    Err,
    Result,
    Scheduler,
    init_logger,
)
from mm_telegram import send_telegram_message

from app.config import AppConfig, DConfigSettings, DValueSettings
from mm_base1.models import DConfig, DLog, DValue
from mm_base1.services.base import BaseServiceParams
from mm_base1.services.dconfig_service import DConfigService
from mm_base1.services.dvalue_service import DValueService
from mm_base1.services.system_service import SystemService


class BaseApp:
    def __init__(
        self,
        app_config: AppConfig,
        dconfig_settings: DConfigSettings,
        dvalue_settings: DValueSettings,
        debug_scheduler: bool = False,
    ) -> None:
        self.app_config = app_config
        self.logger = init_logger(
            "app",
            file_path=f"{app_config.data_dir}/app.log",
            level=logging.DEBUG if self.app_config.debug else logging.INFO,
        )
        conn = MongoConnection(app_config.database_url)
        self.mongo_client = conn.client
        self.database = conn.database
        self.dconfig_collection: MongoCollection[str, DConfig] = MongoCollection(self.database, DConfig)
        self.dvalue_collection: MongoCollection[str, DValue] = MongoCollection(self.database, DValue)
        self.dlog_collection: MongoCollection[ObjectId, DLog] = MongoCollection(self.database, DLog)
        self.dconfig: DConfigSettings = DConfigService.init_storage(self.dconfig_collection, dconfig_settings, self.dlog)  # type:ignore[assignment]
        self.dvalue: DValueSettings = DValueService.init_storage(self.dvalue_collection, dvalue_settings)  # type:ignore[assignment]
        self.scheduler = Scheduler(self.logger, debug=debug_scheduler)
        self.dconfig_service = DConfigService
        self.dvalue_service = DValueService
        self.system_service = SystemService(app_config, self.dconfig, self.dvalue, self.scheduler, self.database)

    def dlog(self, category: str, data: object = None) -> None:
        self.logger.debug("dlog %s %s", category, data)
        self.dlog_collection.insert_one(DLog(id=ObjectId(), category=category, data=data))

    def send_telegram_message(self, message: str) -> Result[list[int]]:
        token = self.dconfig.get("telegram_token")
        chat_id = self.dconfig.get("telegram_chat_id")
        if token and chat_id:
            return send_telegram_message(cast(str, token), cast(int, chat_id), message)
        return Err("token or chat_id is not set")

    def startup(self) -> None:
        self.logger.debug("app started")
        self.scheduler.start()
        if not self.app_config.debug:
            self.dlog("app_start")

    def shutdown(self) -> None:
        self.scheduler.stop()
        if not self.app_config.debug:
            self.dlog("app_stop")
        self.stop()
        self.mongo_client.close()
        self.logger.debug("app stopped")
        # noinspection PyUnresolvedReferences
        os._exit(0)

    def stop(self) -> None:
        pass

    @property
    def base_params(self) -> BaseServiceParams:
        return BaseServiceParams(
            app_config=self.app_config,
            logger=self.logger,
            dconfig=self.dconfig,
            dvalue=self.dvalue,
            dlog=self.dlog,
            send_telegram_message=self.send_telegram_message,
        )
