# CSE 6424 - Final Project

Our data collection and analysis scripts, and our dashboard for visualizating and understanding the data collected. (All data for the dashboard is precomputed into this repo).

![screenshot](img/screenshot.png)

## How to setup

In order to run the project you will need to install Python 3.10. Head to https://www.python.org/ to figure out how to install and download.

Next in your terminal, we will need to install `pipenv`, a tool that takes care of both package management and creating a virtual environment. To do this run the following command.

```bash
pip install pipenv
```

Once installed navigate to the folder for this project and run the following command.

```bash
pipenv install
```

This will create a virtual environment and install all the preqrueiesti packages you'll need to be able to run the web app and the project.

## How to run the web app

To run the web app is very simple, you'll only need to run this one command using `pipenv` to get the dashboard to come alive.

```
pipenv run python -m dashboard
```


That's seriously it, no more work needs to be done!!!!

## How to obtain data and perform experiment

All the code to perform the experiments are within the `data_scrape_and_sentiment` directory. First to get into it, run the following command.

```bash
pipenv run jupyter lab
```

This will open juypter lab which is needed to run the code in the jupyter notebooks in that directory. The first notebook is the text extract, use this to start collecting the all the subreddit posts using various keywords. This will take some time to run through, but after that you will have a a set of the raw large scale text data.

After that, move over to the sentiment data notebook, where we will load a state of the art sentiment transformer model to condense the large corpus of text data down to individual sentiment for each post. After this is done you should have the data now condensed down to purely sentiment by branch.

From here, add this data to the `raw` directory and run the following script to help condense and reorient the data into a more analytical and usable form for the dashboard

```
pipenv run python data_preparation.py
```

After that, you can start using the dashboard in order to start look at how various events reflect in changes in this data.
