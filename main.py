import os
import pickle


class file():
    files = []
    def __init__(self, name, size, path):
        self.name = name
        self.size = size
        self.path = path
        file.files.append(self)
    def __str__(self):
        return self.name +'     '+ self.change()+'      ' +self.path

    def change(self): #This is used for converting bytes to other sized
        size = self.size
        if size >= 1024**3:
            size = str(round(size/(1024)**3,2))+'Gb'
        elif size >= 1024**2:
            size = str(round(size/(1024)**2,2)) + 'Mb'
        elif size >= 1024:
            size = str(round(size/1024,2)) + 'Kb'
        else: size = str(size) + 'b'
        return size


class Main():
    def __init__(self):
        self.files=[]
        while True:
            print('####SELECT OPTION####')
            print('1. Search Files In Specific Path')
            print('2. Save Files in database')
            print('3. Load Files from database')
            print('4. Show Files')
            opt = input()
            if opt == '1':
                path = input('Give the name of the path you want to search.(blank will search current dir)')
                if path == '':
                    self.find_files(os.getcwd())
                else:
                    self.find_files(path)
            elif opt == '2':
                filename = input('What name do you want to give to the file?') + '.db'
                self.save(filename)
            elif opt == '3':
                try:
                    filename = input('What is the name of the database file?') + '.db'
                    file.files = self.load(filename)
                    print(str(len(file.files)) + ' files loaded.')
                except FileNotFoundError:
                    print('There is no such file. Make sure you mention the right file and don\'t include the extension')
            elif opt == '4':
                try:
                    amount = int(input('How many files do you want to see?'))
                    self.print_files(amount)
                except ValueError:
                    print('Please give a number')
            elif opt == '':
                break

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(file.files, f)
            print('Succesfully created the database: {}'.format(filename))

    def load(self, filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)

    def find_files(self, path):
        file.files = [] #reset the files list
        for root, dirs, filenames in os.walk(path): #for the given path
            for name in filenames:
                try:
                    fullpathname = (os.path.join(root, name)) #creates the fullpath directory for the file
                    size = os.path.getsize(fullpathname) #gets the file of the file in bytes
                    file(name, size, fullpathname) #creates a file object
                except:
                    pass
        file.files.sort(key=lambda x: x.size, reverse=True) #sorts the files based on their size
        print(str(len(file.files)) + ' files found.')

    def print_files(self, amount):
        for f in file.files[:amount]:
            print(f)


if __name__ == '__main__':
    Main()

