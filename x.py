import requests
from bs4 import BeautifulSoup
import telebot

bot = telebot.TeleBot("7163297851:AAGc4a6XT86VUxh6zXsx_nlgDrleVAkwGKc")  # Replace "YOUR_TOKEN" with your actual bot token
chat_id = "6006736380"  # Replace "YOUR_CHAT_ID" with your actual chat ID

def cleanup_name(name):
    if ")" in name:
        name = name.split("(")[0]
    return name.rstrip().replace("'", "")

def cleanup_followers(followers):
    if "F" in followers:
        followers = followers.split("F")[0]
    return followers.rstrip().replace("'", "")

def cleanup_bio(bio, followers):
    y = followers[0]
    bio = bio.split(y)[0]
    return bio.strip().replace("'", "")

def get_instagram_info(username):
    url = f"https://www.instagram.com/{username}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    account_name = soup.select("meta[property='og:title']")
    account_name = account_name[0]['content']
    account_name = cleanup_name(account_name)
    followers = soup.find('meta', attrs={'name': 'description'})['content']
    followers = cleanup_followers(followers)
    following = soup.find('meta', attrs={'name': 'description'})['content'].split(",")[1].strip().split(" ")[0]
    posts = soup.find('meta', attrs={'name': 'description'})['content'].split(",")[2].strip().split(" ")[0]
    bio = soup.select("meta[property='og:description']")
    bio = bio[0]['content']
    bio = cleanup_bio(bio, followers)
    is_private = soup.select("meta[property='og:description']")
    is_private = "Private" in is_private[0]['content']
    api = f"https://www.instagram.com/{username}"
    an = requests.get(api).text
    idd = an.split('props":{"id":"')[1].split('"')[0]
    return {'Name': account_name ,'Followers': followers, 'Following': following, 'Posts': posts, 'Bio': bio, 'Id': idd, 'Is_private': is_private}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to Instagram Info Bot! Please enter the Instagram username you want to get information about.")

@bot.message_handler(func=lambda message: True)
def get_info(message):
    username = message.text
    try:
        info = get_instagram_info(username)
        response = ""
        for key, value in info.items():
            response += f"{key}: {value}n"
        bot.reply_to(message, response)
        bot.send_message(chat_id, f"Instagram info for {username}:n{response}")
    except Exception as e:
        bot.reply_to(message, "An error occurred. Please try again later.")
        print(e)

bot.polling()
