"""
Copyright (c) 2019 Michael McCartney, Kevin McLoughlin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from hivemind.data.abstract.table import _TableLayout
from hivemind.data.abstract.field import _Field
from hivemind.data.tables import NodeRegister

class TaskRegister(_TableLayout):
    """
    Task table with the required fields to help the user work
    with their task nodes.
    """
    node = _Field.ForeignKeyField(NodeRegister)

    # -- The name of this task
    name = _Field.TextField()

    # -- The current state of the task
    state = _Field.TextField(default='pending')

    # -- The endpoint that we use to construct
    #    requests for the task
    endpoint = _Field.TextField()

    # -- The type of this task
    type = _Field.TextField()


    @classmethod
    def unqiue_constraints(cls):
        return (('node', 'name'),)


class TaskInfo(_TableLayout):
    """
    Task info based on a single run of a given job...
    """
    task = _Field.ForeignKeyField(TaskRegister)

    info = _Field.JSONField(null=True)