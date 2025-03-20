
import os, pickle, warnings

#, sys, time, random, string, re, datetime

 
    
#############################################################################################################
###
### Permanence
###
#############################################################################################################    


def dump_pickle( anything, filename ):
    '''
    open, dump, close
    '''
    f = open(filename,'wb')
    try:
        pickle.dump( anything, f )
    finally:
        f.close()
        
        
    


def load_pickle(filename):
    """
    open, load, close
    Handles FileNotFoundError and pickle.UnpicklingError.
    """
    try:
        with open(filename, 'rb') as f:
            result = pickle.load(f)
        return result
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except pickle.UnpicklingError:
        print(f"Error: Could not unpickle '{filename}'. The file might be corrupted.")
        return None




            

class StreamFiles(object):
    """Iterable, returns all filenames of a parent directory.
       Instantiation with
       * a path which is traversed recursively
       * a file extension. All other files will be igorated.
    """

    def __init__(self, _path, _extension):
        self.path = _path
        self.extension = _extension

    def __iter__(self):
        """Yields one filename."""
        for verzeichnis, egal_subdirs, dateien in os.walk(self.path):
            dateien.sort()
            for fname in dateien:
                if not fname.endswith(self.extension):
                    continue
                fname_full = os.path.join(verzeichnis, fname)  # Dateiname der Quell-Datei
                yield fname_full


StreamDateien = StreamFiles

                
                

class StreamLines(object):
    """Iterable, returns all lines of a text file"""

    def __init__(self, _filename):
        self.filename = _filename


    def __iter__(self):
        """Streams the file line by line."""
        with open(self.filename, 'r') as f:
            for zeile in f:
                yield zeile

            
StreamZeilen = StreamLines            
            
    
def path_join(basepath, supplement, test='ignore'):
    """
    Robustly joins two path parts of a path.
    With optionally test if the directory and/or the path exist.
    basepath:   a path
    supplement: path to join.
    test:       should it be checked if the path or the directory exist? If yes, set it to 'warn' or 'raise'.
    """
    supplement = os.path.normpath(supplement)
    parts = tuple(supplement.split(os.sep))
    result = os.path.join(basepath, *parts)

    if test == 'warn':
        if not os.path.exists(os.path.dirname(result)):
            warnings.warn('Directory does not exist: ' + os.path.dirname(result))
        if not os.path.exists(result):
            warnings.warn('Path does not exist: ' + result)
    elif test == 'raise':
        if not os.path.exists(os.path.dirname(result)):
            raise Exception('Directory does not exist: ' + os.path.dirname(result))
        if not os.path.exists(result):
            raise Exception('Path does not exist: ' + result)

    return result

