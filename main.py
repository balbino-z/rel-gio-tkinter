import tkinter as tk
from tkinter import *
from time import strftime, localtime
from datetime import datetime
import pytz
import requests
import locale
from tkinter import ttk

# Função para obter o nome da conta Microsoft
def get_nome_conta_microsoft():
    return "Vinícius Balbino" 

# Configuração do idioma local para português do Brasil
locale.setlocale(locale.LC_TIME, 'pt_BR.utf-8')

# Configuração da janela principal
root = tk.Tk()
root.title('Relógio Moderno')
root.geometry("400x300")

# Definição das cores para os modos claro e escuro
cor_modo_claro = {
    'bg': '#E2E2E2',
    'fg_saudacao': '#333',
    'fg_data': '#666',
    'fg_horas': '#111',
    'borderwidth': 2,
    'relief': 'solid'
}

cor_modo_escuro = {
    'bg': '#1d1d1d',
    'fg_saudacao': '#8e27ea',
    'fg_data': '#8e27ea',
    'fg_horas': '#8e27ea',
    'borderwidth': 2,
    'relief': 'solid'
}

modo_atual = cor_modo_claro

# Criação do frame principal
frame = Frame(root, bg=modo_atual['bg'])
frame.pack(expand=True, fill=BOTH)

# Configuração dos rótulos de saudação, data e horas
saudacao = Label(frame, bg=modo_atual['bg'], fg=modo_atual['fg_saudacao'], font=('Helvetica', 20, 'bold'))
saudacao.pack(pady=(20, 0))

data = Label(frame, bg=modo_atual['bg'], fg=modo_atual['fg_data'], font=('Helvetica', 16))
data.pack(pady=5)

horas = Label(frame, bg=modo_atual['bg'], fg=modo_atual['fg_horas'], font=('Helvetica', 36, 'bold'))
horas.pack(pady=10)

# Configuração do menu suspenso para seleção do fuso horário
fuso_var = StringVar()
fuso_var.set("America/Sao_Paulo") 
fuso_label = Label(frame, text="Fuso Horário:", bg=modo_atual['bg'], fg=modo_atual['fg_data'], font=('Helvetica', 14))
fuso_label.pack(pady=(10, 0))
fuso_menu = OptionMenu(frame, fuso_var,
                       "America/New_York",
                       "Europe/Lisbon",
                       "Europe/Paris",
                       "Europe/London",
                       "Africa/Luanda",
                       "Africa/Maputo",
                       "Atlantic/Cape_Verde",
                       "Asia/Tokyo",
                       "Asia/Shanghai",
                       "Australia/Sydney",
                       "Pacific/Honolulu",
                       "UTC",
                       "Brazil/East",
                       )
fuso_menu.config(bg="#C7C4C4", fg=modo_atual['fg_data'], font=('Helvetica', 10, 'bold'))
fuso_menu.pack(pady=(10, 20))

# Função para definir e disparar um alarme
def set_alarme():
    print("Botão 'Definir Alarme' clicado.")
    alarme_hora = alarme_hora_var.get()
    alarme_minuto = alarme_minuto_var.get()
    alarme_fuso = fuso_var.get()

    print(f"Alarme definido para {alarme_hora}:{alarme_minuto} no fuso horário {alarme_fuso}")

    agora = datetime.now(pytz.timezone(alarme_fuso))
    alarme = agora.replace(hour=alarme_hora, minute=alarme_minuto, second=0, microsecond=0)

    diferenca = alarme - agora
    segundos_ate_alarme = diferenca.total_seconds()

    if segundos_ate_alarme > 0:
        horas.after(int(segundos_ate_alarme * 1000), disparar_alarme)

# Função para exibir "ALARME!" quando o alarme é disparado
def disparar_alarme():
    alarme_label.config(text="ALARME!", fg='#ff0000')  

# Configuração do rótulo para exibição do estado do alarme
alarme_label = Label(frame, text="", bg=modo_atual['bg'], fg='#e44d26', font=('Helvetica', 20, 'bold'))
alarme_label.pack()

# Variáveis e entradas para configurar a hora do alarme
alarme_hora_var = IntVar()
alarme_minuto_var = IntVar()

alarme_hora_label = Label(frame, text="Hora do Alarme:", bg=modo_atual['bg'], fg=modo_atual['fg_data'], font=('Helvetica', 14))
alarme_hora_label.pack(pady=(10, 0))
alarme_hora_entry = Entry(frame, textvariable=alarme_hora_var, bg='#fff', fg='#333', font=('Helvetica', 12), width=5, borderwidth=modo_atual['borderwidth'], relief=modo_atual['relief'])
alarme_hora_entry.pack()

alarme_minuto_label = Label(frame, text="Minuto do Alarme:", bg=modo_atual['bg'], fg=modo_atual['fg_data'], font=('Helvetica', 14))
alarme_minuto_label.pack(pady=(5, 0))
alarme_minuto_entry = Entry(frame, textvariable=alarme_minuto_var, bg='#fff', fg='#333', font=('Helvetica', 12), width=5, borderwidth=modo_atual['borderwidth'], relief=modo_atual['relief'])
alarme_minuto_entry.pack()

# Botão para definir o alarme
alarme_botao = Button(frame, text="Definir Alarme", command=set_alarme, bg='#bb0b0b', fg='#fff', font=('Helvetica', 12), borderwidth=modo_atual['borderwidth'], relief=modo_atual['relief'])
alarme_botao.pack(pady=(10, 20))

# Rótulo para exibição da previsão do tempo
previsao_tempo_label = Label(frame, text="", bg=modo_atual['bg'], fg=modo_atual['fg_data'], font=('Helvetica', 12))
previsao_tempo_label.pack()

# Função para obter e exibir a previsão do tempo
def obter_previsao_tempo():
    cidade = "Santa Bárbara d'Oeste"
    api_key = "c9c28e33300968f619a5aad5bf024775"  
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&units=metric"

    try:
        resposta = requests.get(url)
        dados = resposta.json()

        descricao = dados['weather'][0]['description']
        temperatura = dados['main']['temp']

        traducao_condicoes = {
            'clear sky': 'céu limpo',
            'few clouds': 'poucas nuvens',
            'scattered clouds': 'nuvens dispersas',
            'broken clouds': 'nuvens quebradas',
            'light rain': 'chuva leve',
            'rain': 'chuva',
            'thunderstorm': 'tempestade',
            'moderate rain': 'chuva moderada',
            'snow': 'neve',
            'mist': 'névoa'
        }

        if descricao.lower() in traducao_condicoes:
            descricao_traduzida = traducao_condicoes[descricao.lower()]
        else:
            descricao_traduzida = descricao

        previsao_tempo_label.config(text=f"Condição: {descricao_traduzida.capitalize()}, Temperatura: {temperatura}°C", font=('Helvetica', 16))
    except Exception as e:
        previsao_tempo_label.config(text="Erro ao obter previsão do tempo")

# Botão para obter a previsão do tempo
obter_previsao_tempo_botao = Button(frame, text="Obter Previsão do Tempo", command=obter_previsao_tempo, bg='#ecab0f', fg='#fff', font=('Helvetica', 12), borderwidth=modo_atual['borderwidth'], relief=modo_atual['relief'])
obter_previsao_tempo_botao.pack()

# Função para alternar entre os modos claro e escuro
def alternar_modo():
    global modo_atual

    if modo_atual == cor_modo_claro:
        modo_atual = cor_modo_escuro
    else:
        modo_atual = cor_modo_claro

    frame.configure(bg=modo_atual['bg'])
    saudacao.configure(bg=modo_atual['bg'], fg=modo_atual['fg_saudacao'])
    data.configure(bg=modo_atual['bg'], fg=modo_atual['fg_data'])
    horas.configure(bg=modo_atual['bg'], fg=modo_atual['fg_horas'])
    fuso_label.configure(bg=modo_atual['bg'], fg=modo_atual['fg_data'])
    fuso_menu.configure(bg=modo_atual['bg'], fg=modo_atual['fg_data'])
    alarme_label.configure(bg=modo_atual['bg'])
    alarme_hora_label.configure(bg=modo_atual['bg'], fg=modo_atual['fg_data'])
    alarme_minuto_label.configure(bg=modo_atual['bg'], fg=modo_atual['fg_data'])
    alarme_hora_entry.configure(bg='#fff', fg='#333', relief="solid")
    alarme_minuto_entry.configure(bg='#fff', fg='#333', relief="solid")
    alarme_botao.configure(borderwidth=modo_atual['borderwidth'], relief=modo_atual['relief'])
    previsao_tempo_label.configure(bg=modo_atual['bg'], fg=modo_atual['fg_data'])
    obter_previsao_tempo_botao.configure(borderwidth=modo_atual['borderwidth'], relief=modo_atual['relief'])

# Botão para alternar entre os modos claro e escuro
modo_botao = Button(frame, text="Alternar Modo", command=alternar_modo, bg='#7B7B7B', fg='#fff', font=('Helvetica', 12), borderwidth=modo_atual['borderwidth'], relief=modo_atual['relief'])
modo_botao.pack(pady=10)

# Função para atualizar o relógio
def update():
    fuso_horario = pytz.timezone(fuso_var.get())
    atual = datetime.now(fuso_horario)
    data_atual = atual.strftime('%A, %d %B %Y')
    horas_atual = atual.strftime('%H:%M:%S %p')

    saudacao.config(text="Olá, " + get_nome_conta_microsoft())
    data.config(text=data_atual)
    horas.config(text=horas_atual)

    root.after(1000, update)

# Inicia a atualização do relógio
update()

# Inicia o loop principal da interface gráfica
root.mainloop()