# CloudDump

Python script to automate database backups creation, uploading them to a cloud storage service.

Currently supports MySQL databases, with Mega.co.nz as storage service. Other database engines
and storage services can be easily added (see below).
 
## How To Use

CloudDump is actually composed by two different scripts: the main one, `clouddump.py`, is in charge
of dumping, compressing and uploading the database, while `cloudsweep.py` takes care of deleting outdated
dumps from the cloud service. Dump files will be named as `yyyymmddhhmmss_database_name.sql.gz`.

Before starting, you need to set up the configuration for both scripts in a JSON file
named `config.json` (a sample one is attached in the sources)

Both are designed to be executed as cron tasks. While `clouddump.py` ideally should be executed at least once a day,
`cloudsweep.py` doesn't need to be executed that often. In the end, that frequence will depend on the amount of available space
you have.

Needless to say, you should be **very** careful when executing `cloudsweep.py`, as it will remove **all** files older than
the specified number of days. It is recommended to store backups in a dedicated service account, or at least 
use a specific folder.

By default, both scripts will run silently, writing their outputs to log files located at the logs directory. If you want to see
this output also in the console, just add ` -v` or `--verbose`.

## Adding more services / database engines

You can add more services and database engines creating new drivers for them. To do that, write a new class that must inherit
from `Service` in the case of services and `Database` for database engines. 
Take a look at both `drivers/driver_mega.py` and `drivers/driver_mysql.py` for implementation examples.  
All drivers must be located in the drivers directory.
Driver file names must always start with `driver_`, followed by the driver name. To use your newly created driver, specify its name in the _driver_ param of the service / database section in the `config.json` file.

## Troubleshooting

You can view log files, stored in the `logs` directory.

## Requirements

  1. Python 2.7+
  2. mega.py - https://github.com/richardasaurus/mega.py

## To do

  1. Tests

## Contribute

Feel free to pull the source and make changes and additions.
Make a pull request with your changes.