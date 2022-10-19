from __future__ import annotations
from .stage import Stage


class FastqDumpStage(Stage):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.stage_name = 'fastq_dump'
    
    def check_dependencies(self) -> FastqDumpStage:
        self.add_log('checking dependencies')
        # create out dir if not exists
        self.create_outdir()
        return self

    def run(self) -> FastqDumpStage:
        if not self.status[0]:
            return self
        self.add_log('running the stage')
        self.exec(self.get_config('cmd0').format(self.outdir, self.entry.name))
        return self
