import requests
from html.parser import HTMLParser


class ProjectException(Exception):
    pass

class ExtranetParser(HTMLParser):
    def handle_data(self, data):
        print("Found data  :", data)

def get_config():
    """ Parse config file
        and save data as a dictionary
    """

    try:
        with open('config.txt') as f:
            settings={}
            for line in f:
                line = line.strip()
                settings[(line.split('=')[0])]=(line.split('=')[1])
    except IOError:
        raise ProjectException("Config file not found")
    return settings


def get_image(get_config):

    try:
        status_code = requests.get(get_config['url'], auth=(get_config['user'], get_config['pass'])).status_code
        if status_code == 200:
            pass
        else:
            raise ProjectException('URL return {0} code'.format(status_code))
        text = requests.get(get_config['url'], auth=(get_config['user'], get_config['pass'])).text

        parser = ExtranetParser()
        parsed = parser.feed(text)


    except ProjectException:
        raise ProjectException()
    return parsed



def main():

    print(get_image(get_config()))

main()