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
    print(f"Response: {tweet_content}")
    print(topic)
    # Uncomment the line below to tweet the random fun fact
    # client1.create_tweet(text=tweet_content)


def generate_random_fun_fact():
    r = RandomWords()
    random_technical_word = r.get_random_word()
    system_prompt = f"You are a chatbot that outputs fun facts about {random_technical_word} topics."
    " I will feed you the same prompt so try to be as random as possible with the output, "
    "but when outputting just say like Random Fun Fact: then the fact don't number them, throw in some relevant emojis and hashtags too!"
    
    prompt = "Hello. This prompt is from an api request. basically I am using you to create fun fact tweets."
    "Please generate a fun fact. Do not start off with anything before just start off with the fun fact NO OTHER TEXT BEFORE."
    tweet_content = generate_response(prompt, system_prompt, 60)
    print(f"Response: {tweet_content}")
    print(random_technical_word)
    # Uncomment the line below to tweet the explanation
    # client1.create_tweet(text=tweet_content)



print("Hello Welcome to helpful_gpt, a Twitter bot you can control!")
while True:
    print("Please explain what you want to do, you have these options:")
    print("1. Generate 5 random fun facts")
    print("2. Get an explanation of a word or topic")
    #want to make it more interactive rather than the user just selecting 1 or 2, so I'll have gpt interpret what the user inputs and make a decision.
    system_prompt = "You are a chatbot that outputs only 1, 2, 3. "
    "Basically I am trying to get you to interpret what the user is saying, so if the user says something similar to Generate 5 random fun facts then output the number 1, "
    "if the user says something similar to  Get an explanation of a topic output the number 2, if the user says anything similar to quit then ouput the number 3. "
    "Please only output a number, i am going to make the token limit very low as I would only like 1, 2, or 3 outputted thanks. NO OTHER TEXT BEFORE ONLY NUMBER 1 2 OR 3"
    "DO NOT I REPEAT DO NOT OUPTUT SURE... OR ANYTHING LITERALLY ONLY OUPUT THE NUMBER 1 2 OR 3 I CANNOT STRESS THIS ENOUGH ONLY THE NUMBER!!!!!!!!"
    user_input = input()
    content = f"Ok literally output only the number 1 2 or 3 like i described in the system prompt that best correlates to this prompt please: user_input"
    choice = generate_response(content, system_prompt, 20)
    count1 = choice.count('1')
    count2 = choice.count('2')
    count3 = choice.count('3')
    print(choice)
    if count1 == 1:
        for i in range(5):
            generate_random_fun_fact()
        print("5 fun facts have been generated! Check @helpful_gpt on Twitter/x for them. Keep in mind rate limits!")
    elif count2 == 1:
        user_input = input("Please enter a topic that you want an explanation of")
        generate_topic_explanation(user_input)
        print(f"An Explanation about {user_input} has been generated! Check @helpful_gpt on Twitter/x for the post. Keep in mind rate limits!")
    elif count3 == 1:
        print("Exiting the program. Thanks for using helpful_gpt. See you next time!")
        break
    else:
        print("Invalid request")
        break
    

'''Notes: is working kinda, just need to tweak the prompts as they are sometimes incosistent. 
   Sometimes prints the desired results other times prints unwanted parts despite me telling it not to. 
   need to work my way around this. Other than prompting should be fine
'''