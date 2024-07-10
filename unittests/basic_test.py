from core.main import matchmaking_main
from core.utils.dataformats import read_yaml_file,read_agregator_file
from core.mmlog import get_logger
import os

log = get_logger('__name__')

if __name__ == '__main__':
    log.info('Running basic test')
    print(os.getcwd())
    appdesc_yaml= read_yaml_file('unittests/application.yaml')
    log.info('App descriptor:')
    log.info(appdesc_yaml)
    print(os.getcwd())
    taxonomy_json = read_agregator_file('unittests/agregator.json')
    log.info('Taxonomy:')
    log.info(taxonomy_json)
    result=matchmaking_main(appdesc_yaml,taxonomy_json)
    print("Final matching:")
    print(result)
