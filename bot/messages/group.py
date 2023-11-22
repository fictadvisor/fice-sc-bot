from bot.messages.environment import environment

ALL_MEMBERS = environment.from_string("""
Всі учасники  - {{ users|length }}:
<code>{% for user in users %}
{{ user.username }}
{% endfor %}</code>
""")

DELETED_MEMBERS = environment.from_string("""
Видалені учасники:
<code>{% for user in users %}
{{ user.username }}
{% endfor %}</code>
""")

GROUPS_MEMBERS = environment.from_string("""
{% for group in groups %}
<b>{{ group.title }} - {{ group.users|length }}</b>
<code>{% for user in group.users %}
{{ user.username }}
{% endfor %}</code>
{% endfor %}
""")

GROUP_MEMBERS = environment.from_string("""
Учасники чату - {{ group.users|length }}:
<code>{% for user in group.users %}
{{ user.username }}
{% endfor %}</code>
""")

SELECT_TYPE = """
Оберіть тип:
"""

SELECT_GROUP = """
Оберіть групу:
"""

SELECT_TOPIC = """
Оберіть гілку
"""

FORWARD_MESSAGE = environment.from_string("""
{% if status %}
Статус: {{ status.value }}
{% endif %}
{% if responsible %}
Відповідальний: {{ responsible.username }}
{% endif %}

{{ html_text|default('', true) }}

<b>{{ title }}</b>, <code>{{ username }}</code>
""")

SENT = environment.from_string("""
Надіслано у <b>{{ title }}</b>

{% if status %}
Статус: {{ status.value }}
{% endif %}
""")

SET_RESPONSIBLE = """
Відповідального встановлено
"""

HELP = """
/all - Усі учасники
/groups - Учасники груп
/users - Учасники чату
/send - Надіслати повідомлення
/responsible @{username} - Встановити відповідального
/delete @{username} - Видалити юзера
/help - Допомога
"""

RANDOM_COFFEE = environment.from_string("""
Пари на Random Coffee:
{% for pair in pairs %}
{{ pair.first.username }} - {{ pair.second.username }}
{% endfor %}
""")