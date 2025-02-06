"""Initial migration

Revision ID: 91c635f5566d
Revises: 
Create Date: 2025-02-06 14:05:49.859543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91c635f5566d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.alter_column('subject',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('teacher',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('date',
               existing_type=sa.DATE(),
               nullable=False)
        batch_op.alter_column('roll_number',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('student_name',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(length=1),
               nullable=False)
        batch_op.create_foreign_key(None, 'student', ['roll_number'], ['roll_number'])

    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.alter_column('roll_number',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('roll_number',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(length=1),
               nullable=True)
        batch_op.alter_column('student_name',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('roll_number',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('date',
               existing_type=sa.DATE(),
               nullable=True)
        batch_op.alter_column('teacher',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('subject',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)

    # ### end Alembic commands ###
