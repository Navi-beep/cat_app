"""empty message

Revision ID: 9e3dfa24a8c5
Revises: 392a3a54a938
Create Date: 2022-09-10 20:14:30.611929

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e3dfa24a8c5'
down_revision = '392a3a54a938'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('add__cat',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fav_cat_breed', sa.String(length=50), nullable=False),
    sa.Column('fav_int_cat', sa.String(length=75), nullable=False),
    sa.Column('fav_cat_fact', sa.String(length=300), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('add__cat')
    # ### end Alembic commands ###
