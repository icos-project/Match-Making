from core.getrequirements import extract_resources
from core.bestmatch import search_best
from core.filtering import filter_taxonomy_candidates
from core.mmlog import get_logger

log = get_logger('__name__')

# Main matchmaking function, it gets the application descriptor and the taxonomy from aggregator in json
# For the re-scheduling there are two optional parameters the remediationAction and the actual setup TBD in which form
def matchmaking_main(appdesc_json: str, taxonomy_json:str, remediationAction=None, current_setup=[]): 

    log.info('Calling matchmaking with: \n AppDesc %s \n Taxonomy %s \n',appdesc_json,taxonomy_json)
    #print(appdesc_json[0]['components'])    
    # extract resources from json_data_list$
    app_req_components_list={}
    app_req_components_list['components']=extract_resources(appdesc_json) # getrequirements.py$
    #print(app_req_components_list)
    #app_req_candidates_list=filter_taxonomy_candidates(app_req_components_list ,taxonomy_json) #filtering.py$
    filter_taxonomy_candidates(app_req_components_list ,taxonomy_json) #filtering.py$
    #print(app_req_candidates_list)
    log.info('app_req_components_list has already the list of candidates per component:\n %s',app_req_components_list)
    #print('\nAfter filetering\n')
    #print(app_req_components_list)
    #search_best $
    candidates_per_component_list=search_best(taxonomy_json,app_req_components_list)
    return candidates_per_component_list