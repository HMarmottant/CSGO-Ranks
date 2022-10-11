import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import undetected_chromedriver
import pandas as pd
from time import sleep
from threading import Thread, Barrier
import os

def fetchMatch(matchID, driver):
    driver.get("https://csgostats.gg/match/" + str(matchID))
    
    mm = driver.find_elements(By.XPATH,"//body/div[2]/div[1]/div[2]/div/div[1]/div[2]/div[1]/div")

    macthdate =  driver.find_elements( By.CLASS_NAME, 'match-date-text')
    if(macthdate.__len__()):
        macthdate = macthdate[0].get_attribute("textContent").strip()
        
    if((mm.__len__() >= 1) and (mm[0].get_attribute("textContent").strip()[:20] == "Official Matchmaking")):
        players =  driver.find_elements( By.CLASS_NAME, 'player-link')
        match = []
        for player in players:

            playerstats = {}
            playerstats["Match ID"] = matchID
            playerstats["Match Date"] = macthdate
            playerstats["Player ID"] = player.get_attribute('href')[-17:]


            PCard = player.find_element(By.XPATH,"./..").find_element(By.XPATH,"./..")

            rank = PCard.find_elements(By.CLASS_NAME, "rank")

            if rank.__len__():
                playerstats["Rank"] = (rank[0].get_attribute("src"))[-6:-4].strip("/")

            rankupicon = PCard.find_elements(By.XPATH, "./td/div/div/span")

            if(rankupicon.__len__()):
                rankup = rankupicon[0].get_attribute("class")
                if rankup == "glyphicon glyphicon-chevron-up" :
                    playerstats["Rank Gain"] = 1

                elif rankup == "glyphicon glyphicon-chevron-down" :
                    playerstats["Rank Gain"] = -1

            else :
                playerstats["Rank Gain"] = 0        
            
            # print(stats["rank gain"])
            # teamScore = player.find_element(By.XPATH,"./..")
            # teamScore = teamScore.find_element(By.XPATH,"./..")
            team = PCard.find_element(By.XPATH,"./..")
            
            #teamScore = teamScore.find_element(By.ID,'match-scoreboard')
            #teamScore = teamScore.find_element(By.CLASS_NAME,'scoreboard')
            
            playerstats["Team"] = team.find_element(By.XPATH, "./tr/td/div").get_attribute("textContent").strip() [-1:]

            teams = team.find_element(By.XPATH,"./..")

            scores = teams.find_elements(By.XPATH, "./tbody/tr/td/div[2]")

            playerstats["Team 1 Score"] = scores[0].get_attribute("textContent").strip()
            playerstats["Team 2 Score"] = scores[1].get_attribute("textContent").strip()

            stats = PCard.find_elements(By.TAG_NAME, "td")

            # for stat in stats:
            #     print(stat.get_attribute("data-collapse"),stat.get_attribute("textContent").strip() )

            playerstats["K"] =                  stats[2].get_attribute("textContent").strip()
            playerstats["D"] =                  stats[3].get_attribute("textContent").strip()  
            playerstats["A"] =                  stats[4].get_attribute("textContent").strip()  
            playerstats["+/-"] =                stats[5].get_attribute("textContent").strip()  
            playerstats["K/D"] =                stats[6].get_attribute("textContent").strip()  
            playerstats["ADR"] =                stats[7].get_attribute("textContent").strip()  
            playerstats["HS%"] =                stats[8].get_attribute("textContent").strip()  
            playerstats["KAST"] =               stats[9].get_attribute("textContent").strip()  
            playerstats["Rating"] =             stats[10].get_attribute("textContent").strip()  
            playerstats["EF"] =                 stats[11].get_attribute("textContent").strip()  
            playerstats["FA"] =                 stats[12].get_attribute("textContent").strip()  
            playerstats["EBT"] =                stats[13].get_attribute("textContent").strip()  
            playerstats["UD"] =                 stats[14].get_attribute("textContent").strip()  
            playerstats["FKD"] =                stats[15].get_attribute("textContent").strip()  
            playerstats["FK"] =                 stats[16].get_attribute("textContent").strip() 
            playerstats["FD"] =                 stats[17].get_attribute("textContent").strip() 
            playerstats["FK as T"] =            stats[18].get_attribute("textContent").strip()  
            playerstats["FD as T"] =            stats[19].get_attribute("textContent").strip()  
            playerstats["FK as CT"] =           stats[20].get_attribute("textContent").strip()  
            playerstats["FD as CT"] =           stats[21].get_attribute("textContent").strip()  
            playerstats["Trade K"] =            stats[22].get_attribute("textContent").strip()  
            playerstats["Trade D"] =            stats[23].get_attribute("textContent").strip()  
            playerstats["Trade FK"] =           stats[24].get_attribute("textContent").strip()  
            playerstats["Trade FD"] =           stats[25].get_attribute("textContent").strip()  
            playerstats["Trade FK as T"] =      stats[26].get_attribute("textContent").strip()  
            playerstats["Trade FD as T"] =      stats[27].get_attribute("textContent").strip()  
            playerstats["Trade FK as CT"] =     stats[28].get_attribute("textContent").strip()  
            playerstats["Trade FD as CT"] =     stats[29].get_attribute("textContent").strip()  
            playerstats["1vX"] =                stats[30].get_attribute("textContent").strip()  
            playerstats["1v5"] =                stats[31].get_attribute("textContent").strip()  
            playerstats["1v4"] =                stats[32].get_attribute("textContent").strip()  
            playerstats["1v3"] =                stats[33].get_attribute("textContent").strip()  
            playerstats["1v2"] =                stats[34].get_attribute("textContent").strip()  
            playerstats["1v1"] =                stats[35].get_attribute("textContent").strip()  
            playerstats["3K+"] =                stats[36].get_attribute("textContent").strip()  
            playerstats["5K"] =                 stats[37].get_attribute("textContent").strip()  
            playerstats["4K"] =                 stats[38].get_attribute("textContent").strip()  
            playerstats["3K"] =                 stats[39].get_attribute("textContent").strip()  
            playerstats["2K"] =                 stats[40].get_attribute("textContent").strip()  
            playerstats["1K"] =                 stats[41].get_attribute("textContent").strip()  
        
            # print(playerstats["Team Score"])
            match.append(playerstats)
        return match
        
    else :
        return []


def multiFetch(offset,nb,driver):
    
    df = pd.DataFrame()

    # frame = []

    

    # driver.implicitly_wait(0.1)
    # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    for i in range(nb):
        res = fetchMatch((offset + i),driver)
        # sleep(1)
        # print(res)
        df = pd.concat([pd.DataFrame(res),df])
        # driver.execute_script("window.open();")
        # driver.close()
        # driver.switch_to.window(driver.window_handles[-1])
        if((i != 0) and (i%100 == 0)):
            df.to_csv("./matches/matches"+str(offset + i)+".csv")
            df = pd.DataFrame()

        
    driver.quit()

    df.to_csv("./matches/matchesrest"+str(offset + nb)+".csv")

    # print(frame)
    # df = pd.concat(frame)
    # display(df)
    # return df

def testing(offset):
    print(offset,os.getpid())


if __name__ == '__main__':
            
    # df = pd.DataFrame()

    offset = int(sys.argv[1])
    # print(offset)
    step = int(sys.argv[2])
    # print(step)
    nb = int(sys.argv[3])
    # print(nb)

    print(offset + (nb*step),step)

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    driver = undetected_chromedriver.Chrome(options= options)

    multiFetch(offset + (nb*step),step,driver)

    # nb = 10

    # nbarray = []

    # for i in range(0,nb * os.cpu_count()-1,nb):
    #     nbarray.append(i + 79000000)

    # print(nbarray)


    # number_of_threads = 5

    # barrier = Barrier(number_of_threads)

    # threads = []

    # for i in range(number_of_threads):
    #     options = webdriver.ChromeOptions()
    #     # options.add_argument("--headless")
    #     driver = undetected_chromedriver.Chrome(options= options)

    #     # print("here")

    #     t = Thread(target=multiFetch(nbarray[i],nb,driver),daemon= True) 
    #     t.start()
    #     threads.append(t)

    # for t in threads:
    #     t.join()

    # print(df)
    # df.to_csv("test.csv")