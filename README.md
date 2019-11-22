Extension for climate MAG
==============

Getting Started
---------------
- Clone repository
```
$ git clone https://github.com/acoto/magsequia.git ext_climate
```

- Activate the FormShare environment.
```
$ . ./path/to/FormShare/bin/activate
```

- Change directory into your newly created plugin.
```
$ cd ext_climate
```

- Build the plugin
```
$ python setup.py develop
```

- Add the plugin to the FormShare list of plugins by editing the following line in development.ini or production.ini
```
    #formshare.plugins = examplePlugin
    formshare.plugins = ext_climate
```

- Run FormShare again
