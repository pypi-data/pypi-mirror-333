# Copyright (C) 2020 Bloomberg LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  <http://www.apache.org/licenses/LICENSE-2.0>
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Add index on queued_timestamp in jobs table

Revision ID: 083f52d97bcb
Revises: 69ceb5938c06
Create Date: 2020-06-01 22:05:44.274091

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "083f52d97bcb"
down_revision = "69ceb5938c06"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(op.f("ix_jobs_queued_timestamp"), "jobs", ["queued_timestamp"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_jobs_queued_timestamp"), table_name="jobs")
