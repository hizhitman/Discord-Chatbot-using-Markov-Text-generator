import spacy  #import spacy: This imports the Spacy library, which is a popular open-source library for NLP in Python.
import re #This imports the re module, which provides support for regular expressions in Python.
import markovify
import nltk
from nltk.corpus import gutenberg
import warnings
warnings.filterwarnings('ignore')
#nltk.download('gutenberg')
import discord
from dotenv import load_dotenv
# IMPORT THE OS MODULE.
import os
from pathlib import Path

dotenv_path = Path('/Users/rajakumarisureshbabu/HelloWorld/amiz/ftyu/t.env')
load_dotenv(dotenv_path=dotenv_path)
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
#print(gutenberg.fileids())



hamlet = gutenberg.raw('shakespeare-hamlet.txt')
macbeth = gutenberg.raw('shakespeare-macbeth.txt')
caesar = gutenberg.raw('shakespeare-caesar.txt')
whit = gutenberg.raw('whitman-leaves.txt')

#print('\nRaw:\n', hamlet[:100])
#print('\nRaw:\n', macbeth[:100])
#print('\nRaw:\n', caesar[:100])

def text_cleaner(text):
  text = re.sub(r'--', ' ', text)
  text = re.sub('[\[].*?[\]]', '', text)
  text = re.sub(r'(\b|\s+\-?|^\-?)(\d+|\d*\.\d+)\b','', text)
  text = ' '.join(text.split())
  return text

#remove chapter indicator
hamlet = re.sub(r'Chapter \d+', '', hamlet)
macbeth = re.sub(r'Chapter \d+', '', macbeth)
caesar = re.sub(r'Chapter \d+', '', caesar)
whit= re.sub(r'Chapter \d+', '', whit)
#apply cleaning function to corpus
hamlet = text_cleaner(hamlet)
caesar = text_cleaner(caesar)
macbeth = text_cleaner(macbeth)
whit = text_cleaner(whit)

#parse cleaned novels
nlp = spacy.load("en_core_web_sm")
hamlet_doc = nlp(hamlet)
macbeth_doc = nlp(macbeth)
caesar_doc = nlp(caesar)
whit_doc=nlp(whit)

hamlet_sents = ' '.join([sent.text for sent in hamlet_doc.sents if len(sent.text) > 1])
macbeth_sents = ' '.join([sent.text for sent in macbeth_doc.sents if len(sent.text) > 1])
caesar_sents = ' '.join([sent.text for sent in caesar_doc.sents if len(sent.text) > 1])
whit_sents = ' '.join([sent.text for sent in whit_doc.sents if len(sent.text) > 1])
shakespeare_sents = hamlet_sents + macbeth_sents + caesar_sents + whit_sents
#inspect our text
#print(shakespeare_sents)

#create text generator using markovify
generator_1 = markovify.Text(shakespeare_sents, state_size=3)

#next we will use spacy's part of speech to generate more legible text
class POSifiedText(markovify.Text):
   def word_split(self, sentence):
      return ['::'.join((word.orth_, word.pos_)) for word in nlp(sentence)]
   def word_join(self, words):
      sentence = ' '.join(word.split('::')[0] for word in words)
      return sentence
#Call the class on our text
generator_2 = POSifiedText(shakespeare_sents, state_size=3)


bot=discord.Client(intents=discord.Intents.default())

@bot.event
async def on_ready():
	guild_count = 0
	for guild in bot.guilds:
		# PRINT THE SERVER'S ID AND NAME.
		print(f"- {guild.id} (name: {guild.name})")

		# INCREMENTS THE GUILD COUNTER.
		guild_count = guild_count + 1

	# PRINTS HOW MANY GUILDS / SERVERS THE BOT IS IN.


	print("SampleDiscordBot is in " + str(guild_count) + " guilds.")

# EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL.
@bot.event
async def on_message(message):
	# CHECKS IF THE MESSAGE THAT WAS SENT IS EQUAL TO "HELLO".
	if message.content == "How dost thou?":
		# SENDS BACK A MESSAGE TO THE CHANNEL.
		await message.channel.send("generator_2.make_sentence()")
#if message.content == "hi":
		# SENDS BACK A MESSAGE TO THE CHANNEL.
		#await message.channel.send("generator_2.make_short_sentence(max_chars=100)")

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run(DISCORD_TOKEN)