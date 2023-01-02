"""first migrate

Revision ID: 53f7cdecf3b1
Revises: 
Create Date: 2023-01-01 10:36:49.889496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53f7cdecf3b1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('article_likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_article_likes'))
    )
    op.create_table('articles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=True),
    sa.Column('slug', sa.String(length=20), nullable=True),
    sa.Column('is_draft', sa.Boolean(), nullable=False),
    sa.Column('last_updated_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_articles'))
    )
    op.create_table('comment_likes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_comment_likes'))
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('comment', sa.Text(), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.Column('edited', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_comments'))
    )
    op.create_table('contact_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('date_sent', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_contact_messages'))
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=255), nullable=False),
    sa.Column('lastname', sa.String(length=255), nullable=False),
    sa.Column('username', sa.String(length=25), nullable=False),
    sa.Column('email', sa.Text(length=150), nullable=False),
    sa.Column('password_hash', sa.Text(length=255), nullable=False),
    sa.Column('about_author', sa.Text(), nullable=True),
    sa.Column('date_joined', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('email', name=op.f('uq_users_email')),
    sa.UniqueConstraint('password_hash', name=op.f('uq_users_password_hash')),
    sa.UniqueConstraint('username', name=op.f('uq_users_username'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('contact_messages')
    op.drop_table('comments')
    op.drop_table('comment_likes')
    op.drop_table('articles')
    op.drop_table('article_likes')
    # ### end Alembic commands ###