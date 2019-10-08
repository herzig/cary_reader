import pandas as pd
import numpy as np
from datetime import datetime
import re

class CaryData:
    """Reads and processes csv files from cary eclipse fluorescence spectrometer
    
    Attributes:
        file (str): path to the source csv file
        contains_log (bool): whether the source file contains additional log information at the end of the file 
        all_wavelengths_equal (bool): whether all spectra are defined over the same wavelength range. This is the case for 3D (excitation-emission matrix) scans. Use get_collapsed_df to get a collapsed dataset
        names (list of str): all list of all trace names
		collection_times (dict): contains the collection time for each trace name
    """

    file = None
    contains_log = False
    all_wavelengths_equal = False
    names = None
    collection_times = None
    
    _traces = {} 
    _df = None
    

    def __getitem__(self, name):
        """return the trace with the given name
        """
        return self._df[name]
    
    
    def get_collapsed_df(self):
        """returns a pandas dataframe containing one column per trace.
        
        The resulting dataframe contains n rows and m columns, where n is the number of data points (wavelength axis)
        and m is the number of spectra. This only works if all spectra in the original source file share the same wavelength range.
        """
        if not self.all_wavelengths_equal:
            raise RuntimeError('collapsed dataframe is only possible whenn all trace wavelengths are equal')
       
        # drop wavelength columns
        wavecols = self._df[self._df.columns[0:-1:2]]
        df = self._df.drop(wavecols.columns, axis=1)
        df.columns = self._traces.keys()
        df.index = wavecols.iloc[:,0]
        df.index.name = 'Wavelength (nm)'
        
        return df
    
    def get_ex_em_matrix(self):
        """returns an excitation-emission matrix in a pandas dataframe
        
        In a Cary Eclipse excitation emission matrix scan (3D scan), 
        the trace names contain the corresponding excitation wavelengths as a string
        This method extracts those names and converts them to numeric values.
        It also collapses the dataframe to a compact format (see get_collapsed_df()).
        
        The resulting dataframe contains n rows and m columns, where n is emission 
        wavelengths and m is the excitation wavelengths.
        """
        df = self.get_collapsed_df();
        
        # the excitation wavelength is encoded in each column name.
        # we extract it and convert it to float
        columns = [float(re.search(r'EX_(\d+\.\d+)', col).groups()[0]) for col in df]
        df.columns = columns 
        
        return df
    
    @staticmethod
    def from_csv(file):
        """reads spectra from a Cary Eclipse csv file and creates a new CaryData instance
        
        Args
            file (str): file path to the csv file
        """
        
        result = CaryData()
        
        result.file = file
    
        df = pd.read_csv(file, sep=',', skiprows=[1], encoding='latin_1')
        df.drop(df.columns[-1], axis='columns', inplace=True) # files always contain an extra, empty column

        # the .csv may contain log information after the actual spectrum data.
        # the log is separated from the spectrum data by an empty line.
        # We search the empty line and drop it:
        endidx = df.iloc[:,1:].isnull().all(axis=1).idxmax()
        result.contains_log = endidx != 0
        
        if result.contains_log:
            df.drop(df.index[endidx:], inplace=True)
            
        # convert all entries to float
        df = df.astype(float)
        
        # every second colum contains wavelength information.
        wavecols = df[df.columns[0:-1:2]]
        
        # check if all wavelengths are equal
        eq = [np.allclose(wavecols.iloc[:,i], wavecols.iloc[:,i+1]) for i in range(wavecols.shape[1]-1)]
        result.all_wavelengths_equal = all(eq)
        
        # split frame in a dictionary of series, each having a wavelength index and intensities as values
        for i in range(0,len(df.columns),2):
            wavelen = df.iloc[:,i];
            intensities = df.iloc[:,i+1]
            series = pd.Series(intensities)
            series.index = wavelen
            series.index.name = 'Wavelength (nm)'
            series.dropna(inplace=True)
            series.name = df.columns[i]
            result._traces[series.name] = series
            
        result.names = list(result._traces.keys())
        
        if result.contains_log:
            result._parse_log(endidx+2) # +2 because header rows not included in dataframe
            
        result._df = df
        return result
    
    
    def _parse_log(self, start_line):
        self.collection_times = {}
        name_dupl_counts = [0 for i in range(len(self.names))]
        
        with open(self.file) as f:
            
            current_trace = None
            for i, line in enumerate(f):
                if i < start_line: continue
                
                line = line[:-1] # remove \n
                if line in self.names:
                    current_trace = line
                    
                    # handle duplicate traces names, the same way as pandas (suffix .1 .2 .3 etc.)
                    idx = self.names.index(current_trace)
                    
                    if name_dupl_counts[idx] > 0:
                        current_trace = f'{current_trace}.{name_dupl_counts[idx]}'
                    name_dupl_counts[idx] += 1    
                                        
                    
                if current_trace is not None: # we are curently in a block corresponding to a trace
                    if line.startswith('Collection Time:'):
                        
                        t = datetime.strptime(line, 'Collection Time:  %m/%d/%Y %H:%M:%S %p')
                        self.collection_times[current_trace] = t