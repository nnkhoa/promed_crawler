import justext
import os

def remove_boiler_plate(raw_dir, file_name, output_dir):
    f = open(raw_dir + file_name, 'r')
    output = open(output_dir + file_name, 'w+')
    
    content = f.read()
    
    paragraphs = justext.justext(content, justext.get_stoplist('English'))

    for paragraph in paragraphs:
        if not paragraph.is_boilerplate:
            output.write("<p>%s</p>\n"%paragraph.text)
    
    f.close()
    output.close()

def get_raw_content(raw_directory):
    return [raw_file for raw_file in os.listdir(raw_directory) if os.path.isfile(os.path.join(raw_directory, raw_file))]

# TODO use os for directory access and such
if __name__ == "__main__":
    raw_dir = "./content/"
    output_dir = "noBoilerPlate"

    try:
        os.mkdir(output_dir)
        print("Directory " + output_dir + " created.")
    except FileExistsError:
        print("Directory " + output_dir + " existed.")
    
    output_dir = "./noBoilerPlate/"

    raw_list = get_raw_content(raw_dir)
    for raw_file in raw_list:
        remove_boiler_plate(raw_dir, raw_file, output_dir)
