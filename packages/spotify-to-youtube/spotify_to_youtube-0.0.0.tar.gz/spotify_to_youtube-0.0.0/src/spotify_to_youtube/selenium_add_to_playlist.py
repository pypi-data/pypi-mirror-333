from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import os
import re
import time
import urllib.parse

class AddSongsToPlaylist():
    def __init__(self, profile, executable_path):
        # Set up selenium driver
        opts = Options()
        opts.add_argument("-profile")
        opts.add_argument(profile)
        opts.headless = True
        service = FirefoxService(executable_path=executable_path, service_args=["--marionette-port", "2828"])

        # # os.environ['MOZ_HEADLESS'] = '0'
        # os.environ.pop("MOZ_HEADLESS")
        self.driver = webdriver.Firefox(
            service=service,
            options=opts
        )


    # def search_and_add_video_to_playlist(self, title, artist, playlist):
    #     # Search for song directly using youtube URL format
    #     self.driver.get(f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(title)}+{urllib.parse.quote_plus(artist)}")

    #     # Find video
    #     time.sleep(0.1)
    #     video = WebDriverWait(self.driver, 3).until(
    #         EC.presence_of_element_located((By.XPATH, '//*[@aria-label="Action menu"]')) #Improved XPATH
    #     );
    #     video.click()

    #     # Find save button
    #     # time.sleep(5);
    #     save = WebDriverWait(self.driver, 3).until(
    #         EC.presence_of_element_located((By.XPATH, "//yt-formatted-string[contains(text(), 'Save to playlist')]"))
    #     )
    #     save.click()

    #     # Find playlist text first then find playlist checkbox
    #     playlist_title_element = WebDriverWait(self.driver, 3).until(
    #         EC.presence_of_element_located((By.XPATH, f'//*[@title="{playlist}"]'))
    #     )
    #     playlist_parent = playlist_title_element.find_element(By.XPATH, './../../../..')
    #     print(playlist_parent.get_attribute("id"))

    #     playlist_checkbox = playlist_parent.find_element(By.ID, "checkboxContainer")
    #     print(playlist_checkbox.get_attribute("class"))
    #     playlist_checkbox.click()


    def create_playlist_search_and_add_video_to_playlist(self, title, artist, playlist):
        # Search for song directly using youtube URL format
        self.driver.get(f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(title)}+{urllib.parse.quote_plus(artist)}")

        # Find video
        # print(self.driver.execute_script("return document.readyState"))
        # while (self.driver.execute_script("return document.readyState") != "complete"):
        #     # print(self.driver.execute_script("return document.readyState"))
        #     continue 
        
        # try:
        #     video_filter = WebDriverWait(self.driver, 5).until(
        #         EC.visibility_of_element_located((By.XPATH, '//*[@title="Videos"]'))
        #     )
        #     video_filter.click()
        # except (NoSuchElementException, TimeoutException):
        #     pass

        time.sleep(1)
        video = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@aria-label="Action menu"]')) #Improved XPATH
        )
        video.click()

        # Find save button
        save = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//yt-formatted-string[contains(text(), 'Save to playlist')]"))
        )
        save.click()

        try:
            # Find playlist text first then find playlist checkbox
            playlist_title_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//*[@title="{playlist}"]'))
            )
            playlist_parent = playlist_title_element.find_element(By.XPATH, './../../../..')

            playlist_checkbox = playlist_parent.find_element(By.ID, "checkboxContainer")

            playlist_checkbox.click()
        except (NoSuchElementException, TimeoutException):
            # Find new playlist button
            new_playlist = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@aria-label='New playlist']"))
            )
            new_playlist.click()

            # Fill playlist name 
            playlist_textarea = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//textarea[@placeholder='Choose a title']"))
            )
            playlist_textarea.send_keys(playlist)

            # Find create button
            buttons = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//*[contains(text(), 'Create')]"))
            )
            create = buttons[2].find_element(By.XPATH, "./../../..")
            create.click()  
        return
    

    def find_playlist(self, playlist_name):
        self.driver.get("https://www.youtube.com/feed/playlists")
        contents = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='contents']"))
        )

        playlists = contents.find_elements(By.XPATH, "ytd-rich-item-renderer")

        # Check if user's current playlists contains a playlist called playlist_name
        for playlist in playlists:
            title = WebDriverWait(playlist, 5).until(
                EC.presence_of_element_located((By.XPATH, ".//yt-lockup-metadata-view-model//span"))
            )

            if title.text == playlist_name:
                link = WebDriverWait(playlist, 5).until(
                    EC.presence_of_element_located((By.XPATH, ".//yt-lockup-view-model//a[@href]"))
                )
                return link.get_attribute('href')

        return -1
    
    def find_title_of_video(self, video):
        title = WebDriverWait(video, 5).until(
            EC.visibility_of_element_located((By.XPATH, ".//a[@id='video-title']"))
        )

        return title.get_attribute("title")


    def get_all_songs_in_playlist(self, playlist_name):
        URL = self.find_playlist(playlist_name)
        
        if URL == -1:
            return []
        
        # Extract playlist link using regex
        list_id = re.search(r"&list=(.+?)&", URL) # use .group(n) to extract
        
        self.driver.get(f"https://www.youtube.com/playlist?list={list_id.group(1)}")

        contents = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//ytd-item-section-renderer//ytd-playlist-video-list-renderer/div[@id='contents']/ytd-playlist-video-renderer"))
        )

        titles = []
        # Loop over all video elements in contents
        for video in contents:
            title = self.find_title_of_video(video)
            titles.append(title)
        
        print(titles)
        return titles 
 

    def quit(self):
        self.driver.quit()

