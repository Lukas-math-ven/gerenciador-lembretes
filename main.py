import schedule
import time
import threading
from plyer import notification
from database import criar_banco, adicionar_lembrete, listar_lembretes_com_id, deletar_lembrete, registrar_usuario, verificar_login
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import csv

# Funções de notificação e agendamento
def enviar_notificacao(mensagem):
    notification.notify(
        title='Lembrete!',
        message=mensagem,
        app_name='Gerenciador de Lembretes',
        timeout=10
    )

def agendar_lembretes(user_id):
    lembretes = listar_lembretes_com_id(user_id)
    for _, mensagem, hora, recorrencia in lembretes:
        if recorrencia == 'diario':
            schedule.every().day.at(hora).do(enviar_notificacao, mensagem)
        elif recorrencia == 'semanal':
            schedule.every().monday.at(hora).do(enviar_notificacao, mensagem)
        else:
            schedule.every().day.at(hora).do(enviar_notificacao, mensagem)

def rodar_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Funções compartilhadas para temas
temas = {
    'claro': {
        'bg': 'white',
        'fg': 'black',
        'button_bg': 'lightgray',
        'tree_bg': 'white',
        'tree_fg': 'black'
    },
    'escuro': {
        'bg': '#333333',
        'fg': 'white',
        'button_bg': '#555555',
        'tree_bg': '#444444',
        'tree_fg': 'white'
    }
}

def aplicar_tema(root, tema, label_status=None, tree=None):
    style = ttk.Style()
    root.config(bg=temas[tema]['bg'])
    style.configure('TLabel', background=temas[tema]['bg'], foreground=temas[tema]['fg'])
    style.configure('TButton', background=temas[tema]['button_bg'], foreground=temas[tema]['fg'])
    if tree:
        style.configure('Treeview', background=temas[tema]['tree_bg'], foreground=temas[tema]['tree_fg'], fieldbackground=temas[tema]['tree_bg'])
        style.map('Treeview', background=[('selected', 'blue')], foreground=[('selected', 'white')])
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(bg=temas[tema]['bg'], fg=temas[tema]['fg'])
        elif isinstance(widget, tk.Button):
            widget.config(bg=temas[tema]['button_bg'], fg=temas[tema]['fg'])
    if label_status:
        label_status.config(bg=temas[tema]['bg'], fg=temas[tema]['fg'])

# GUI principal
def abrir_gui_principal(user_id):
    tema_atual = 'claro'

    def alternar_tema():
        nonlocal tema_atual
        tema_atual = 'escuro' if tema_atual == 'claro' else 'claro'
        aplicar_tema(root_principal, tema_atual, label_status, tree)
        button_tema.config(text=f"Alternar para {'Escuro' if tema_atual == 'claro' else 'Claro'}")

    def atualizar_lista():
        tree.delete(*tree.get_children())
        lembretes = listar_lembretes_com_id(user_id)
        for id_lem, msg, hr, rec in lembretes:
            tree.insert('', 'end', values=(id_lem, hr, msg, rec))

    def adicionar_gui():
        msg = entry_msg.get()
        hr = entry_hora.get()
        rec = combo_recorrencia.get()
        try:
            datetime.strptime(hr, '%H:%M')
            adicionar_lembrete(msg, hr, rec, user_id)
            atualizar_lista()
            label_status.config(text="Adicionado com sucesso!")
        except ValueError:
            label_status.config(text="Hora inválida! Use HH:MM.")

    def deletar_gui():
        selected = tree.selection()
        if selected:
            id_lem = tree.item(selected)['values'][0]
            deletar_lembrete(id_lem, user_id)
            atualizar_lista()
            label_status.config(text="Deletado com sucesso!")
        else:
            label_status.config(text="Selecione um item para deletar.")

    def exportar_csv():
        lembretes = listar_lembretes_com_id(user_id)
        with open('lembretes.csv', 'w', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(['ID', 'Hora', 'Mensagem', 'Recorrência'])
            for lembrete in lembretes:
                writer.writerow(lembrete)
        label_status.config(text="Exportado para lembretes.csv com sucesso!")

    root_principal = tk.Tk()
    root_principal.title("Gerenciador de Lembretes")
    root_principal.iconbitmap('icone.ico')

    tk.Label(root_principal, text="Mensagem:").pack()
    entry_msg = tk.Entry(root_principal)
    entry_msg.pack()

    tk.Label(root_principal, text="Hora (HH:MM):").pack()
    entry_hora = tk.Entry(root_principal)
    entry_hora.pack()

    tk.Label(root_principal, text="Recorrência:").pack()
    combo_recorrencia = ttk.Combobox(root_principal, values=['unico', 'diario', 'semanal'])
    combo_recorrencia.current(0)
    combo_recorrencia.pack()

    tk.Button(root_principal, text="Adicionar", command=adicionar_gui).pack()
    tk.Button(root_principal, text="Deletar Selecionado", command=deletar_gui).pack()
    tk.Button(root_principal, text="Exportar para CSV", command=exportar_csv).pack()

    button_tema = tk.Button(root_principal, text="Alternar para Escuro", command=alternar_tema)
    button_tema.pack()

    tree = ttk.Treeview(root_principal, columns=('ID', 'Hora', 'Mensagem', 'Recorrência'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Hora', text='Hora')
    tree.heading('Mensagem', text='Mensagem')
    tree.heading('Recorrência', text='Recorrência')
    tree.pack()

    label_status = tk.Label(root_principal, text="")
    label_status.pack()

    aplicar_tema(root_principal, tema_atual, label_status, tree)
    atualizar_lista()
    root_principal.mainloop()

    agendar_lembretes(user_id)
    threading.Thread(target=rodar_schedule, daemon=True).start()
    print("App rodando em background. Pressione Ctrl+C para sair.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("App encerrado.")

# Tela de Login com tema
def tela_login():
    tema_atual = 'claro'

    def alternar_tema():
        nonlocal tema_atual
        tema_atual = 'escuro' if tema_atual == 'claro' else 'claro'
        aplicar_tema(root_login, tema_atual, label_status_login)
        button_tema_login.config(text=f"Alternar para {'Escuro' if tema_atual == 'claro' else 'Claro'}")

    def login():
        username = entry_user.get()
        password = entry_pass.get()
        user_id = verificar_login(username, password)
        if user_id:
            root_login.destroy()
            abrir_gui_principal(user_id)
        else:
            label_status_login.config(text="Login inválido! Tente novamente.")

    def registrar():
        username = entry_user.get()
        password = entry_pass.get()
        if registrar_usuario(username, password):
            label_status_login.config(text="Usuário registrado! Faça login.")
        else:
            label_status_login.config(text="Usuário já existe! Escolha outro.")

    root_login = tk.Tk()
    root_login.title("Login - Gerenciador de Lembretes")
    root_login.iconbitmap('icone.ico')

    tk.Label(root_login, text="Username:").pack()
    entry_user = tk.Entry(root_login)
    entry_user.pack()

    tk.Label(root_login, text="Senha:").pack()
    entry_pass = tk.Entry(root_login, show="*")
    entry_pass.pack()

    tk.Button(root_login, text="Login", command=login).pack()
    tk.Button(root_login, text="Registrar Novo Usuário", command=registrar).pack()

    button_tema_login = tk.Button(root_login, text="Alternar para Escuro", command=alternar_tema)
    button_tema_login.pack()

    label_status_login = tk.Label(root_login, text="")
    label_status_login.pack()

    aplicar_tema(root_login, tema_atual, label_status_login)
    root_login.mainloop()

def fade_in_label(label, text, duration=1000, steps=20, tema_atual='claro'):
    label.config(text=text, fg='gray')  # Inicia cinza (opacidade baixa)
    root = label.winfo_toplevel()  # Pega raiz para after
    delta = 1 / steps  # Incremento de opacidade
    def fade_step(step=0, tema_atual=tema_atual):  # Passe tema como parâmetro
        if step < steps:
            # Simula fade mudando cor (de cinza a preta/branca baseado no tema)
            if tema_atual == 'claro':
                color = f'#{int(128 + 128 * (step / steps)):02x}{int(128 + 128 * (step / steps)):02x}{int(128 + 128 * (step / steps)):02x}'  # Cinza a preto
            else:
                color = f'#{int(128 * (step / steps)):02x}{int(128 * (step / steps)):02x}{int(128 * (step / steps)):02x}'  # Preto a cinza claro
            label.config(fg=color)
            root.after(duration // steps, fade_step, step + 1, tema_atual)
    fade_step()



# Inicializa e abre login
criar_banco()
tela_login()