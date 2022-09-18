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
    
    mm = driver.find_element(By.XPATH,"//body/div[2]/div[1]/div[2]/div/div[1]/div[2]/div[1]/div")
    if(mm.get_attribute("textContent").strip()[:20] == "Official Matchmaking"):
        players =  driver.find_elements( By.CLASS_NAME, 'player-link')
        match = []
        for player in players:

            playerstats = {}
            playerstats["Match ID"] = matchID
            playerstats["Player ID"] = player.get_attribute('href')[-17:-1]

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
            teamScore = player.find_element(By.XPATH,"./..")
            teamScore = teamScore.find_element(By.XPATH,"./..")
            teamScore = teamScore.find_element(By.XPATH,"./..")
            
            #teamScore = teamScore.find_element(By.ID,'match-scoreboard')
            #teamScore = teamScore.find_element(By.CLASS_NAME,'scoreboard')
            
            playerstats["Team"] = teamScore.find_element(By.XPATH, "./tr/td/div").get_attribute("textContent").strip() [-1:]

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
        
            # print(stats["team"])
            match.append(playerstats)
        return match
        
    else :
        return []


def multiFetch(offset,nb,driver):
    
    columns = ['Match ID', 'Player ID', 'Rank', 'Rank Gain', 'Team', 'K', 'D', 'A',
        '+/-', 'K/D', 'ADR', 'HS%', 'KAST', 'Rating', 'EF', 'FA', 'EBT', 'UD',
        'FKD', 'FK', 'FD', 'FK as T', 'FD as T', 'FK as CT', 'FD as CT',
        'Trade K', 'Trade D', 'Trade FK', 'Trade FD', 'Trade FK as T',
        'Trade FD as T', 'Trade FK as CT', 'Trade FD as CT', '1vX', '1v5',
        '1v4', '1v3', '1v2', '1v1', '3K+', '5K', '4K', '3K', '2K', '1K']
    df = pd.DataFrame(columns= columns)

    # frame = []

    

    # driver.implicitly_wait(0.1)
    # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    for i in range(nb):
        res = fetchMatch((offset + i),driver)
        # sleep(1)
        # print(res)
        df = pd.concat([pd.DataFrame(res,columns= columns),df])
        # driver.execute_script("window.open();")
        # driver.close()
        # driver.switch_to.window(driver.window_handles[-1])
        

    driver.quit()

    df.to_csv("matches"+str(offset)+".csv")
    # print(frame)
    # df = pd.concat(frame)
    # display(df)
    # return df

def testing(offset):
    print(offset,os.getpid())


if __name__ == '__main__':

    columns = ['Match ID', 'Player ID', 'Rank', 'Rank Gain', 'Team', 'K', 'D', 'A',
            '+/-', 'K/D', 'ADR', 'HS%', 'KAST', 'Rating', 'EF', 'FA', 'EBT', 'UD',
            'FKD', 'FK', 'FD', 'FK as T', 'FD as T', 'FK as CT', 'FD as CT',
            'Trade K', 'Trade D', 'Trade FK', 'Trade FD', 'Trade FK as T',
            'Trade FD as T', 'Trade FK as CT', 'Trade FD as CT', '1vX', '1v5',
            '1v4', '1v3', '1v2', '1v1', '3K+', '5K', '4K', '3K', '2K', '1K']
            
    df = pd.DataFrame(columns= columns)

    offset = int(sys.argv[1])
    print(offset)
    step = int(sys.argv[2])
    print(step)
    nb = int(sys.argv[3])
    print(nb)

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