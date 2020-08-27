import time
from dateutil.parser import parse

def combine_filters(*filters):
    
    combined_filter = []
    
    for trace_filter in filters:
        if type(trace_filter) is list:
            combined_filter += trace_filter
        else:
            combined_filter.append(trace_filter)
    
    return(combined_filter)
    
    
def create_timespan_filter(start: str, end: str):
    
    timespan_filter = {'startInRange': False,
                       'endInRange': False,
                       'type': 'timeRangeFilter',
                       'from': time.mktime(parse(start).timetuple()) * 1000,
                       'to': time.mktime(parse(end).timetuple()) * 1000}
    
    return(timespan_filter)
    

def create_attribute_filter(attribute_name: str, values: list):
    
    attribute_filter = {
        'type': 'attributeFilter',
        'attributeName': attribute_name,
        'values': values
        }
    
    return(attribute_filter)
    
    
def create_numeric_attribute_filter(attribute_name: str, value_min, value_max):
    
    numeric_attribute_filter = {
        'type': 'numericAttributeFilter',
        'attributeName': attribute_name,
        'min': value_min,
        'max': value_max
        }
    
    return(numeric_attribute_filter)
    
    
def create_variant_slider_filter(group_min: int, group_max: int):
    
    variant_slider_filter = {
        'type': 'variantSliderFilter',
        'min': group_min,
        'max': group_max
        }
    
    return(variant_slider_filter)
    
    
def create_activity_filter(activity: str, include: bool = True):
    
    activity_filter = {
        'type': 'activityFilter',
        'activity': activity,
        'inverted': not include
        }
    
    return(activity_filter)
    
    
def create_activity_filters(include: list, exclude: list = []):
    
    activity_filters = [create_activity_filter(activity) for activity in include] +\
    [create_activity_filter(activity, include = False) for activity in exclude]
    
    return(activity_filters)
    
    
def create_follower_filter(pre: str, succ: str, direct_follower = False, include = True):
    
    if pre == "Start":
        pre = "__LANA_START__"
    
    if succ == "End":
        succ = "__LANA_END__"
    
    follower_filter = {
        'type': 'followerFilter',
        'pre': pre,
        'succ': succ,
        'direct': direct_follower,
        'inverted': not include
        }
    
    return(follower_filter)