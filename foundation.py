
import json
import engine # importing form engine.py

# class for extracting the documents 
class index():
    def __init__(self, word:str, filetype:str):
        self.word = word
        self.filetype = filetype # describe a filetype such as 'pdf'
        # calling extracting engine
        self.results = engine.accumulate(self.word, self.filetype)

    def get_result(self):
        return self.results.all()


# class for extracting the acadimics papers
class Get_academics:
    
    def get_research_papers(self, query:str):
        papers = engine.Academics()
        return papers.researches(query)
