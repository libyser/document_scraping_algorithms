

import json
from libser_engine import engine

def reverse(lst):
    return [ele for ele in reversed(lst)]


database_path = 'database/searh_query_database.json'


class get_db():

    def w_open(self): # opening a datbase file for writing

        self.fl_open = open(database_path, 'w')
        return self.fl_open

    def r_open(self): # opening a datbase file for reading

        try:
            self.fl_read = open(database_path, 'r')
            read_data = json.load(self.fl_read)
            self.fl_read.close()
        except: read_data = None

        return read_data

    def __init__(self):
        self.read_data = self.r_open()
    
    
    def load_data_in(self, input_data : dict):

        self.input_data = input_data
        
        try:
            self.f_1 = self.w_open()
            self.new_data = self.read_data
            self.new_data.update(self.input_data)

            json.dump(self.read_data, self.f_1)
            self.f_1.close()

            return True
                
        except: return False # if it is False the database will be lost
    
    def return_data(self):
        
        self.data = []
        for bookname in self.read_data:
            self.data.append(bookname)

        return self.data

class index():
    def __init__(self, word, filetype):
        self.word = word
        self.filetype = filetype
        self.results = engine.accumulate(self.word, self.filetype)


    def get_result(self):
        return self.results.all()


class Get_academics:
    
    def get_research_papers(self, query):
        papers = engine.Academics()

        return papers.researches(query)
