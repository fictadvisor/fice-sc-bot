from bot.messages.environment import environment

ALL_MEMBERS = environment.from_string("""
{% for group in groups %}
<b>{{ group.title }}</b>
{% for user in group.users %}
{{ user.username }}
{% endfor %}

{% endfor %}
""")

GROUP_MEMBERS = environment.from_string("""
{% for user in group.users %}
{{ user.username }}
{% endfor %}
""")

SELECT_GROUP = """
Оберіть групу:
"""

FORWARD_MESSAGE = environment.from_string("""
Переслано з {{ title }} від {{ username }}:

{{ text }}
""")

SENT = """
Надіслано
"""
