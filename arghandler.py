import argparse 

def parse_argv():
    parser = argparse.ArgumentParser(prog='promed_crawler', description='Process input for searching ProMed\'s database')
    parser.add_argument('--search', required = False, default = '', help = 'search for disease')
    parser.add_argument('--date-start', required = False, default = '2019-01-01', help = 'start of search range (format YYYY-MM-DD)')
    parser.add_argument('--date-end', required = False, default = '', help = 'end of search range (format YYYY-MM-DD)')
    
    args = parser.parse_args()
    print(vars(args))
    return vars(args)
