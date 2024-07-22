# GDELTS Conflict Analysis

To set up the project, [install pyenv](https://github.com/pyenv/pyenv), and run the following command:

```
pyenv install 3.12.4
```

Then [install Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer), and run the following command:

```
poetry install
```

When installing dependencies, make sure to use `poetry add` instead of `pip`. That way everyone can be sure that they are using the agreed upon versions of the packages.

Also, [direnv](https://direnv.net/) might be useful in the future, if we have to deal with secrets. But we will cross that bridge when we get to it.