import os


def get_filenames(folder_path):
    filenames = [
        filename.replace(".py", "").replace("_", "-")
        for filename in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, filename))
        if filename != "__init__.py"
    ]
    return filenames


folder_path = "maple-leafs/spiders"
filenames = get_filenames(folder_path)

for filename in filenames:
    command = f'scrapy crawl {filename} -o output.jl -a keyword="Maple Leafs"'
    os.system(command)
