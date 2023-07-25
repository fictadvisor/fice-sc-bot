"""Added responsible

Revision ID: 39270bcf2897
Revises: d62d1504838a
Create Date: 2023-07-24 22:45:46.624350

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39270bcf2897'
down_revision = 'd62d1504838a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('topics', sa.Column('responsible_id', sa.BigInteger(), nullable=True))
    op.create_foreign_key(op.f('fk_topics_responsible_id_users'), 'topics', 'users', ['responsible_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_topics_responsible_id_users'), 'topics', type_='foreignkey')
    op.drop_column('topics', 'responsible_id')
    # ### end Alembic commands ###
