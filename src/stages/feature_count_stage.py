from __future__ import annotations
from .stage import Stage


class FeatureCountStage(Stage):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.stage_name = 'feature_count'
    
    def check_dependencies(self) -> FeatureCountStage:
        self.add_log('checking dependencies')
        # create out dir and file if not exists
        self.create_outdir('{}.count')

        # check if input exists
        self.retrieve_infile('{}.sam')
        return self

    def run(self) -> FeatureCountStage:
        if not self.status[0]:
            return self
        self.add_log('running the stage')
        self.exec(self.get_config('cmd0').format(
            self.get_config('strandness'), 
            self.get_config('attribute_type'),
            self.get_config('cores'),
            self.get_config('feature_type'),
            self.get_config('annotation_file'),
            self.outfile,
            self.infile
        ))
        return self

