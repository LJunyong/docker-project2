"""Initial migration

Revision ID: 869632429f1b
Revises: 
Create Date: 2024-11-17 19:40:27.459101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '869632429f1b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('survey_completed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('survey_response',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('responses', sa.PickleType(), nullable=False),
    sa.Column('score', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('survey_response')
    op.drop_table('user')
    # ### end Alembic commands ###
