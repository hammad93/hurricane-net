import logging
from langchain_core.prompts import PromptTemplate

class Prompt
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="hurricane_net %(asctime)s - %(levelname)s - %(name)s - %(message)s")
    def __init__(self):
        self.daily_report = self.prompt_daily_report()
    
    def load_prompt(self, path):
        with open(path) as f:
            return f.read()
    
    def prompt_daily_report(self, path = 'prompts/daily_report.txt'):
        return self.load_prompt(path)
prompt = Prompt()