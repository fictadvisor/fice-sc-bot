from bot.messages.environment import environment

TOPIC_NOT_FOUND = environment.from_string("""
Гілка <b>{{ title }}</b> не знайдена.
""")

USER_NOT_FOUND = """
Користувача з таким тегом не знайдено
"""

ONLY_FOR_TOPIC = """
Ця функція тільки для гілок
"""
