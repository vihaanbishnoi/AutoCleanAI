from scanner import scan_folder

folder = input("Enter folder path: ")

files = scan_folder(folder)

print("Files Found:")
for f in files:
    print(f)
