import csv

def loadCsv(filename):
    lines = csv.reader(open(filename))
    dataset = list(lines)
    for i in range(len(dataset)):
        dataset[i] = [float(x) for x in dataset[i]]
    return dataset

if __name__=='__main__':
    filename = 'pima-indians-diabetes.data.csv'
    dataset = loadCsv(filename)
    print dataset
    # print("loaded data file {0} with {1} rows").format(filename,len(dataset))