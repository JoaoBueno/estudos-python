from kivy.uix.widget import Widget
from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen

# Carrega a configuração
Config.read("config.ini")

# Gerenciador de telas
screen_manager = ScreenManager()

# Criação das telas
tela_1 = Screen(name='Tela 1')
tela_2 = Screen(name='Tela 2')

# Declara a Tela do Vencedor 1
class TelaVencedor1(Screen):
    pass

# Adiciona as telas ao ScreenManager
screen_manager.add_widget(tela_1)
screen_manager.add_widget(tela_2)

# Por padrão, a primeira tela adicionada será aquela mostrada pelo gerenciador.
# Para mudar para, por exemplo, a tela 2, utilizamos o parâmetro name:
screen_manager.current = 'Tela 2'

# Nesse momento, a Tela 2 será mostrada!

class Pong(Widget):
    pass

class PongApp(App):
    def build(self):
        return Pong()

if __name__ == '__main__':
    PongApp().run()