
from typing import Dict, Any

Context = Dict[str, Any]


class Knight:

    NAME = "Unknown"
    HOUSE = 0
    ARCHETYPE = "Undefined"

    def __init__(self, executor=None):
        self.executor = executor

    def should_handle(self, ctx):
        return True

    def prepare(self, ctx):
        return ctx

    def execute(self, ctx):

        if self.executor:
            return self.executor.execute(ctx)

        return ctx

    def finalize(self, ctx):
        return ctx
