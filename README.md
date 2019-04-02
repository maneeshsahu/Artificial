## Python AT Command

### Installation

Install the python packages - APScheduler and RPyC that are not part of the standard distribution

You can install from the frozen requirements.txt of this project.

`pip install -r requirements.txt`

### Usage

Run the background scheduler before running any of the clients

`python -m server`

Run the clients

#### AT Python
echo 'echo hello world' | python at.py 9:30 PM Tue

#### ATQ Python

python atq.py

#### ATRM Python

python atrm.py




