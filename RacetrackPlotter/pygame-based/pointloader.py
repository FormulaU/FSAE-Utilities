import csv
def main():
    data = load_data()
    print(data)

def load_data(filename='data.txt'): 
    data = [[]]
    with open(filename) as csv_file:
        data = [[]]
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if len(row) == 0:
                data = data + [[]]
#               print("New Line")
            else:
#               print(f"X: {row[0]}, Y: {row[1]}")
                data[-1] = data[-1] + [[int(row[0]), int(row[1])]]
    return data
if __name__ == "__main__":
    main()
