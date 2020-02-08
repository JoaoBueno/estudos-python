#coding: utf-8
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from sys import argv


class Pagina(object):
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.packtpub.com/packt/offers/free-learning?from=block"
        self.sing_in = "/html/body/div[7]/div[2]/div[1]/div[1]/div/div[1]/div[4]/a[1]/div"
        self.username = 'email'
        self.password = 'password'
        self.botao_login = 'edit-submit-1'
        self.botao_dowload = '//*[@id="free-learning-claim"]'

    def navegar(self):
        self.driver.get(self.url)

    def login(self, _email="None", _senha="None"):
        self.driver.find_element_by_xpath(self.sing_in).click()

        for tentativa_email in self.driver.find_elements_by_id(self.username):
            try:
                tentativa_email.send_keys(_email)
            except:
                pass

        for tentavia_senha in self.driver.find_elements_by_id(self.password):
            try:
                tentavia_senha.send_keys(_senha)
            except:
                pass

        for click_botao in self.driver.find_elements_by_id(self.botao_login):
            try:
                click_botao.click()
            except:
                pass

        self.driver.find_element_by_xpath(self.botao_dowload).click()


email_pessoa = input("Digite seu email: ")
senha_pessoa = input("Digite sua senha: ")

navegador = webdriver.Firefox()
pegar_livro = Pagina(navegador)
pegar_livro.navegar()
pegar_livro.login(email_pessoa, senha_pessoa)
