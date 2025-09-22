from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
#para rolar a página
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def start_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_window_size(1200,900)
    return driver

def scroll_page(driver, times=3, pause=2):
    #Rola a página principal para carregar mais postagens.
    for _ in range(times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)

def collect_last_posts_with_comments(driver, profile, limit=30):
    url = f"https://x.com/{profile.lstrip('@')}"
    driver.get(url)
    time.sleep(5) #aguarda a renderização inicial

    #rolagem até carregar posts suficientes
    posts_data = []
    seen = set()
    while len(posts_data) < limit:
        scroll_page(driver, times = 2, pause = 3)

        #localizar blocos de postagens (os seletores podem mudar)
        posts = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
        for post in posts:
            try:
                #captura link do post (com ID único)
                link_el = post.find_element(By.XPATH, './/a[@href and contains(@href,"/status/")]')
                post_url = link_el.get_attribute("href")
                codigo = post_url.split("/")[-1]

                if codigo in seen:
                    continue

                #texto do post
                texto_el = post.find_element(By.XPATH, './/div[@data-testid="tweetText"]')
                texto_post = texto_el.text

                #abrir em nova aba para pegar comentários
                driver.execute_script("window.open(argument[0]);", post_url)
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(4)

                comentarios = collect_comments_from_post(driver)

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

                posts_data.append({
                    "codigo": codigo,
                    "texto_post": texto_post,
                    "comentarios": comentarios
                })
                seen.add(codigo)

                if len(posts_data) >= limit:
                    break
            except Exception as e:
                print("Erro ao coletar um post: ", e)
    return posts_data

def collect_comments_from_post(driver, max_scrolls=5):
    comentarios = []
    for _ in range(max_scrolls):
        scroll_page(driver, times=1, pause=2)
        try:
            replies = driver.find_elements(By.XPATH, '//div[@data-testid="reply"]')
            for r in replies:
                try:
                    texto = r.text.strip()
                    if texto and texto not in comentarios:
                        comentarios.append(texto)
                except:
                    pass
        except:
            pass
    return comentarios
