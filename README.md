# Auto Tweet

Auto Tweet is a tool for automatically tweeting state and national debt information.

## Usage
* Create a twitter developer account https://developer.twitter.com/en/apply-for-access
* Once your account has been created create a new project and give it read, write, and direct messages access in the developer portal
* Get your api username and key and token username and key, you'll need to plug in these values in the script

* Create a linux based AWS instance https://aws.amazon.com/lightsail/
* Download Python3 to your aws instance 

```bash
sudo yum install python3
```

* Download chromedriver to your AWS instance 

```bash
cd/tmp/
wget https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver
```

* Download chrome to your AWS instance 

```bash
curl https://intoli.com/install-google-chrome.sh | bash
sudo mv /usr/bin/google-chrome-stable /usr/bin/google-chrome
google-chrome --version && which google-chrome
``` 

* Install dependencies
```bash
pip3 install -r requirements.txt
```

* Create bash scripts a cronjob will trigger to call the python file
```bash
echo "python3 ~/auto_tweet.py --type national" > national.sh
echo "python3 ~/auto_tweet.py --type state" > states.sh
```

* Create the cronjobs to trigger each script
```bash
crontab -e
0 18 * * * /home/ec2-user/national.sh
0 23 * * * /home/ec2-user/states.sh
```
