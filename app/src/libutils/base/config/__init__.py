import os.path as path

home = "/opt/sugarbox/config"
tar_path = "{}/{}".format(home, "tar")
base_path = path.abspath(path.join(__file__, "../../../../.."))
config_path = "{}{}".format(base_path, "/config/")
edge_package_structure_path = "{}/{}".format(home, "edge_package_structure")
