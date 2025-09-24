import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# --- SELETORES (ATUALIZE AQUI SE O SITE MUDAR) ---
HOME_LINK_SELECTOR = (By.XPATH, '//a[@data-testid="AppTabBar_Home_Link"]')
POST_CONTAINER_SELECTOR = (By.XPATH, "//article[@data-testid='tweet']")
POST_TEXT_SELECTOR = (By.XPATH, ".//div[@data-testid='tweetText']")
POST_LINK_SELECTOR = (By.XPATH, './/a[contains(@href, "/status/")]')
COMMENT_SELECTOR = (By.XPATH, "//article[@data-testid='tweet']//div[@data-testid='tweetText']") # <<< LINHA ATUALIZADA


def start_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_window_size(1280, 1024)
    return driver

def login_and_wait(driver, wait_time=120):
    print("Abrindo tela de login do X... Por favor, faça o login manualmente.")
    driver.get("https://x.com/i/flow/login")
    try:
        WebDriverWait(driver, wait_time).until(EC.presence_of_element_located(HOME_LINK_SELECTOR))
        print("Login detectado com sucesso! Continuando...")
        return True
    except TimeoutException:
        print(f"ATENÇÃO: Login não detectado após {wait_time} segundos. O script pode falhar.")
        return False

def collect_comments_from_post_page(driver, max_comments=50):
    """Coleta comentários da página de um post individual."""
    comments = []
    seen_comments = set()
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    print("  Coletando comentários...")
    while len(comments) < max_comments:
        try:
            # Espera os elementos de comentário carregarem
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(COMMENT_SELECTOR))
            replies = driver.find_elements(*COMMENT_SELECTOR)
            
            for reply in replies:
                comment_text = reply.text
                if comment_text and comment_text not in seen_comments:
                    comments.append(comment_text)
                    seen_comments.add(comment_text)
                    if len(comments) >= max_comments:
                        break
            
            if len(comments) >= max_comments:
                break

            # Rolagem para carregar mais comentários
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2) # Pausa para carregamento
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("  Fim da página de comentários.")
                break
            last_height = new_height
        except TimeoutException:
            print("  Nenhum comentário encontrado ou o tempo de espera esgotou.")
            break
            
    print(f"  {len(comments)} comentários coletados.")
    return comments

def collect_last_posts_with_comments(driver, profile, limit=30):
    url = f"https://x.com/{profile.lstrip('@')}"
    print(f"Navegando para o perfil: {url}")
    driver.get(url)

    post_links = []
    seen_links = set()
    
    # 1. Coletar os links de todos os posts primeiro
    print("Coletando links dos posts...")
    while len(post_links) < limit:
        try:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located(POST_CONTAINER_SELECTOR))
            posts_on_page = driver.find_elements(*POST_CONTAINER_SELECTOR)
            
            for post in posts_on_page:
                try:
                    link_element = post.find_element(*POST_LINK_SELECTOR)
                    post_url = link_element.get_attribute("href")
                    if post_url not in seen_links:
                        post_links.append(post_url)
                        seen_links.add(post_url)
                        if len(post_links) >= limit:
                            break
                except NoSuchElementException:
                    continue
            
            if len(post_links) >= limit:
                break

            last_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("Fim da página do perfil alcançado.")
                break
        except TimeoutException:
            print("Tempo esgotado ao procurar posts no perfil.")
            break

    # 2. Visitar cada link para coletar dados do post e comentários
    posts_data = []
    print(f"\nIniciando coleta detalhada de {len(post_links)} posts...")
    for i, link in enumerate(post_links):
        print(f"Processando Post {i+1}/{len(post_links)}: {link}")
        driver.get(link)
        try:
            # Espera o post principal carregar
            WebDriverWait(driver, 15).until(EC.presence_of_element_located(POST_TEXT_SELECTOR))
            post_text_element = driver.find_element(*POST_TEXT_SELECTOR)
            post_text = post_text_element.text
            
            # Coleta os comentários
            comments = collect_comments_from_post_page(driver)
            
            posts_data.append({
                "codigo": link.split("/")[-1],
                "texto_post": post_text,
                "comentarios": comments
            })
        except TimeoutException:
            print(f"  Não foi possível carregar o conteúdo do post: {link}")
            continue
            
    print(f"\nColeta finalizada. Total de {len(posts_data)} posts com comentários foram processados.")
    return posts_data