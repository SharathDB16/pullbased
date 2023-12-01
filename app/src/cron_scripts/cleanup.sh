#!/bin/bash

find /opt/sugarbox/config/tar -mtime +0 -type f -delete

pkg_struct_dir=/opt/sugarbox/config/edge_package_structure
cd $pkg_struct_dir && find . -mtime +0 -delete && find . -type d -empty -delete
