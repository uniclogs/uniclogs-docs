

# pass_calculator
pip install -r ./pass_calculator/requirements.txt
python3 ./pass_calculator/setup.py bdist_wheel
python -m pip install ./rads/dist/rads*.whl

# rads
pip install -r ./rads/requirements.txt
python3 ./rads/setup.py bdist_wheel
python -m pip install ./rads/dist/rads*.whl
