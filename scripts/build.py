from datapackage_utilities import building, processing

# clean directories to avoid errors
processing.clean_datapackage()

# get config file
config = building.get_config()

# initialize directories etc. based on config file
building.initialize_dpkg()

# run scripts to add data
import buses
import prepare_load
import prepare_technologies

building.infer_metadata()
