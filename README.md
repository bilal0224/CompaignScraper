# CompaignScraper- A Simple Kickstarter Scraper
DigLit is simple python program that scrapes kickstarter campaign data and provides it in json format.

## Getting Started
To start using the diglit, clone the repo and install the dependencies. You need have `Python3` and `Pip3` installed.
```bash
git clone https://github.com/bilal0224/CompaignScraper.git
cd CompaignScraper.
pip3 install -r dependencies.txt
```

## Usuage
You need to run the following command and enter the password for kickstarter account where campaign name is the unique name of campaign in url and -u takes the username of kickstarter.
```bash
python3 diglit.py -c Campign-name-in-url -u Username
```
You will be prompted for password, enter the password and data will be printed and save in file.

You can also view format and available commands with
```bash
python3 diglit.py -h
```

## License
The code is free to use for any personal or bussiness application development purposes.