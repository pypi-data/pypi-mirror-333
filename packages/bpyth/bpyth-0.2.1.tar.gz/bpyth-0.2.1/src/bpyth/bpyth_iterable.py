
try:
  from collections import Iterable
except:
    from collections.abc import Iterable

from collections        import Counter, defaultdict
from functools          import lru_cache  


          
            
            
            
#############################################################################################################
###
### List
###
############################################################################################################# 




def remove_dups(seq):
    """
    Removes duplicates from a list while preserving the original order.

    This function considers elements of different types as distinct, even if their values are equal.
    For example, `1` (integer), `1.0` (float), and `True` (boolean) are treated as different elements.

    Args:
        seq: The input list (or any iterable).

    Returns:
        A new list with duplicates removed, maintaining the original order.

    Examples:
        >>> remove_dups([1, 2, 2, 3, 4, 4, 4, 5])
        [1, 2, 3, 4, 5]
        >>> remove_dups([1, 1.0, 1.0, "1", "1", True, True, False, False, None, None, "1"])
        [1, 1.0, '1', True, False, None]
        >>> remove_dups([1, (1,2), (1,2), [1,2], [1,2], {1,2}, {1,2}])
        [1, (1, 2), [1, 2], {1, 2}]
    """
    seen = []
    result = []
    for x in seq:
        if (x, type(x)) not in seen:
            seen.append((x, type(x)))
            result.append(x)
    return result






def sort_by_priority_list(sortme_list, priority, default_value=float('inf') ):
    """
    Sort a list by a list or tuple of prioritized objects.
    (You can prepare the priority object with make_priority_dict,
    if you want to use always the same priorities in pandas)
    """

    if len(sortme_list) < 2:
        return sortme_list

    if type(priority) is tuple:
        priority = make_priority_dict(priority, default_value)

    elif type(priority) is list:
        priority = make_priority_dict(tuple(priority), default_value)

    priority_getter = priority.__getitem__  # dict.get(key)
    return [x[1] for x in sorted(enumerate(sortme_list), key=lambda x: (priority_getter(x[1]), x[0]))]


@lru_cache
def make_priority_dict(priority_tuple, default_value=float('inf')):
    # print('Neuberechnung')
    priority_list = list(priority_tuple)
    return defaultdict(lambda: default_value, zip(priority_list, range(len(priority_list))))



#############################################################################################################
###
### Counter
###
############################################################################################################# 



def cut_counter( counts, cut_percent ):
    '''Truncates rare values of a counter, given a percent value 0..100'''
    if cut_percent <= 0:
        return counts
    if cut_percent >= 100:
        return Counter()    
    minvalue = int(0.5 + sum(counts.values()) * (cut_percent / 100.0))
    #print(minvalue)
    filtered = { k:counts[k] for k in counts if counts[k] > minvalue } 
    return Counter(filtered)

counter_belöschen = cut_counter    




def ranking_from_counter( counts ):
    '''Converts a counter into a ranking.
    Returns a sorted dict.'''
    ranking = {pair[0]: rank  for rank, pair in enumerate(counts.most_common())}   
    return ranking     





#############################################################################################################
###
### Iterable
###
############################################################################################################# 


def flatten(items):
    """
    Yields all elements from a potentially nested iterable, effectively flattening the structure.
    Nested lists, tuples, and other iterables are traversed recursively, yielding their individual elements.
    Strings and bytes are treated as single elements and are not flattened further.
    """
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in flatten(x):
                yield sub_x
        else:
            yield x


            
#############################################################################################################
###
### Set
###
#############################################################################################################             
    

    
def minivenn(set0, set1, format='dict'):
    """
    Compare two iterables like sets. Returns 3 sets like a Venndiagram.
    format='print'         Formated print of a dict with 3 keys   
    format='print2'        Formated print of a dict with 2 keys      
    format='dict':         Returns a dict with 3 keys 
    format='list':         Returns a list with 3 elements
    format='count':        Returns a dict with 3 keys , the elements are only counts of the Venndiagramm.
    """
    
    if not isinstance(set0, set):
        set0 = set(set0)
    if not isinstance(set1, set):        
        set1 = set(set1)  
        
    if format=='dict':
        result = { 'left_only':  set0 - set1,
                   'both':       set0 & set1,
                   'right_only': set1 - set0,              
                 }  
    
    elif format=='count':
        result = { 'left_only':  len(set0 - set1),
                   'both':       len(set0 & set1),
                   'right_only': len(set1 - set0),              
                 }      
    
    elif format=='list':
        result = [set0 - set1, 
                  set0 & set1,
                  set1 - set0] 
        
    elif format=='print':
        v = [set0 - set1, 
             set0 & set1,
             set1 - set0]         
        result = 'left_only:  {0}\nboth:       {1}\nright_only: {2}\n'.format(*v) 
        result = result.replace('set()','{}')
        print(result)
        return
    
    elif format=='print2':
        v = [set0 - set1, 
             set1 - set0]         
        result = 'left_only:  {0}\nright_only: {1}\n'.format(*v) 
        result = result.replace('set()','{}')
        print(result)
        return    
            
        
    else:
        raise ValueError('format not recognised')
        
    return result
    
    
    