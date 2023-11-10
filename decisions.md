# input file format is hdf5 with pandas dataframe dumps
- pandas dataframes are very common in our setting
- hdf5 enables collections of data, storage of meta data and compression in one file format

# metadata stored in the data files have to be plot agnostic
- as the same data file might be used with different plots it is necessary that not plot specific data is stored in this file. All plot specific data should be stored in the plot config

# there is a plot config which contains user overrides influencing the look and feel of single plots
- needed for example for different plot legends in different languages

# plot metadata is stored as a json string and is stored in the hdf5
- metadata needs to be serialized for secure storage and json is the most common format