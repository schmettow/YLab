#import glob

ydt_path = r'e:\\ylab_buzzwire1676980172.ydt'
csv_path = r'e:\\ylab_buzzwire1676980172.csv'
#files = glob.glob(ydt_path)
#print(files)



from struct import iter_unpack
import os

ydt_format = "@fif"

def read_ydt(path):
    out = []
    with open(path, "rb") as file:
        pdata = file.read()
    pdata = iter_unpack(ydt_format, pdata)
    for row in pdata:
        out.append(row)
    return out

def write_csv(data, path):
    import csv
    with open(path, "w") as f:
        writer = csv.writer(f)
        writer.writerows(data)


def printcwd():
    print(os.listdir(os.getcwd()))    

data = read_ydt(ydt_path)
write_csv(data, csv_path)

print(data)