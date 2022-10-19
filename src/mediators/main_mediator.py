from __future__ import annotations
from libs.python_library.config.config import Config
from libs.python_library.file.file import File
from libs.python_library.argument.argument_parser import ArgumentParser
from libs.python_library.path.path import Path
from src.helpers.log.runtime_log import RuntimeLog
from src.factories.stage_factory import StageFactory


class MainMediator:
    def __init__(self) -> None:
        self.log = RuntimeLog(*Config.read('main.log_path'))
    
    def apply_local_config(self) -> MainMediator:
        config = Config.read('main')
        for key, value in config.items():
            self.log.add_log(f'_{key} = {value}', 'local_config')
            setattr(self, f'_{key}', value)
        return self
    
    def apply_arguments_config(self) -> MainMediator:
        modifiables = Config.read('main').keys()
        for option in ArgumentParser.get_options():
            if option in modifiables:
                self.log.add_log(f'_{option} = {ArgumentParser.get_value(option)[0]}', 'arguments')
                setattr(self, f'_{option}', ArgumentParser.get_value(option)[0])
        return self
    
    def load_inputs(self) -> MainMediator:
        self.log.add_log('loading input')
        self.inputs = File.read_json(
            Path.from_root(*self._input_file_path)
        )
        return self
    
    def run_pipeline(self) -> MainMediator:
        self.log.add_log('run pipeline')
        pipeline = self._pipelines[str(self._pipeline)]
        for entry in self.inputs:
            self.log.add_log(f'enter process for {entry}', 'pipline')
            for stage_name in pipeline:
                StageFactory.generate(
                    stage_name=stage_name,
                    entry=entry,
                    log=self.log
                ) \
                    .check_dependencies() \
                    .run() \
                    .closure()
                print(stage_name)
        return self
    
    def closure(self) -> MainMediator:
        self.log.add_log(f'ended in {0:0.2f} seconds')
        return self
