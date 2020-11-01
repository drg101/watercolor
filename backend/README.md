Watercolor's backend. Uses k8 and docker.
# Setup
	#create environment from file
	conda env create -p ./env -f environment.yml
# Structure 
	api/
		__init__.py
		app.py          # this file contains your app and routes
		resources/
			__init__.py
			r1.py #resource 
		common/
			__init__.py
			util.py #random utility files


# Running the project
First, activate the python environment:

	cd watercolor/backend
	conda activate ./env
to run the project:

	cd watercolor/backend/api
	python app.py
