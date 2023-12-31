"""update chat message column

Revision ID: c52f16e5449d
Revises: ac14e5491186
Create Date: 2023-11-05 17:05:29.027107

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c52f16e5449d'
down_revision = 'ac14e5491186'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('chat_message', 'role',
               existing_type=postgresql.ENUM('system', 'user', 'assistant', name='roletype'),
               nullable=False)
    op.alter_column('chat_message', 'content',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('chat_message', 'chat_room_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('chat_room', 'title',
               existing_type=sa.VARCHAR(length=40),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('chat_room', 'title',
               existing_type=sa.VARCHAR(length=40),
               nullable=True)
    op.alter_column('chat_message', 'chat_room_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('chat_message', 'content',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('chat_message', 'role',
               existing_type=postgresql.ENUM('system', 'user', 'assistant', name='roletype'),
               nullable=True)
    # ### end Alembic commands ###
