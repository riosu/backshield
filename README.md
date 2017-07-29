# Backshield 
Backshield is simple backup tool for server configurations with git.

# Install
```
ln -s "`pwd`/backshield.py" /usr/local/bin/backshield
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