import csv
import xlrd

def csv_from_excel():
    wb = xlrd.open_workbook('excel.xlsx')
    sh = wb.sheet_by_name('Final Scores')
    your_csv_file = open('your_csv_file.csv', 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()


def main():
    wb = xlrd.open_workbook(r'C:\Users\brett\OneDrive\Desktop\githubinfra\data\CS 196 SP20 Bash 1.xlsx')
    sh = wb.sheet_by_name('Final Scores')
    your_csv_file = open(r'C:\Users\brett\OneDrive\Desktop\githubinfra\data\Bash1.csv', 'w')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

# runs the csv_from_excel function:
if "__name__" == "__main__":
    main()