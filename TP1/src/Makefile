# Signifies our python version
PYTHON = python3.9
.PHONY = help run clean
# Defines the default target that `make` will to try to make, or in the case of a phony target, execute the specified commands
# This target is executed whenever we just type `make`
.DEFAULT_GOAL = help

help:
	@echo "----------------HELP------------------"
	@echo "To run the project type make run"
	@echo "To clean project files type make clean"
	@echo "--------------------------------------"

run:
	${PYTHON} main.py

clean:
	rm -rf /html/*.html html
	rm -rf equipas.html