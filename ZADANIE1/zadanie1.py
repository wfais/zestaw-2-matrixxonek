def dodaj_element(wejscie):
    
    maxDepthLevel = 0

    def find_max_depth(element, currentDepth):
        nonlocal maxDepthLevel
        
        if isinstance(element, (list, dict)): 
            if currentDepth > maxDepthLevel:
                maxDepthLevel = currentDepth
        
        if isinstance(element, (list, tuple)):
            for e in element:
                find_max_depth(e, currentDepth + 1)
        elif isinstance(element, dict):
            for e in element.values():
                find_max_depth(e, currentDepth + 1)
    
    def find_max_local_number(data):
        """Znajduje największą liczbę w liście, ignorując inne typy."""
        max_val = 0
        for element in data:
            if isinstance(element, (int, float)):
                max_val = max(max_val, element)
        return max_val
    
    def append_next_value(element, currentDepth):
        
        if isinstance(element, list):
            
            if currentDepth == maxDepthLevel:
                nowa_wartosc = find_max_local_number(element) + 1
                element.append(nowa_wartosc)
            
            for e in element[:]:
                append_next_value(e, currentDepth + 1)
                
        elif isinstance(element, tuple):
            for e in element:
                append_next_value(e, currentDepth + 1)
                
        elif isinstance(element, dict):
            for e in element.values():
                append_next_value(e, currentDepth + 1)

    if not isinstance(wejscie, (list, tuple, dict)):
        return wejscie

    find_max_depth(wejscie, 0)
    
    append_next_value(wejscie, 0) 
    
    return wejscie

if __name__ == '__main__':
    structure = [
        [],       
        {"a": ()},
        [1, 2, 3, 4]
    ]
    expected = [[1], {"a": ()}, [1, 2, 3, 4, 5]]
    
    print("Przed:", structure)
    dodaj_element(structure)
    print("Po:", structure)