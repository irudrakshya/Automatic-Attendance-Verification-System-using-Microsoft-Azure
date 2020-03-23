import csv
import os


class Attendance:

    def __init__(self):
        pass

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
            for row in readData:
                if row['Names'] in names:
                    row['Attendance'] = 1

        readHeader = readData[0].keys()
        self.writer(readHeader, readData, filename, "update")
