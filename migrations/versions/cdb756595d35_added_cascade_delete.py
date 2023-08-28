"""Added cascade delete

Revision ID: cdb756595d35
Revises: fcf386700c7c
Create Date: 2023-07-25 22:44:06.008304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cdb756595d35'
down_revision = 'fcf386700c7c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_topics_responsible_id_users', 'topics', type_='foreignkey')
    op.drop_constraint('fk_topics_group_id_groups', 'topics', type_='foreignkey')
    op.create_foreign_key(op.f('fk_topics_responsible_id_users'), 'topics', 'users', ['responsible_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(op.f('fk_topics_group_id_groups'), 'topics', 'groups', ['group_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_topics_group_id_groups'), 'topics', type_='foreignkey')
    op.drop_constraint(op.f('fk_topics_responsible_id_users'), 'topics', type_='foreignkey')
    op.create_foreign_key('fk_topics_group_id_groups', 'topics', 'groups', ['group_id'], ['id'])
    op.create_foreign_key('fk_topics_responsible_id_users', 'topics', 'users', ['responsible_id'], ['id'])
    # ### end Alembic commands ###