import discord, requests, asyncpraw, random
from discord.ext import commands
from discord.ext.commands import Bot
from discord import FFmpegPCMAudio
from bs4 import BeautifulSoup

####################################### Haro Bot by Sarwar Rashid ####################################### 
# Functions as a general utility bot for the application Discord
# Made to practice Python 

bot = Bot(command_prefix="h! ") # Current prefix is h! 

# Command list
# h! cmd - Displays command list
# h! amazonitem - Finds specific amazon item
# h! amazonlist - Lists a set of amazon items which can be sorted
# h! redditimg - Returns a random image post from specified subreddit

@bot.event
async def on_ready():
    print('Haro! Haro!')

# List commands
@bot.command()
async def cmd(ctx):
    embed = discord.Embed(title = "Haro Command List", description = "Use h! to call Haro! Haro!\nUse \" \" if entering multiple keywords\n", colour = discord.Color.from_rgb(131, 186, 119))
    embed.add_field(name = ":tennis: Main commands :tennis:", value = "∎ **cmd** - Display Haro's commands\n", inline = False)
    embed.add_field(name = ":tools: Utility commands :tools:", value = "∎ **amazonitem [item name]** - Find a specific item from Amazon\n∎ **amazonlist [item name]** - List a set of amazon items\n∎ **redditimg [subreddit]** - Returns a random image post from specified subreddit", inline = False)
    embed.set_image(url = "https://i.stack.imgur.com/2haP4.jpg")
    await ctx.send(embed=embed)

# Amazon function
@bot.command()
async def amazonitem(ctx, name):
    url = "https://www.amazon.co.uk/s?k=" + name

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.content, "html.parser")

    product = soup.find("a", class_="a-link-normal s-no-outline") # Get approximate item
    await ctx.send("https://www.amazon.co.uk/" + product['href'])


@bot.command()
async def amazonlist(ctx, name, sort):
    count = 0 # Define amount the user can search up to // MAX 5

    # Sort by 
    featured = "s=relevanceblender&qid=1629203950&ref=sr_st_relevanceblender"
    sortByLow = "s=price-asc-rank&qid=1629203831&ref=sr_st_price-asc-rank"
    sortByHigh = "s=price-desc-rank&qid=1629203843&ref=sr_st_price-desc-rank"
    sortByReviews = "s=review-rank&qid=1629203907&ref=sr_st_review-rank"
    sortByNew = "s=date-desc-rank&qid=1629203924&ref=sr_st_date-desc-rank"

    url = ""

    if sort == "F":
        url = url = "https://www.amazon.co.uk/s?k=" + name + "&" + featured
    elif sort == "L":
        url = url = "https://www.amazon.co.uk/s?k=" + name + "&" + sortByLow
    elif sort == "H":
        url = url = "https://www.amazon.co.uk/s?k=" + name + "&" + sortByHigh
    elif sort == "R":
        url = url = "https://www.amazon.co.uk/s?k=" + name + "&" + sortByReviews
    else:
        url = url = "https://www.amazon.co.uk/s?k=" + name + "&" + sortByNew

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.content, "html.parser")

    if soup.find_all("div", class_="a-section a-spacing-none"):
        product = soup.find_all("div", class_="a-section a-spacing-none") # Get each item
        for product in product:
            try:
                if product.find("span", {"class": "a-size-base-plus a-color-base a-text-normal"}):
                    productName = product.find("span", {"class": "a-size-base-plus a-color-base a-text-normal"}) # Product name
                    productName = productName.text
                elif product.find("span", {"class": "a-size-medium a-color-base a-text-normal"}):
                    productName = product.find("span", {"class": "a-size-medium a-color-base a-text-normal"})
                    productName = productName.text

                productPrice = product.find("span", {"class": "a-offscreen"}) # Product price
                productPrice = productPrice.text

                await ctx.send(productName + " // " + productPrice + "\n")
                
                # Display a limited amount to prevent spam
                count += 1
                if count == 5:
                    break

            except AttributeError:
                pass
    elif soup.find_all("div", class_="a-section a-spacing-medium"):
        product = soup.find_all("div", class_="a-section a-spacing-medium") # Get each item
        for product in product:
            try:
                if product.find("span", {"class": "a-size-base-plus a-color-base a-text-normal"}):
                    productName = product.find("span", {"class": "a-size-base-plus a-color-base a-text-normal"}) # Product name
                    productName = productName.text
                elif product.find("span", {"class": "a-size-medium a-color-base a-text-normal"}):
                    productName = product.find("span", {"class": "a-size-medium a-color-base a-text-normal"})
                    productName = productName.text

                productPrice = product.find("span", {"class": "a-offscreen"}) # Product price
                productPrice = productPrice.text

                await ctx.send(productName + " // " + productPrice + "\n")

                # Display a limited amount to prevent spam
                count += 1
                if count == 5:
                    break

            except AttributeError:
                pass

# Reddit function
@bot.command()
async def redditimg(ctx, subredditname):
    subredditname = subredditname # User can decide the subreddit

    # Setup
    reddit = asyncpraw.Reddit(
        client_id="i61X67doYr4WJH5IBe7cog",
        client_secret="VC5QdFLuIKsso_SGeA4_vm8PRR0_VA",
        user_agent="Haro/Sarwar",
    )

    subreddit = await reddit.subreddit(subredditname)

    posts = []

    async for submission in subreddit.new(limit = 50):
        if submission.url.endswith("jpg") or submission.url.endswith("png") or submission.url.endswith("gif"):
            posts.append(submission.url) # Add all submissions to the array post

    await ctx.send(random.choice(posts)) # Then pick a random post from the array

# Error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Haro does not recognize that command !!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You're missing an argument !!")


# Haro on!
bot.run('ODc2MDgwOTE3NDU2NzY0OTI4.YRe37w.R9AJsmP2y6Ehtknjpwpy0ZQbgHY')