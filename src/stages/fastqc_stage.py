from __future__ import annotations
from .stage import Stage


class FastqcStage(Stage):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.stage_name = 'fastqc'
    
    def check_dependencies(self) -> FastqcStage:
        self.add_log('checking dependencies')
        # create out dir if not exists
        self.create_outdir()

        # check if input exists
        self.retrieve_infile('{}_1.fastq.gz')
        return self

    def run(self) -> FastqcStage:
        if not self.status[0]:
            return self
        self.add_log('running the stage')
        self.exec(self.get_config('cmd0').format(self.outdir, self.infile))
        return self
