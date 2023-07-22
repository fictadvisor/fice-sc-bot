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

{{ html_text|default('', true) }}

<b>{{ title }}</b>, <code>{{ username }}</code>
""")

SENT = environment.from_string("""
Надіслано у <b>{{ title }}</b>

{% if status %}
Статус: {{ status.value }}
{% endif %}
""")
