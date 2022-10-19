from __future__ import annotations
from abc import ABC, abstractmethod
from libs.python_library.config.config import Config
from libs.python_library.data.data_transfer_object import DataTransferObject
from src.helpers.log.runtime_log import RuntimeLog
from libs.python_library.path.path import Path
from src.helpers.file.file_helper import FileHelper
from src.helpers.terminal.single_process import SingleProcess


class Stage(ABC):
    def __init__(self, entry: dict, log: RuntimeLog=None) -> None:
        self.entry = DataTransferObject.from_dict(entry)
        self.stage_name = 'stage'
        self.status = (True, 'Success')
        if not log is None:
            self.log = log
        self.timer = 0
    
    @abstractmethod
    def check_dependencies(self) -> Stage:
        pass
    
    @abstractmethod
    def run(self) -> Stage:
        pass

    def add_log(self, log: str) -> Stage:
        if not self.log is None:
            self.log.add_log(log, self.stage_name)
        return self

    def closure(self) -> Stage:
        self.add_log(f'{self.stage_name} completed!')
        return self
    
    def terminate(self, message: str) -> Stage:
        self.add_log(message)
        self.status = (False, message)
        return self
    
    def get_config(self, selector: str=None) -> dict:
        if selector is None:
            return Config.read(f'stages.{self.stage_name}')
        return Config.read(f'stages.{self.stage_name}.{selector}')
    
    def create_outdir(self, outfile: str=None) -> Stage:
        self.outdir = self.get_config('out_directory')
        if self.outdir is None:
            return self.terminate('invalid path')
        self.outdir = Path.from_root(*self.outdir)
        if not FileHelper.dir_exists(self.outdir):
            self.add_log(f'creating {self.outdir}')
            FileHelper.make_directories(self.outdir)
        
        if not outfile is None:
            self.outfile = Path.from_root(
                *self.get_config('out_directory'), 
                outfile.format(self.entry.name)
            )
        return self
    
    def retrieve_infile(self, base: str) -> Stage:
        self.infile = Path.from_root(
            *self.get_config('in_directory'), 
            base.format(self.entry.name)
        )
        if not FileHelper.file_exists(self.infile):
            return self.terminate('invalid input file')
        return self
    
    def exec(self, command: str) -> Stage:
        out, err = SingleProcess(
            command,
            log=self.log, 
        ).run().communicate()
        print(f'out: {out}')
        print(f'err: {err}')
        return self
