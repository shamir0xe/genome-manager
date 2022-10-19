from src.helpers.string.case_convertor import CaseConvertor
from src.stages.stage import Stage
from src.stages.fastq_dump_stage import FastqDumpStage
from src.stages.fastqc_stage import FastqcStage
from src.stages.trim_galore_stage import TrimGaloreStage
from src.stages.bowtie_stage import BowtieStage
from src.stages.feature_count_stage import FeatureCountStage


class StageFactory:
    def __init__(self, stage: Stage) -> None:
        self.stage = stage
    
    def get_stage(self) -> Stage:
        return self.stage

    @staticmethod
    def generate(stage_name: str, *args, **kwargs) -> Stage:
        classname = f'{CaseConvertor.to_camel_case(stage_name, True)}Stage'
        # print(f'classname={classname}')
        return StageFactory(
            stage=eval(classname)(*args, **kwargs)
        ).get_stage()
