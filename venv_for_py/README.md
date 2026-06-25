# These comments are used to create a python venv for linux 



## for python3.14

```bash
pip install --user virtualenv --break-system-packages 
```

The above comment is one time, only for the first venv you create in a linux system

```bash
python3 -m virtualenv .venv
```

The above comment is for creating the venv

```bash
source .venv/bin/activate
```

The above comment is to activate the venv




# for python3.12

```bash
sudo apt install python3.12-venv -y
```

```bash
python3.12 -m venv .venv
```
