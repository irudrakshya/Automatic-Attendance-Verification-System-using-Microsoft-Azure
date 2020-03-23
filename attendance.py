import csv
import os

'''
# Attendance marking in csv file
    loc = os.getcwd() + '\Attendance.csv'
    csv_path = os.path.join(loc)
    with open(csv_path, 'w', newline='') as w:
        thewriter = csv.writer(w)
        thewriter.writerow(['Names', 'Attendance'])
        for _ in names.keys():
            thewriter.writerow([_,0])

    w.close()
    with open(csv_path, 'r') as w:
        thereader = csv.reader(w)
        content = list(thereader)
        for i in range(len(content)):
            if content[i][0] in person_identified:
                content[i][1] = 1
    w.close()
    with open(csv_path, 'w', newline='') as w:
        thewriter = csv.writer(w)
        thewriter.writerows(content)

    os.startfile(csv_path)
    print("Attendance taken successfully!")
'''


class Attendance:

    def writer(self, header, data, filename, option):
        with open(filename, "w", newline="") as csvfile:
            if option == "write":

                movies = csv.writer(csvfile)
                movies.writerow(header)
                for x in data:
                    movies.writerow(x)
            elif option == "update":
                writer = csv.DictWriter(csvfile, fieldnames=header)
                writer.writeheader()
                writer.writerows(data)
            else:
                print("Option is not known")

    def updater(self, filename, names):
        with open(filename, newline="") as file:
            readData = [row for row in csv.DictReader(file)]
            # readData[2]['Attendance'] = 1
            for row in readData:
                if row['Names'] in names:
                    row['Attendance'] = 1

        readHeader = readData[0].keys()
        self.writer(readHeader, readData, filename, "update")
