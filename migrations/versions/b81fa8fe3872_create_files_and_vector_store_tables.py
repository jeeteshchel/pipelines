"""create files and vector store tables

Revision ID: b81fa8fe3872
Revises: 
Create Date: 2024-07-09 11:51:00.864047

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import apps

# revision identifiers, used by Alembic.
revision: str = 'b81fa8fe3872'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('object', sa.String(), nullable=False),
    sa.Column('bytes', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('filename', sa.Text(), nullable=False),
    sa.Column('purpose', sa.Text(), nullable=False),
    sa.Column('status', sa.Text(), nullable=False),
    sa.Column('status_details', sa.Text(), nullable=True),
    sa.Column('meta', apps.openai.internal.db.JSONField(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vector_store',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('last_active_at', sa.BigInteger(), nullable=False),
    sa.Column('metadata', apps.openai.internal.db.JSONField(), nullable=True),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('object', sa.Text(), nullable=False),
    sa.Column('status', sa.Text(), nullable=False),
    sa.Column('usage_bytes', sa.BigInteger(), nullable=False),
    sa.Column('expires_at', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('file_content',
    sa.Column('content', sa.LargeBinary(), nullable=False),
    sa.Column('file_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['file_id'], ['file.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('file_id')
    )
    op.create_table('vector_store_expires_after',
    sa.Column('days', sa.BigInteger(), nullable=True),
    sa.Column('anchor', sa.Text(), nullable=True),
    sa.Column('vector_store_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['vector_store_id'], ['vector_store.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('vector_store_id')
    )
    op.create_table('vector_store_file',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('object', sa.Text(), nullable=False),
    sa.Column('usage_bytes', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.BigInteger(), nullable=False),
    sa.Column('vector_store_id', sa.String(), nullable=False),
    sa.Column('status', sa.Text(), nullable=False),
    sa.Column('file_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['file_id'], ['file.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['vector_store_id'], ['vector_store.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vector_store_file_counts',
    sa.Column('in_progress', sa.BigInteger(), nullable=False),
    sa.Column('completed', sa.BigInteger(), nullable=False),
    sa.Column('failed', sa.BigInteger(), nullable=False),
    sa.Column('cancelled', sa.BigInteger(), nullable=False),
    sa.Column('total', sa.BigInteger(), nullable=False),
    sa.Column('vector_store_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['vector_store_id'], ['vector_store.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('vector_store_id')
    )
    op.create_table('chunking_strategy',
    sa.Column('type', sa.Text(), nullable=True),
    sa.Column('vector_store_file_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['vector_store_file_id'], ['vector_store_file.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('vector_store_file_id')
    )
    op.create_table('last_error',
    sa.Column('code', sa.Text(), nullable=True),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('vector_store_file_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['vector_store_file_id'], ['vector_store_file.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('vector_store_file_id')
    )
    op.create_table('chunking_strategy_static',
    sa.Column('chunk_overlap_tokens', sa.BigInteger(), nullable=True),
    sa.Column('max_chunk_size_tokens', sa.BigInteger(), nullable=True),
    sa.Column('chunking_strategy_id', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['chunking_strategy_id'], ['chunking_strategy.vector_store_file_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('chunking_strategy_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chunking_strategy_static')
    op.drop_table('last_error')
    op.drop_table('chunking_strategy')
    op.drop_table('vector_store_file_counts')
    op.drop_table('vector_store_file')
    op.drop_table('vector_store_expires_after')
    op.drop_table('file_content')
    op.drop_table('vector_store')
    op.drop_table('file')
    # ### end Alembic commands ###
