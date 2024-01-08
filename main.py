import tweepy
import api_keys
import random
import time
import os
from openai import OpenAI
from random_word import RandomWords

client1 = tweepy.Client(api_keys.bearer_token, api_keys.api_key, api_keys.api_key_secret, 
                       api_keys.access_token, api_keys.api_token_secret)



auth = tweepy.OAuth1UserHandler(api_keys.api_key, api_keys.api_key_secret, 
                       api_keys.access_token, api_keys.api_token_secret)

api_access = tweepy.API(auth)

# ^establishing connection

client2 = OpenAI(
    api_key=api_keys.openAi_key,
)


def generate_response(prompt, system_prompt, tokens):
    random_seed = random.randint(0, 100)
    chat_completion = client2.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        model="gpt-3.5-turbo",
        seed=random_seed,
        max_tokens=tokens,
        temperature=1,
    )
    return chat_completion.choices[0].message.content

def generate_topic_explanation(topic):
    system_prompt = f"You are a chatbot that gives a brief explanation about {topic}. throw in some relevant emojis and hashtags too!"
    prompt = f"Hello. This prompt is from an api request. basically I am using you to create a breif explanation of {topic}. "
    "Do not start off with anything before just start off with the explanation NO OTHER TEXT BEFORE."
    tweet_content = generate_response(prompt, system_prompt, 65)
    print(f"Your tweet is: {tweet_content}")
    
    client1.create_tweet(text=tweet_content)


def generate_random_fun_fact():
    r = RandomWords()
    random_technical_word = r.get_random_word()
    system_prompt = f"You are a chatbot that outputs fun facts about {random_technical_word}."
    "but when outputting just say Random Fun Fact: then the fact don't number them, throw in some relevant emojis and hashtags too!" 
    prompt = "Hello. This prompt is from an api request. I am using you to create fun fact tweets."
    "Please generate a fun fact. Do not start off with anything before just start off with the fun fact NO OTHER TEXT BEFORE."
    tweet_content = generate_response(prompt, system_prompt, 60)
    print(f" Your tweet is: {tweet_content}") 
    
    client1.create_tweet(text=tweet_content)


def modify_tweet(tweet_content, modification):
    system_prompt = f"You are a chatbot that does this modification on a tweet: {modification}"
    "Make sure to make the modfication a similar lenght to the orginal unless otherwise specified"
    "Also make sure to only output the modified version NO OTHER TEXT BEFORE."
    tweetx = generate_response(tweet_content, system_prompt, 60)
    print(f"Your tweet is: {tweetx}")

    client1.create_tweet(text=tweetx)
    
    


print("Hello Welcome to helpful_gpt, a Twitter bot you can control!")

#Want to make the bot more interactive so gpt will interpret what the user wants
system_prompt = "You are a chatbot that outputs only 1, 2, 3, 4. "
"I am trying to get you to interpret what the user is saying,"
"if the prompt says something similar to Generate 5 random fun facts then output the number 1, "
"if the prompt says something similar to get an explanation of a topic output the number 2,"
"if the prompt says something similar to modify a tweet then output the number 3"
"if the prompt says anything similar to quit then ouput the number 4. "
"PLEASE ONLY OUTPUT THE NUMBER"

while True:
    print("Please explain what you want to do, you have these options:")
    print("1. Generate 5 random fun facts")
    print("2. Get an explanation of a word or topic")
    print("3. Modify a tweet")
    print("4. Quit")
    
    
    user_input = input()
    content = f"Only output the number 1, 2, 3, or 4 as described in the system prompt that best correlates to this prompt please: {user_input}"
    choice = generate_response(content, system_prompt, 20)
    count1 = choice.count('1')
    count2 = choice.count('2')
    count3 = choice.count('3')
    count4 = choice.count('4')
    #print(choice)
    
    #5 random fun facts
    if count1 == 1:
        for i in range(5):
            generate_random_fun_fact()
        print("5 fun facts have been generated! Check @helpful_gpt on Twitter/x for them. Keep in mind rate limits!")
    
    #explanation of topic
    elif count2 == 1:
        user_input = input("Please enter a topic that you want an explanation of: ")
        generate_topic_explanation(user_input)
        print(f"An Explanation about {user_input} has been generated! Check @helpful_gpt on Twitter/x for the post. Keep in mind rate limits!")
    
    #help modifying a tweet
    elif count3 == 1:
        user_tweet = input("Please enter what you would like to tweet. Keep it under 280 characters: ")
        while len(user_tweet) > 280:
            print("Sorry, your tweet is too long. Please keep it under 280 characters.")
            user_tweet = input("Please enter what you would like to tweet: ")
            
        user_modification = input("How would you like us to modify this tweet? ")  
        modify_tweet(user_tweet, user_modification)
       
        print(f"Your tweet has been generated! Check @helpful_gpt on Twitter/x for the post. Keep in mind rate limits!")
    
   #quit
    elif count4 == 1:
        print("Exiting the program. Thanks for using @helpful_gpt. See you next time!")
        exit()
    else:
        print("Invalid request. Exiting the program")
        exit()
    
    """Notes: One thing to keep in mind is models can be unpredictable and openAI makes changes to their models everyday. 
       Therefore it might not always output the desired result. However, most of it should work fine. If you encounter a problem, 
       I would reccomend just having the user input a number when selecting what they want to do. GPT interpreting what the user is
       saying is more interactive but can be a little incositent/unpredictable with it's ouputs at time. Other than that everything seems
       to be pretty consistent. If you want to use/add on to this feel free. Happy coding :) """
    