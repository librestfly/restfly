'''
version info
'''
VERSION = '1.4.7'
AUTHOR = 'Steve McGrath <steve@mcgrath.sh>'
DESCRIPTION = 'REST API library framework'
version_info = tuple(
    int(d) for d in VERSION.split("-", maxsplit=1)[0].split(".")
)
