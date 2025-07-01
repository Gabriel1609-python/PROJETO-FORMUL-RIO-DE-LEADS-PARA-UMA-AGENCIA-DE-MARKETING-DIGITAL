import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

def conectar():
    return sqlite3.connect('leads.db')

def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT,
            interesse TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def inserir_lead():
    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()
    interesse = entry_interesse.get()
    status = combo_status.get()

    if nome and email:
        conn = conectar()
        c = conn.cursor()
        c.execute('''
            INSERT INTO leads (nome, email, telefone, interesse, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, email, telefone, interesse, status))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Lead cadastrado com sucesso!")
        mostrar_leads()
        limpar_campos()
    else:
        messagebox.showerror("Erro", "Nome e E-mail são obrigatórios.")

def mostrar_leads():
    for row in tree.get_children():
        tree.delete(row)
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM leads')
    for lead in c.fetchall():
        tree.insert("", tk.END, values=lead)
    conn.close()

def deletar_lead():
    selecao = tree.selection()
    if selecao:
        lead_id = tree.item(selecao)['values'][0]
        conn = conectar()
        c = conn.cursor()
        c.execute('DELETE FROM leads WHERE id = ?', (lead_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Lead deletado com sucesso.")
        mostrar_leads()
        limpar_campos()
    else:
        messagebox.showwarning("Atenção", "Selecione um lead para deletar.")

def atualizar_lead():
    selecao = tree.selection()
    if selecao:
        lead_id = tree.item(selecao)['values'][0]
        nome = entry_nome.get()
        email = entry_email.get()
        telefone = entry_telefone.get()
        interesse = entry_interesse.get()
        status = combo_status.get()

        if nome and email:
            conn = conectar()
            c = conn.cursor()
            c.execute('''
                UPDATE leads
                SET nome = ?, email = ?, telefone = ?, interesse = ?, status = ?
                WHERE id = ?
            ''', (nome, email, telefone, interesse, status, lead_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Lead atualizado com sucesso.")
            mostrar_leads()
            limpar_campos()
        else:
            messagebox.showerror("Erro", "Nome e E-mail são obrigatórios.")
    else:
        messagebox.showwarning("Atenção", "Selecione um lead para atualizar.")

def selecionar_lead(event):
    selecao = tree.selection()
    if selecao:
        valores = tree.item(selecao)['values']
        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, valores[1])
        entry_email.delete(0, tk.END)
        entry_email.insert(0, valores[2])
        entry_telefone.delete(0, tk.END)
        entry_telefone.insert(0, valores[3])
        entry_interesse.delete(0, tk.END)
        entry_interesse.insert(0, valores[4])
        combo_status.set(valores[5])

def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_interesse.delete(0, tk.END)
    combo_status.set("")

janela = tk.Tk()
janela.title("Gerenciador de Leads - Agência Marketing Digital")

tk.Label(janela, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
entry_nome = tk.Entry(janela)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

tk.Label(janela, text="Email:").grid(row=1, column=0, padx=5, pady=5)
entry_email = tk.Entry(janela)
entry_email.grid(row=1, column=1, padx=5, pady=5)

tk.Label(janela, text="Telefone:").grid(row=2, column=0, padx=5, pady=5)
entry_telefone = tk.Entry(janela)
entry_telefone.grid(row=2, column=1, padx=5, pady=5)

tk.Label(janela, text="Interesse:").grid(row=3, column=0, padx=5, pady=5)
entry_interesse = tk.Entry(janela)
entry_interesse.grid(row=3, column=1, padx=5, pady=5)

tk.Label(janela, text="Status:").grid(row=4, column=0, padx=5, pady=5)
combo_status = ttk.Combobox(janela, values=["Em andamento", "Convertido", "Perdido"])
combo_status.grid(row=4, column=1, padx=5, pady=5)

tk.Button(janela, text="Cadastrar", command=inserir_lead).grid(row=5, column=0, padx=5, pady=10)
tk.Button(janela, text="Atualizar", command=atualizar_lead).grid(row=5, column=1, padx=5, pady=10)
tk.Button(janela, text="Deletar", command=deletar_lead).grid(row=5, column=2, padx=5, pady=10)
tk.Button(janela, text="Limpar", command=limpar_campos).grid(row=5, column=3, padx=5, pady=10)

columns = ("ID", "Nome", "Email", "Telefone", "Interesse", "Status")
tree = ttk.Treeview(janela, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=6, column=0, columnspan=4, padx=10, pady=10)
tree.bind("<ButtonRelease-1>", selecionar_lead)

criar_tabela()
mostrar_leads()
janela.mainloop()