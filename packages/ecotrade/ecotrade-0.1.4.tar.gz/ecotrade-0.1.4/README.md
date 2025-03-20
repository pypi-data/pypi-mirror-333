Ecotrade PY

rm -rf dist/
python setup.py sdist bdist_wheel
python -m twine upload -u __token__ -p pypi-AgEIcHlwaS5vcmcCJGFjMjZhNDA1LTg0OTEtNDQ5ZS1iODBjLWI2ODFkOTIwNjc4YwACKlszLCIwMTdmNzJhYi0yYmY0LTQ2MDktYjI0Yy02ZDVkYTBlZjNlM2YiXQAABiDuddemgIJc16zLLNMzyAiUowwHuIKXIAr4tG6y8Hgh2g dist/*


python -m pip install --upgrade Ecotrade