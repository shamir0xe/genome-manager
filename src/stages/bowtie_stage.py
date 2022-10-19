from __future__ import annotations
from .stage import Stage


class BowtieStage(Stage):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.stage_name = 'bowtie'
    
    def check_dependencies(self) -> BowtieStage:
        self.add_log('checking dependencies')
        # create out dir and file if not exists
        self.create_outdir('{}.sam')

        # check if input exists
        self.retrieve_infile('{}_1_trimmed.fq.gz')
        return self

    def run(self) -> BowtieStage:
        if not self.status[0]:
            return self
        self.add_log('running the stage')
        self.exec(self.get_config('cmd0').format(
            self.get_config('bowtie_index'), 
            self.get_config('cores'),
            self.infile,
            self.outfile
        ))
        return self
