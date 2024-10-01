import sqlite3
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.config import Config
from datetime import datetime
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView 
from kivymd.uix.card import MDCard
from kivy.clock import Clock
Config.set('graphics', 'orientation', 'portrait')

# Funções de banco de dados
def get():
    data_atual = datetime.now().strftime('%d/%m/%Y') # Formata a data atual como YYYY-MM-DD
    try:
        conn = sqlite3.connect('vendas.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM vendas WHERE data = ?''', (data_atual,))
        vendas = cursor.fetchall()
        return vendas 
    except Exception as e:
        print(f"Erro ao buscar vendas: {e}")
        return "erro no banco."
    finally:
        conn.close()
        
def init_db():
    try:
        conn = sqlite3.connect('vendas.db')
        cursor = conn.cursor()
        

        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL
            )
        ''')
        
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                servico TEXT,
                valor TEXT,
                data TEXT
            )
        ''')
        conn.commit()
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
    finally:
        conn.close()

def insert_user(nome, senha):
    
    
    if len(nome) < 5:
        erro = "Nome muito pequeno, tente novamente."
        return erro
    if len(senha) < 5:
        erro= "senha muito pequena, tente novamente."
        return erro
    
    try:
        conn = sqlite3.connect('vendas.db')
        cursor = conn.cursor()
        cursor.execute(''' 
            INSERT INTO usuarios (nome, senha) VALUES (?, ?)
        ''', (nome, senha))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Usuário já existe")
    except Exception as e:
        print(f"Erro ao inserir usuário: {e}")
    finally:
        conn.close()
        
    return erro

def verify_login(nome, senha):
    conn = sqlite3.connect('vendas.db')
    cursor = conn.cursor()
    cursor.execute(''' 
        SELECT * FROM usuarios WHERE nome = ? AND senha = ?
    ''', (nome, senha))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def anotv(nome, servico, valor ):
    data = datetime.now().strftime('%d/%m/%Y') 
    conn = sqlite3.connect('vendas.db')
    cursor = conn.cursor()
    cursor.execute(''' 
        INSERT INTO vendas (nome, servico, valor, data)
        VALUES (?, ?, ?, ?)
    ''', (nome, servico, valor, data))
    conn.commit()
    conn.close()

class Cadastro(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.build_ui()
        self.add_widget(self.layout)
        
    def go_back(self, instance):
        self.manager.current = 'login'
        
    def build_ui(self):
        self.layout.canvas.before.clear()
        with self.layout.canvas.before:
            Color(1, 1, 1, 1)  # Branco
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)

        label_wel = MDLabel(
            text='CADASTRO',
            halign='center',
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )
        self.layout.add_widget(label_wel)

        self.username = MDTextField(
            hint_text='Nome',
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            multiline=False
        )
        self.layout.add_widget(self.username)

        self.passw = MDTextField(
            hint_text='Senha',
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            multiline=False,
            password=True
        )
        self.layout.add_widget(self.passw)

        submit_button = MDRaisedButton(
            text='Cadastrar',
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            on_press=self.submit
        )
        self.layout.add_widget(submit_button)
        
        back_button = MDRaisedButton(
            text='Voltar',
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.27},
            on_press=self.go_back
        )
        self.add_widget(back_button)

    def submit(self, instance):
        
        erro = insert_user(self.username.text, self.passw.text)
        if erro:  # Se erro for diferente de None, houve um erro
            aviso = MDLabel(
            color="red",
            text=erro,  # Exibir a mensagem de erro específica
            halign='center',
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        self.username.text = ''
        self.passw.text = ''
        
        Clock.schedule_once(lambda dt: self.remove_widget(aviso), 2)
        
        return self.add_widget(aviso)


class Logins(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def build(self):
        layout = FloatLayout()

        label_wel = MDLabel(
            text='LOGIN',
            halign='center',
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )
        layout.add_widget(label_wel)

        self.username_input = MDTextField(
            hint_text='Nome',
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            multiline=False
        )
        layout.add_widget(self.username_input)

        self.password_input = MDTextField(
            hint_text='Senha',
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            multiline=False,
            password=True
        )
        layout.add_widget(self.password_input)

        but = MDRaisedButton(
            text='ENTRAR',
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            on_press=self.login
        )
        layout.add_widget(but)

        self.add_widget(layout)

    def login(self, instance):
        nome = self.username_input.text
        
        senha = self.password_input.text
        
        
        
        if nome == "adm":
            self.manager.current = "Cadastro"
        if verify_login(nome, senha):
            self.manager.current = 'nvendas'
        else:
            print("Nome ou senha incorretos")

class nvendas(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.build_ui()
        self.add_widget(self.layout)
    def go_res(self, instance):
        self.manager.current = 'resum'

    def build_ui(self):
        self.layout.canvas.before.clear()
        with self.layout.canvas.before:
            Color(1, 1, 1, 1)  # Branco
            self.rect = Rectangle(size=self.layout.size, pos=self.layout.pos)

        label_wel = MDLabel(
            text='VENDAS',
            halign='center',
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.9}
        )
        self.layout.add_widget(label_wel)

        self.input_nome = MDTextField(
            hint_text='Nome',
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            multiline=False
        )
        self.layout.add_widget(self.input_nome)

        self.input_serv = MDTextField(
            hint_text='Serviço',
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            multiline=False
        )
        self.layout.add_widget(self.input_serv)



        self.input_val = MDTextField(
            hint_text='Valor',
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            multiline=False
        )
        self.layout.add_widget(self.input_val)

        submit_button = MDRaisedButton(
            text='ENVIAR',
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            on_press=self.anotv
        )
        self.layout.add_widget(submit_button)
        
        resumo_ve = MDRaisedButton(
            text='ir para resumo',
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.20},
            on_press=self.go_res
        )
      
        self.layout.add_widget(resumo_ve)

    def anotv(self, instance):
        nome = self.input_nome.text
        servico = self.input_serv.text
        valor = self.input_val.text
        anotv(nome, servico, valor)

class resum(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.build_iu()
        self.add_widget(self.layout)
    
    def build_iu(self):
        
        self.card = MDCard(
            size_hint=(None, None),
            size=(400, 300),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            orientation='vertical'
        )
        self.layout.add_widget(self.card)
        self.scroll_view = ScrollView(size_hint=(1, None), size=(400, 300))
        self.card.add_widget(self.scroll_view)
        self.vendas_layout = MDBoxLayout(orientation='vertical', size_hint_y=None)
        self.vendas_layout.bind(minimum_height=self.vendas_layout.setter('height'))
        self.scroll_view.add_widget(self.vendas_layout)

        self.resumo_label = MDLabel(
            text='Resumo das Vendas',
            halign='center',
            size_hint=(1, None),
            height=50
        )
        self.layout.add_widget(self.resumo_label)
        
        gerar_resumo = MDRaisedButton(
            text='Resumo',
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            on_press=self.gerar_res
        )
        self.layout.add_widget(gerar_resumo)
        

    def gerar_res(self, instance):
        vendas = get()  # Chamar a função para buscar as vendas
        self.vendas_layout.clear_widgets()  # Limpa os widgets anteriores

        if not vendas:
            
            venda_label = MDLabel(
                text="Nenhuma venda encontrada para a data atual.",
                size_hint_y=None,
                height=40
            )
            self.vendas_layout.add_widget(venda_label)
            return
            
        
        resumo_text = "Vendas do dia atual:\n"
        for venda in vendas:
            venda_label = MDLabel(
                text=f"Nome: {venda[1]}, Serviço: {venda[2]}, Valor: {venda[3]}, Data: {venda[4]}",
                size_hint_y=None,
                height=40
            )
        self.vendas_layout.add_widget(venda_label)
      
       
        
        
    
class MyApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Logins(name='login'))
        sm.add_widget(Cadastro(name='Cadastro'))
        sm.add_widget(nvendas(name='nvendas'))
        sm.add_widget(resum(name='resum'))
        return sm

    

if __name__ == '__main__':
    init_db()
    MyApp().run()

