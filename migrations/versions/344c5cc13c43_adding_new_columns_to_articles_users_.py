"""adding new columns to articles, users, likes tables.

Revision ID: 344c5cc13c43
Revises: ca8853da6972
Create Date: 2023-01-02 17:30:27.678320

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '344c5cc13c43'
down_revision = 'ca8853da6972'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article_likes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_added', sa.DateTime(), nullable=True))

    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_deleted', sa.Boolean(), nullable=True))
        batch_op.drop_column('slug')

    with op.batch_alter_table('comment_likes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_added', sa.DateTime(), nullable=True))

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_pic', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('last_updated_by', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('last_updated_on', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('last_updated_on')
        batch_op.drop_column('last_updated_by')
        batch_op.drop_column('profile_pic')

    with op.batch_alter_table('comment_likes', schema=None) as batch_op:
        batch_op.drop_column('date_added')

    with op.batch_alter_table('articles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('slug', sa.VARCHAR(length=20), nullable=True))
        batch_op.drop_column('is_deleted')

    with op.batch_alter_table('article_likes', schema=None) as batch_op:
        batch_op.drop_column('date_added')

    # ### end Alembic commands ###
