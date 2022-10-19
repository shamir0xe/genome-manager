from __future__ import annotations
from .stage import Stage


class TrimGaloreStage(Stage):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.stage_name = 'trim_galore'
    
    def check_dependencies(self) -> TrimGaloreStage:
        self.add_log('checking dependencies')
        # create out dir if not exists
        self.create_outdir()

        # check if input exists
        self.retrieve_infile('{}_1.fastq.gz')
        return self

    def run(self) -> TrimGaloreStage:
        if not self.status[0]:
            return self
        self.add_log('running the stage')
        length = self.get_config('length')
        cores = self.get_config('cores')
        self.exec(self.get_config('cmd0').format(
            self.outdir, 
            length, 
            cores,
            self.infile
        ))
        return self
