from enum import Enum


class Status(str, Enum):
    COMPLETED = "🟢 Виконано"
    PROCESSING = "🟡 Виконується"
    NOT_STARTED = "⚪️ Не розпочато"
    DECLINED = "🔴 Відхилено"
