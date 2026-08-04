class ValidationExecutor:

    def execute(self, ctx):
        return ctx


class KernelExecutor:

    def execute(self, ctx):
        ctx["core_status"] = "STABLE_EXECUTION"
        return ctx
