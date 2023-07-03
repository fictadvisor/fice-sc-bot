from bot.messages.environment import environment

ALL_MEMBERS = environment.from_string("""
Всі учасники:
<code>{% for user in users %}
{{ user.username }}
{% endfor %}</code>
""")

GROUPS_MEMBERS = environment.from_string("""
{% for group in groups %}
<b>{{ group.title }}</b>
<code>{% for user in group.users %}
{{ user.username }}
{% endfor %}</code>
{% endfor %}
""")

GROUP_MEMBERS = environment.from_string("""
Учасники чату:
<code>{% for user in group.users %}
{{ user.username }}
{% endfor %}</code>
""")

SELECT_GROUP = """
Оберіть групу:
"""

FORWARD_MESSAGE = environment.from_string("""
Переслано з <b>{{ title }}</b> від <code>{{ username }}</code>:

{{ text }}
""")

SENT = environment.from_string("""
Надіслано у <b>{{ title }}</b>
""")
