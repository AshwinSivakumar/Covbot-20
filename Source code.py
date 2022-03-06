import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings('ignore')

nltk.download('punkt', quiet=True)


sentence_list = ["Some of the common symptoms are: Shortness of breath, Severe cough, fever, fatigue. \n Headaches and sore throat are also some common symptoms.\nYou must immediately go to a doctor if you have any of the symptoms.",
                 "The history of the virus is traced to a food market in Wuhan, China in early 2020",
                 "It is hard to determine immediately whether it is covid or the flu as the symptoms are similar",
                 "The best way to prevent the virus is to wash your hands for atleast 20 seconds and to socially distance yourself from crowded places. "
                 "Wearing a mask also prevents the transmission of the virus",
                 "The vaccine is not ready yet, some trials are at their final stages.",
                 "Please do not believe any fake information regarding the virus, please consult your doctor for any more information",
                 "To reopen cities are unsafe unless you have to follow social distancing guidelines",
                 "To properly wear a mask, make sure your nose is covered. Do not touch the outside of the mask"]

def greeting_response(text):
  text = text.lower()

  #bots greeting response
  bot_greetings = ['howdy','hi','hey','hello','hola']
  #user greeting
  user_greetings = ['hi','hey','hello','hola','wassup']
  for word in text.split():
    if word in user_greetings:
      return random.choice(bot_greetings)


def index_sort(list_var):
    length = len(list_var)
    list_index = list(range(0, length))

    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                # swap
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp

    return list_index

def bot_response(user_input):
    user_input = user_input.lower()
    sentence_list.append(user_input)
    bot_response = ''
    cm = CountVectorizer().fit_transform(sentence_list)
    similarity_scores = cosine_similarity(cm[-1], cm)
    similarity_scores_list = similarity_scores.flatten()
    index = index_sort(similarity_scores_list)
    index = index[1:]
    response_flag = 0

    j = 0
    for i in range(len(index)):
        if similarity_scores_list[index[i]] > 0.0:
            bot_response = bot_response + ' ' + sentence_list[index[i]]
            response_flag = 1
            j = j + 1

        if j > 0:
            break

    if response_flag == 0:
        bot_response = bot_response + ' ' + "I'm sorry I do not understand what you mean"

    sentence_list.remove(user_input)

    return bot_response

from tkinter import *
root = Tk()
exit_list = ['exit','see you later', 'bye', 'quit', 'break']
def sendMessage():
    user_input = messageWindow.get("1.0","end")
    chatWindow.insert(END,"You:"+user_input)
    messageWindow.delete("1.0",END)
    if user_input.lower() in exit_list:
        chatWindow.insert(END,'CovBot: Will chat with you later'+'\n')
    else:
        if greeting_response(user_input) != None:
            chatWindow.insert(END, "CovBot:" + greeting_response(user_input)+'\n')
        else:
            chatWindow.insert(END, 'CovBot:' + bot_response(user_input)+'\n')


root.title("CovBot '20: Covid-19 chatbot")
root.geometry("700x500")
root.resizable(width=FALSE, height=FALSE)

chatWindow = Text(root, bd=1, bg="#ececec",  width="50", height="8", font=("Arial", 10), foreground="black")
chatWindow.place(x=6,y=6, height=385, width=650)
messageWindow = Text(root, bd=0, bg="white",width="30", height="4", font=("Arial", 10), foreground="black")
messageWindow.place(x=6, y=400, height=88, width=400)
scrollbar = Scrollbar(root, command=chatWindow.yview, cursor="star")
scrollbar.place(x=660,y=5, height=385)

Button = Button(root, text="Send",  width="12", height=5,
                    bd=0, bg="green", activebackground="#00bfff",foreground='#ffffff',font=("Arial", 12), command=sendMessage) 
Button.place(x=500, y=400, height=88)
chatWindow.insert(END,"CovBot: Hello, I'm CovBot! I can answer any of your doubts related to Covid-19 \n")
root.mainloop()
