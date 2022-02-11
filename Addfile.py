import argparse
import sys
import os
import os.path
import shutil
import csv


def main():
    # creating a parser
    parser = argparse.ArgumentParser()
    # adding arguments
    parser.add_argument('--file', type=str, help='insert the file name and the extension')

    args = parser.parse_args()
    sys.stdout.write(str(move_file(args)))


# this function assign to 'newpath' the path of the folder in which the file should be moved
# if this path does not exists (meaning that the folder does not exist), than it creates a new one with 'folder_name'
def new_folder(dirpath, file_type, file):
    folder_name = file_type + 's'
    newpath = os.path.join(dirpath, folder_name)

    if not os.path.isdir(newpath):
        os.makedirs(os.path.join(dirpath, folder_name))

    return newpath


# this function creates a new csv file if this is not already present in the folder files.
# if the csv is already present it just append the now row at the end of the file
def createcsv(filecsv_name, dirpath, file, file_type, size):
    if os.path.exists(os.path.join(dirpath, filecsv_name)):
        app_or_write = 'a'  # append
    else:
        app_or_write = 'w'  # write

    print('app_or_write: ', app_or_write)  # print to be sure that we are not creating a new file everytime

    with open(os.path.join(dirpath, filecsv_name), app_or_write, newline='') as csvfile:
        recap = csv.writer(csvfile)

        # writing headers only if we are creating the file
        if app_or_write == 'w':
            recap.writerow(['name', 'type', 'size(B)'])
        # writing the data about the file moved
        recap.writerow([file, file_type, size])


def move_file(args):
    if not args.file == 'recap.csv':

        try:

            # creating a dictionary to assign each 'file type' to the correspondant extension
            dictionary = {'.jpeg': 'image',
                          '.jpg': 'image',
                          '.mp3': 'audio',
                          '.png': 'image',
                          '.txt': 'doc',
                          '.odt': 'doc', }

            print('dictionary', dictionary)  # just to check

            # getting the path of the folder in which the appendfile.py is
            directory = os.path.dirname(os.path.abspath(__file__))
            # dirpath is the path of the current folder\files
            dirpath = os.path.join(directory, 'files')

            print('dirpath', dirpath)  # just to check

            print('\nName: ', args.file)  # just to check

            size = os.path.getsize(os.path.join(dirpath, args.file))
            print('Size:  {} B '.format(size))

            # checking in the dictionary the file type according to the extension

            for key, value in dictionary.items():
                if args.file.endswith(key):
                    file_type = value
                    break  # just go out from the for when find correspondance, no need to iterate more

            print('Type: ', file_type)

            # calling the function new_folder
            newpath = new_folder(dirpath, file_type, args.file)
            # moving the file in the corresponding folder
            shutil.move(os.path.join(dirpath, args.file), os.path.join(newpath, args.file))

            # writing in a recap.csv file the information about the file, using the function createcsv
            filecsv_name = 'recap.csv'
            createcsv(filecsv_name, dirpath, args.file, file_type, size)

        except:
            print(
                'Il file inserito non è stato riconosciuto.\nRicordarsi di inserire il nome di un file presente nella cartella "files" e la sua estensione.')

    else:
        print('Il file recap.csv è il file di riepilogo.\nIMPOSSIBILE SPOSTARE')


if __name__ == '__main__':
    main()