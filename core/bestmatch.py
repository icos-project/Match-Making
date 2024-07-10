from core.mmlog import save_to_log

from core.mmlog import get_logger

log = get_logger('__name__')
    
    
# Function to search for the best matching cluster and node based on resources  
def search_best_first_fit(taxonomy_json,app_req_components_list):
    ''' This function selects the best candidate for each component'''
    candidate_per_component_list=dict(app_req_components_list)
    for component in candidate_per_component_list['components']:
        if component['targets']:  #if list not empty
            component['targets']=component['targets'][0]
    print(candidate_per_component_list)
    return candidate_per_component_list


# Function to search for the best matching cluster and node based on resources  
def search_best(taxonomy_json,app_req_components_list):
    ''' This function selects the best candidate for each component'''
    candidate_per_component_list=search_best_first_fit(taxonomy_json,app_req_components_list)
    return candidate_per_component_list



