import os
import csv

class CSVDB:
    def __init__(self):
        self.filename = 'db.csv'
        if os.path.exists(self.filename):
            self.data = []
            with open(self.filename, 'r') as fp:
                for line in csv.reader(fp):
                    self.data.append(line)
        else:
            self.data = []
    
    def insert(self, user, name):
        record = [user, name]
        if user not in [r[0] for r in self.data]:
            self.data.append(record)
            with open(self.filename, 'a') as fp:
                fp.write(','.join(record) + '\n')
            return True
        else:
            return False
            #TODO: update record
    
    def get(self, user):
        res = [r[1] for r in self.data if r[0] == user]
        return res[0] if len(res) > 0 else None


if __name__ == "__main__":
    ## Test
    db = CSVDB()
    db.insert('a', 'b')
    db.insert('a', 'b')
    db.insert('c', 'e')
    
    print(db.get('a'))
    print(db.get('c'))
    print(db.get('d'))
