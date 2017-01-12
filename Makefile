.PHONY: install_dependencies

install_dependencies:
	# Download dependency packages via pip, into the workflow directory.
	# NOTE: If DistutilsOptionError occurs, see http://stackoverflow.com/questions/24257803
	# -
	pip install Alfred-Workflow==1.24 --upgrade --ignore-installed --target .      # -> workflow/
	pip install py-applescript        --upgrade --ignore-installed --target .      # -> applescript/
	rm -rf *.dist-info/
	# All DONE :)
