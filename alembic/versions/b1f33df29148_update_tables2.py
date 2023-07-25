"""update tables2

Revision ID: b1f33df29148
Revises: 5db2dfbbfdaf
Create Date: 2023-07-24 01:14:20.696818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1f33df29148'
down_revision = '5db2dfbbfdaf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('dishes_submenu_id_title_description_price_key', 'dishes', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('dishes_submenu_id_title_description_price_key', 'dishes', ['submenu_id', 'title', 'description', 'price'])
    # ### end Alembic commands ###