# pass_calculator
pip3 install -r ./pass_calculator/requirements.txt
python3 ./pass_calculator/setup.py bdist_wheel
python3 -m pip install ./rads/dist/rads*.whl

# rads
pip3 install -r ./rads/requirements.txt
python3 ./rads/setup.py bdist_wheel
python3 -m pip install ./rads/dist/rads*.whl
