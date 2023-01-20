"""some migration

Revision ID: 8b3c33ad996f
Revises: a2e96f4096bf
Create Date: 2023-01-20 04:36:45.897152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b3c33ad996f'
down_revision = 'a2e96f4096bf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('facility', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('facility', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.drop_index('ix__facilities__id', table_name='facility')
    op.drop_index('ix__facilities__name', table_name='facility')
    op.drop_index('ix__facilities__x', table_name='facility')
    op.drop_index('ix__facilities__y', table_name='facility')
    op.create_index('ix__facility__id', 'facility', ['id'], unique=False, postgresql_using='hash')
    op.create_index('ix__facility__name', 'facility', ['name'], unique=False, postgresql_using='hash')
    op.create_index('ix__facility__x', 'facility', ['x'], unique=False, postgresql_using='btree')
    op.create_index('ix__facility__y', 'facility', ['y'], unique=False, postgresql_using='btree')
    op.add_column('users', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'created_at')
    op.drop_index('ix__facility__y', table_name='facility', postgresql_using='btree')
    op.drop_index('ix__facility__x', table_name='facility', postgresql_using='btree')
    op.drop_index('ix__facility__name', table_name='facility', postgresql_using='hash')
    op.drop_index('ix__facility__id', table_name='facility', postgresql_using='hash')
    op.create_index('ix__facilities__y', 'facility', ['y'], unique=False)
    op.create_index('ix__facilities__x', 'facility', ['x'], unique=False)
    op.create_index('ix__facilities__name', 'facility', ['name'], unique=False)
    op.create_index('ix__facilities__id', 'facility', ['id'], unique=False)
    op.drop_column('facility', 'updated_at')
    op.drop_column('facility', 'created_at')
    # ### end Alembic commands ###