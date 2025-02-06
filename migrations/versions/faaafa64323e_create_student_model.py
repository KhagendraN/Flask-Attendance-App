"""Create Student model

Revision ID: faaafa64323e
Revises: 
Create Date: 2025-02-06 14:24:29.388741

"""
from alembic import op
import sqlalchemy as sa

down_revision = None
revision = '91c635f5566d'

def upgrade():
    # Ensure there are no NULL values in the 'status' column before altering it
    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.execute("UPDATE attendance SET status = 'A' WHERE status IS NULL")
        
        # Now we can safely alter the column
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
        batch_op.create_foreign_key('fk_attendance_student', 'student', ['roll_number'], ['roll_number'])

    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.alter_column('roll_number',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)

def downgrade():
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('roll_number',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.drop_constraint('fk_attendance_student', type_='foreignkey')
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
