"""Added media group

Revision ID: 1d6ae52b4aeb
Revises: 61466764c5c8
Create Date: 2023-07-09 19:46:06.813259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d6ae52b4aeb'
down_revision = '61466764c5c8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    mediatypes = sa.Enum('PHOTO', 'VIDEO', 'AUDIO', 'DOCUMENT', name='mediatypes')
    mediatypes.create(op.get_bind(), checkfirst=True)

    op.add_column('messages', sa.Column('media_group_id', sa.String(), nullable=True))
    op.add_column('messages', sa.Column('file_id', sa.String(), nullable=True))
    op.add_column('messages', sa.Column('media_type', sa.Enum('PHOTO', 'VIDEO', 'AUDIO', 'DOCUMENT', name='mediatypes'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('messages', 'media_type')
    op.drop_column('messages', 'file_id')
    op.drop_column('messages', 'media_group_id')

    mediatypes = sa.Enum('PHOTO', 'VIDEO', 'AUDIO', 'DOCUMENT', name='mediatypes')
    mediatypes.drop(op.get_bind(), checkfirst=True)
    # ### end Alembic commands ###
