# Backshield 
Backshield is simple backup tool for server configurations with git.

# Install
```
sudo su
cd /usr/local/src/
git clone git@github.com:riosu/backshield.git
cd backshield
./setup.sh
```

# Usages
```
# Initialize
$ ./backshield.py init <git repository url>

# Add file to backup
$ ./backshield.py add <filename>

# Add file to backup
$ ./backshield.py remove <filename>

# Add file to backup
$ ./backshield.py list

# Backup to git
$ ./backshiled.py backup
```