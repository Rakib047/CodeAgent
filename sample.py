# legacy_data_manager.py

class DataManager(object):
    def __init__(self, filename):
        self.filename = filename
        self.data = []
    
    def load_data(self):
        try:
            f = open(self.filename, 'r')
            header = f.readline()
            while True:
                line = f.readline()
                if not line:
                    break
                line = line.strip()
                if not line:
                    continue
                fields = line.split(',')
                if len(fields) != 3:
                    print "Skipping invalid line: %s" % line
                    continue
                self.data.append({
                    'name': fields[0],
                    'age': int(fields[1]),
                    'score': float(fields[2])
                })
            f.close()
        except IOError, e:
            print "Error opening file: %s" % e
    
    def average_score(self):
        total = 0.0
        count = 0
        for i in xrange(len(self.data)):
            total += self.data[i]['score']
            count += 1
        if count == 0:
            return 0
        return total / count
    
    def print_summary(self):
        avg = self.average_score()
        print "Processed %d entries" % len(self.data)
        print "Average score is %.2f" % avg

def main():
    import sys
    if len(sys.argv) < 2:
        print "Usage: python legacy_data_manager.py <filename>"
        sys.exit(1)
    
    manager = DataManager(sys.argv[1])
    manager.load_data()
    manager.print_summary()

if __name__ == '__main__':
    main()
