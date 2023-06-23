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
