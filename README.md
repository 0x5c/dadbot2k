# dadbot2k

*A probabilistic dadjoking discord bot.*


## Features

- Probabilistic dadjoking
- Per-server chance configuration using a command (`dadctl chance [chance]`)


## Usage

1. Setup a venv and install the dependencies.
    ```none
    $ make install
    ```

2. Start the bot.
    ```none
    $ ./run.sh
    ```

*For advanced usage of the makefile and run script, refer to the documentation in [0x5c/quick-bot-no-pain](https://github.com/0x5c/quick-bot-no-pain).*


### Fileless config

Dadbot can get the Discord token and its configuration from environment instead of `keys.py` and `options.py`. It will only use environemnt if all the config keys from a file are passed in the environment instead. Doing so will fully disable loading the related config file.

```shell
# keys.py
DADBOT_DISCORD_TOKEN=token

# options.py
DADBOT_COMMAND_PREFIX="dadctl :Dadctl "
DADBOT_CHANCE_DIR="./data"
DADBOT_DEFAULT_CHANCE=0.25
```

To pass multiple command prefixes (a list in `options.py`), pass them as a colon-separated (`:`) string.  
eg: `DADBOT_COMMAND_PREFIX="dadctl :Dadctl :?:d!"`


## Docker

*Refer to instructions [here](./README-DOCKER.md).*


## Built using 0x5c/quick-bot-no-pain

Skip the boilerplate, Get straight to coding: [try it for yourself!](https://github.com/0x5c/quick-bot-no-pain)


## License

Copyright (c) 2021-2024 0x5c

Released under the terms of the BSD 3-Clause Licence.  
See [`LICENCE`](LICENCE) for the full license text.
