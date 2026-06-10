from configparser import ConfigParser

def config(filename="database.ini", section="postgresql"):
    # Create parser
    parser = ConfigParser()
    # Read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        # assign all elements into db dictionary
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section{0} is not found in {1} file'.format(section, filename))
    return db