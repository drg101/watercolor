Watercolor's backend. Uses k8 and docker.
# Setup
	#create virtual environment
	conda create --prefix ./env python=3.7
	#activate
	conda activate ./env
	#install flask
	pip install flask
	#install flask_restful
	pip install flask_restful
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
	. venv/bin/activate
to run the project:

	cd watercolor/backend/api
	python app.py
