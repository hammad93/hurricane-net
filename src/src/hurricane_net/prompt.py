import logging
from importlib.resources import files
from langchain_core.prompts import PromptTemplate
import sys

class Prompt:
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="hurricane_net %(asctime)s - %(levelname)s - %(name)s - %(message)s")
    def __init__(self):
        self.daily_report = self.prompt_daily_report()
    
    def load_prompt(self, filename, resource_path = 'hurricane_net.prompts'):
        '''
        References
        ----------
         - https://setuptools.pypa.io/en/latest/userguide/datafiles.html#accessing-data-files-at-runtime
        '''
        raw_prompt = files(resource_path).joinpath(filename).read_text()
        return PromptTemplate.from_template(raw_prompt)
    
    def prompt_daily_report(self, filename = 'daily_report.txt'):
        return self.load_prompt(filename)
prompt = Prompt()