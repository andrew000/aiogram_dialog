from logging import getLogger

from aiogram_dialog.api.entities import (
    DialogAction,
    DialogStartEvent,
    DialogSwitchEvent,
    DialogUpdateEvent,
)
from .manager import ManagerImpl

logger = getLogger(__name__)


async def handle_update(event: DialogUpdateEvent, dialog_manager: ManagerImpl):
    if isinstance(event, DialogStartEvent):
        await dialog_manager.start(
            state=event.new_state,
            data=event.data,
            mode=event.mode,
            show_mode=event.show_mode,
        )
    elif isinstance(event, DialogSwitchEvent):
        await dialog_manager.switch_to(state=event.new_state)
        await dialog_manager.show()
    elif event.action is DialogAction.UPDATE:
        if not dialog_manager.current_context():
            logger.warning("No context found")
            return
        if event.data:
            for k, v in event.data.items():
                dialog_manager.current_context().dialog_data[k] = v
        await dialog_manager.show()
    elif event.action is DialogAction.DONE:
        await dialog_manager.done(result=event.data)
