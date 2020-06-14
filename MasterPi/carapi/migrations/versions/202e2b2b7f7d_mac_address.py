"""mac address

Revision ID: 202e2b2b7f7d
Revises: 
Create Date: 2020-06-10 19:09:53.878914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '202e2b2b7f7d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('car',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('make', sa.String(length=64), nullable=True),
    sa.Column('body_type', sa.Integer(), nullable=True),
    sa.Column('colour', sa.Integer(), nullable=True),
    sa.Column('seats', sa.Integer(), nullable=True),
    sa.Column('location', sa.String(length=64), nullable=True),
    sa.Column('rate', sa.Float(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_car_name'), 'car', ['name'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=128), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('face_token', sa.String(length=128), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('mac_address', sa.String(length=128), nullable=True),
    sa.Column('role', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_face_token'), 'user', ['face_token'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('booking',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timebooked', sa.DateTime(), nullable=True),
    sa.Column('timestart', sa.DateTime(), nullable=True),
    sa.Column('dration', sa.Integer(), nullable=True),
    sa.Column('timeend', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('car_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['car_id'], ['car.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('booking')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_face_token'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_car_name'), table_name='car')
    op.drop_table('car')
    # ### end Alembic commands ###