Watercolor's backend. Uses k8 and docker.
# Setup
	#create virtual environment
	python3 -m venv venv
	#activate
	. venv/bin/activate
	#install flask
	pip install flask
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
to run the project do `python app.py` in the api/ folder
