from core.compiler.interfaces import CompilerError

class CompilerPipeline:
    def __init__(self, stages): self.stages=stages
    def compile(self, ctx):
        for s in self.stages:
            try: ctx=s.run(ctx)
            except Exception as e: raise CompilerError(str(e))
        return ctx
