
import struct as Struct

def ReadHeader(File):
    with open(File, 'rb') as File:
        Header = File.read(4)
        if Header != b'RPF\0':
            raise ValueError("Not a valid RPF File")
        Version = Struct.unpack('<I', File.read(4))[0]
        print("RPF Version: ", Version)

        Offset = Struct.unpack('<I', File.read(4))[0]
        Size = Struct.unpack('<I', File.read(4))[0]

        return Offset, Size
    

def ReadTable(Path, Offset, Size):
    with open(Path, 'rb') as File:
        File.seek(Offset)

        Table = []

        while File.tell() < Offset + Size:
            Length = Struct.unpack('<I',File.read(4))[0]
            Name = File.read(Length).decode('utf-8')

            FileOffset = Struct.unpack('<I',File.read(4))[0]
            FileSize = Struct.unpack('<I',File.read(4))[0]

            Table.append({
                'Name': Name,
                'Offset': FileOffset,
                'Size': FileSize
            })

        return Table

def ExtractFiles(Path, Table):
    with open(Path, 'rb') as File:
        for FileEntry in Table:
            Name = FileEntry['Name']
            Offset = FileEntry['Offset']
            Size = FileEntry['Size']
            File.seek(Offset)
            FileData = File.read(Size)

            with open(f"{Name}", 'wb') as Output:
                Output.write(FileData)
            print(f"Extracted {Name}")



if __name__ == "__main__":
    Path = input("Path to the File: ")
    try:
        Offset, Size = ReadHeader(Path)
        Table = ReadTable(Path, Offset, Size)
        ExtractFiles(Path, Table)
    except Exception as Error:
        print(f"Error: {Error}")