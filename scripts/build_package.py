from datapackage_utilities import building, processing

# clean directories to avoid errors
processing.clean_datapackage(directories=['data', 'resources', 'cache'])

# get config file
config = building.get_config()

# initialize directories etc. based on config file
building.initialize_dpkg()

# run scripts to add data
import buses
import load
import renewable_profiles
import technologies

building.infer_metadata(package_name='100-sea-2050')
