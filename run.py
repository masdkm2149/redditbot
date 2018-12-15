import praw
import config
import urllib2
import time
import urllib
import os

def bot_login():
	print("Logging in...")
	r = praw.Reddit(username = config.username,
				password = config.password,
				client_id = config.client_id,
				client_secret = config.client_secret,
				user_agent = "Beep Boop Bot")
	print("Logged in!")

	return r

def checkingvotes():
    print("Checking votes.")

def run_bot(r, comments_replied_to):
	print("Searching last 1,000 comments")

	for comment in r.subreddit('Damnthatsinteresting+test+DesignPorn+DidntKnowIWantedThat+Eyebleach+Perfectfit+Unexpected+aww+blackmagicfuckery+funny+geek+gifs+gifsthatkeepongiving+holdmybeer+interestingasfuck+oddlysatisfying+pics+videos+woahdude+combinedgifs+beamazed+nextfuckinglevel+wholesomegifs+noisygifs+ofcoursethatsathing+productporn+holdmycatnip+bettereveryloop+gifsthatendtoosoon+holdmycosmo+geek+yesyesyesno+yesyesyesyesno').comments(limit=1000):
		if "/u/BotDetective test" in comment.body and comment.id not in comments_replied_to and comment.author or "etrendan.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "geekydeal.store/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "pearlgadget.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "stiflingdeals.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "prenkart.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "kickize.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author or "hashtagssale.com/products/" in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me():
			print("String with \"fishy link\" found in comment " + comment.id)
			comment.reply("**WARNING:** This is likely a fake account setup to promote the product shown in the video, please don't encourage this by either visiting the website or upvoting.\n\nThese bots are setup to steal unique comments from other users to pass as real people.\n\nIf you would like to help verify whether this user is a bot, you can check for duplicate comments using redditsearch.io\n\n**^If ^the ^user ^is ^indeed ^a ^bot, ^please ^report ^the ^message ^to ^the ^moderators, ^If ^you ^believe ^this ^was ^a ^mistake, [^send ^me ^a ^message!](https://www.reddit.com/message/compose/?to=-WarHounds-&subject=BotDetective - Error)**")
			print("Replied to comment " + comment.id)

			comments_replied_to.append(comment.id)

			with open ("comments_replied_to.txt", "a") as f, open('acc_history.txt', 'w') as c, open ("check_if_op_is_bot.txt", "w") as b:
				f.write(comment.id + "\n")
				b.write("https://api.pushshift.io/reddit/search/comment/?author=" + comment.submission.author.name + "\n")

	print("Search Completed.")

	print(comments_replied_to)

	get_karma()

	print("Sleeping for 60 seconds...")
	#Sleep for 10 seconds...
	time.sleep(60)

def get_karma():
    user = r.user.me()
    comment_list = user.comments.new(limit=20)
    p_id = open("Parent_id.txt","a+")
    for comment in comment_list:
            if comment.score < -2:
                parent_id = comment.parent_id
                if parent_id not in p_id.read().split("\n"):
                    parent_comment = r.comment(id=parent_id)
                    body = comment.body
                    comment.delete()
                    parent_comment.reply(body)
                    p_id.write(comment.parent_id + "\n")
                    print("Comment reposted.")
            else:
                checkingvotes()

def get_saved_comments():
	if not os.path.isfile("comments_replied_to.txt"):
		comments_replied_to = []
	else:
		with open("comments_replied_to.txt", "r") as f:
			comments_replied_to = f.read()
			comments_replied_to = comments_replied_to.split("\n")
			comments_replied_to = filter(None, comments_replied_to)

	return comments_replied_to

r = bot_login()
comments_replied_to = get_saved_comments()
print(comments_replied_to)

while True:
	run_bot(r, comments_replied_to)
