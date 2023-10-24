## Start bash file `setup.sh`.
## Or manual setup:
```
python -m venv venv
```
```
.\venv\Scripts\activate
```
```
pip install -r .\requirements.txt
```
```
mv .\.env_copy .\.env
```
```
cd src/
```
```
python manage.py migrate
```
