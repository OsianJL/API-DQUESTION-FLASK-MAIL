"""Cambiar tipo de columna id a BigInteger

Revision ID: c263aaaed2a7
Revises: fdb0d5c86ea8
Create Date: 2025-02-07 18:45:06.016954

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c263aaaed2a7'
down_revision = 'fdb0d5c86ea8'
branch_labels = None
depends_on = None

def upgrade():
    # Cambia la columna 'id' en la tabla 'users' a BigInteger.
    op.alter_column('users', 'id',
                    type_=sa.BigInteger(),
                    postgresql_using="id::bigint")

def downgrade():
    # Vuelve a cambiar la columna 'id' a Integer en caso de rollback.
    op.alter_column('users', 'id',
                    type_=sa.Integer(),
                    postgresql_using="id::integer")