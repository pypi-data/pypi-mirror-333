from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from datetime import timedelta
import pandas as pd
from tqdm import tqdm
import urllib.parse
from sentence_transformers import SentenceTransformer
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from openai import OpenAI
import matplotlib.pyplot as plt
import tiktoken

def data (url):
    options = webdriver.ChromeOptions()
    options.add_argument("--lang=en-GB")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    driver.get(url)

    if 'consent.google.com' in driver.current_url:
        driver.execute_script('document.getElementsByTagName("form")[0].submit()');

        
    time.sleep(5)
    reviews_tab = driver.find_element(By.XPATH, "//button[@role='tab' and contains(@aria-label, 'Reviews')]").click()
    time.sleep(5)
        
    scrollable_div = driver.find_element(By.CSS_SELECTOR, '#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde')

    initial_reviews = len(driver.find_elements(By.CLASS_NAME, "jftiEf"))
    temp_c = 2

    while True:
        for _ in range(temp_c):
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
            time.sleep(3)
            
        temp_c = 1    
        updated_reviews = len(driver.find_elements(By.CLASS_NAME, "jftiEf"))
        
        if updated_reviews == initial_reviews:
            break
            
        initial_reviews = updated_reviews
        time.sleep(3)

    more_elements = driver.find_elements(By.CLASS_NAME, "w8nwRe")

    for button in more_elements:
        button.click()

    time.sleep(10)
    
    reviews = [element for element in driver.find_elements(By.CLASS_NAME, "jftiEf")]
    
    texts = []
    names = []
    stars = []
    dates = []
    
    for element in reviews:
        try:
            texts.append(element.find_element(By.CLASS_NAME, "wiI7pd").text)
            names.append(element.find_element(By.CLASS_NAME, "d4r55 ").text)
            stars.append(int(element.find_element(By.CLASS_NAME, "kvMYJc").get_attribute("aria-label").split()[0]))
            dates.append(element.find_element(By.CLASS_NAME, "rsqaWe").text)
        except:
            continue
    
    return texts, names, stars, dates

    
def outputs(texts, names, stars, dates):
    
    df = pd.DataFrame({
        "Full_Name": names,
        "Review": texts,
        "Stars": stars,
        "Date": dates
    })
    
    df["Review"] = df["Review"].apply(lambda x: x.replace("\n", " ")) #Removes new lines

    return df
    
    
def sentiment_analysis(sentiment_model_name, df, download_destination_folder):
    tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)
    model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_name)
   
    
    for index, row in tqdm(df.iterrows(), total=len(df)):
      inputs = tokenizer(row["Review"], return_tensors="pt", padding="max_length", truncation=True, max_length=512)
      with torch.no_grad():
        logits = model(**inputs).logits

      df.at[index, "sentiment_score"] = float(f"{max(torch.nn.functional.softmax(logits, dim=-1).squeeze().tolist())*100:.2f}")
      df.at[index, "sentiment_output"] = model.config.id2label[logits.argmax().item()].lower()
        
    negative_reviews = []
    positive_reviews = []
    neutral_reviews = []

    for i,r in df.iterrows():
      if r["sentiment_output"] == "negative":
        negative_reviews.append(r["Review"])
      elif r["sentiment_output"] == "positive":
        positive_reviews.append(r["Review"])
      else:
        neutral_reviews.append(r["Review"])
    
    df.to_csv(download_destination_folder+"/Extracted_reviews.csv", index=False, encoding="utf-8")
        
    return positive_reviews, negative_reviews, neutral_reviews
    

def llm_response(api_token, negative_reviews):
    endpoint = "https://models.inference.ai.azure.com"
    model_name = "gpt-4o"
    client = OpenAI(base_url=endpoint,api_key=api_token)
    
    if negative_reviews != []:
      negative_reviews_text = "; ".join(negative_reviews)
      encoding = tiktoken.encoding_for_model("gpt-4o")
      tokens = encoding.encode(negative_reviews_text)
      
      if len(tokens) > 8000:
        tokens = tokens[:6600] #Truncate to ~6K tokens
        negative_reviews_text = encoding.decode(tokens)
        
      response = client.chat.completions.create(
          messages=[
              {
                  "role": "system",
                  "content": """
                              You are a review expert analyst. Given a list of negative reviews seperated by (;), your job is to:

                              Summarize the main issues mentioned in the reviews.
                              Identify and list the top problems/negative characteristics based on their frequency of occurrence.
                              For each problem, indicate the number of times it appears across the reviews.

                              Output Format:

                              Provide a list of the top 5 problems in the following format:
                              1. Bad food (18)
                              2. Rude customer serivce (2)
                              3. Overpriced (5)
                              4. Long queue (1)
                              5. Small portions (7)

                              Note:

                              Focus on identifying recurring problems that are frequently mentioned in the reviews.
                              Return only the list, with no additional explanation or context.
                              """
              },
              {
                  "role": "user",
                  "content": f"{negative_reviews_text}"
              }
          ],
          temperature=1.0,
          top_p=1.0,
          max_tokens=1000,
          model=model_name
      )

      negative_categories = response.choices[0].message.content.splitlines()
      
      negative_topics = []
      for i in negative_categories:
         topic = i.strip().split(".", 1)[-1].rsplit(" ", 1)[0].strip()
         number_of_topic = int(i.strip().rsplit(" ", 1)[-1][1:-1])
         negative_topics.append((topic,number_of_topic))
         
      negative_topics.sort(key=lambda tup: tup[1], reverse=False)
      return negative_topics
      
    else:
      return False
      
      
def first_plot(positive_reviews, negative_reviews, neutral_reviews, df, sentiment_model_name, download_destination_folder):
    labels = ["Positive reviews", "Negative reviews", "Neutral reviews"]
    amount_of_reviews = [len(positive_reviews), len(negative_reviews), len(neutral_reviews)]
    colors = ["green", "red", "gray"]

    plt.figure(figsize=(10, 6))

    bars = plt.bar(labels, amount_of_reviews, color=colors, edgecolor="black", zorder=3)
    plt.bar_label(bars, [f"{(len(positive_reviews)/len(df))*100:.2f}%", f"{(len(negative_reviews)/len(df))*100:.2f}%", f"{(len(neutral_reviews)/len(df))*100:.2f}%"], padding=1, color='black',
                 fontsize=11, label_type='edge', fontweight='bold')
    plt.legend(bars, [f"{len(positive_reviews)} reviews", f"{len(negative_reviews)} reviews", f"{len(neutral_reviews)} reviews"], title="Review Categories")
    plt.title(f"Summary of sentiment analysis using '{sentiment_model_name}'", fontweight="bold")
    plt.xlabel('Categories', fontweight="bold")
    plt.ylabel('Number of reviews', fontweight="bold")
    plt.grid(zorder=0)
    plt.savefig(download_destination_folder+"/1_Plot.png", format="png", dpi=600, bbox_inches='tight')
    
    
def second_plot(negative_topics, download_destination_folder):
    categories = [i[0] for i in negative_topics]
    frequnecy = [i[1] for i in negative_topics]
    colors = ['orange' if i >= (sum(frequnecy)/len(frequnecy)) else 'gray' for i in frequnecy]

    plt.figure(figsize=(10, 6))

    bars = plt.barh(categories, frequnecy, color=colors, edgecolor="black", zorder=3)
    plt.axvline(x=(sum(frequnecy)/len(frequnecy)), color='red', linestyle='--', linewidth=2, zorder=2)
    plt.bar_label(bars, [f"{(f / sum(frequnecy)) * 100:.2f}%" for f in frequnecy], padding=-55, color='white',
                 fontsize=12, label_type='edge', fontweight='bold')
    plt.text(x=(sum(frequnecy)/len(frequnecy)), y=0, s='Average frequency', ha='center',
            fontsize=12, bbox=dict(facecolor='white', edgecolor='red', ls='--'))

    plt.title(f"Summary of negative analysis reviews using 'GPT-4o'", fontweight="bold")
    plt.xlabel('Frequnecies', fontweight="bold")
    plt.ylabel('Categories', fontweight="bold")
    plt.grid(zorder=0)
    plt.savefig(download_destination_folder+"/2_Plot.png", format="png", dpi=600, bbox_inches='tight')

    
def sentiment_review_analysis(api_token, url, sentiment_model_name, download_destination_folder):
    if api_token=="" or url=="" or sentiment_model_name=="" or download_destination_folder=="":
        raise ValueError("Please fill all the variables")
    if not url.startswith("https://www.google.com/maps/place/"):
        raise ValueError("Please make sure that the url starts with 'https://www.google.com/maps/place/'")
    if sentiment_model_name != "cardiffnlp/twitter-roberta-base-sentiment-latest" and sentiment_model_name != "cardiffnlp/twitter-xlm-roberta-base-sentiment":
        raise ValueError("Please make sure that the 'sentiment_model_name' is either 'cardiffnlp/twitter-roberta-base-sentiment-latest' or 'cardiffnlp/twitter-xlm-roberta-base-sentiment'")
    print("Please wait while the data is being processed... (Around 10 minutes)")
    texts, names, stars, dates = data(url)
    df = outputs(texts, names, stars, dates)
    positive_reviews, negative_reviews, neutral_reviews = sentiment_analysis(sentiment_model_name, df, download_destination_folder)
    negative_topics = llm_response(api_token, negative_reviews)
    if negative_topics:
        first_plot(positive_reviews, negative_reviews, neutral_reviews, df, sentiment_model_name, download_destination_folder)
        second_plot(negative_topics, download_destination_folder)
        print("Analysis complete, check your download files for the results.")
    else:
        print("No negative reviews found by the sentiment model, please try another model.")
        
 
