import tkinter as tk
import tkinter.font as tkFont
from tkinter import PhotoImage
import sqlite3
import pickle


class App:

  def __init__(self, root):
    root.title("Trabalho")
    width = 600
    height = 500
    alignstr = '%dx%d+%d+%d' % (width, height,
                                (root.winfo_screenwidth() - width) / 2,
                                (root.winfo_screenheight() - height) / 2)
    root.geometry(alignstr)
    root.resizable(width=False, height=False)

    self.conexao = sqlite3.connect('Museo.db')
    self.sql = self.conexao.cursor()
    self.sql.execute('CREATE TABLE IF NOT EXISTS Obras (Nomes, Descrição)')
    self.conexao.commit()

    self.imagem = PhotoImage(file="logo_ifrn.png").subsample(16)

    self.logo_ifrn = tk.Label(root, image=self.imagem)
    self.logo_ifrn.place(x=5, y=10)

    self.nome_do_trabalho = tk.Label(root,
                                     text="Sistema de Cadastro de Obras",
                                     font=('Times', 10))
    self.nome_do_trabalho.place(x=120, y=40, width=311, height=30)

    self.label_nomeObra = tk.Label(root, text="Nome da obra")
    self.label_nomeObra.place(x=50, y=110, width=90, height=30)

    self.caixa_nomeObra = tk.Entry(root)
    self.caixa_nomeObra.place(x=70, y=140, width=276, height=25)

    self.label_descricaoObras = tk.Label(root, text="Descrição da obra")
    self.label_descricaoObras.place(x=50, y=180, width=109, height=30)

    self.caixa_descricaoObras = tk.Entry(root)
    self.caixa_descricaoObras.place(x=70, y=210, width=276, height=25)

    self.label_mensagem = tk.Label(root, text="", font=('Times', 10))
    self.label_mensagem.place(x=70, y=235, width=280, height=30)

    self.button_ok = tk.Button(root,
                               text="Ok",
                               bg="light green",
                               command=self.ok)
    self.button_ok.place(x=150, y=265, width=111, height=30)

    self.label_listaObras = tk.Label(root,
                                     text="Lista das Obras",
                                     font=('Times', 10))
    self.label_listaObras.place(x=50, y=305, width=150, height=30)

    self.labels_obras = []

    self.button_adicionarObras = tk.Button(root,
                                           text="Adicionar Obra",
                                           bg="green",
                                           command=self.adicionarObras)
    self.button_adicionarObras.place(x=440, y=100, width=111, height=30)

    self.button_verObras = tk.Button(root,
                                     text="Ver Obras",
                                     bg="yellow",
                                     command=self.verObras)
    self.button_verObras.place(x=440, y=160, width=111, height=30)

    self.button_excluirObras = tk.Button(root,
                                         text="Excluir Obras",
                                         bg="red",
                                         command=self.excluirObras)
    self.button_excluirObras.place(x=440, y=220, width=111, height=30)

    self.button_backup = tk.Button(root,
                                   text="Backup",
                                   bg="blue",
                                   command=self.fazerBackup)
    self.button_backup.place(x=440, y=280, width=111, height=30)

    self.funcao = ''

  def adicionarObras(self):
    self.label_descricaoObras.place(width=129, height=40)
    self.caixa_descricaoObras.place(width=296, height=35)
    self.label_mensagem.place(x=70, y=235, width=280, height=30)
    self.label_mensagem['text'] = ''
    self.button_ok.place(x=150, y=265)

    nome_obra = self.caixa_nomeObra.get()
    descricao_obra = self.caixa_descricaoObras.get()

    try:
      if not nome_obra or not descricao_obra:
        raise ValueError("Nome e descrição não podem estar vazios.")

      self.sql.execute("INSERT INTO Obras (Nomes, Descrição) VALUES (?, ?)",
                       (nome_obra, descricao_obra))
      self.conexao.commit()
      self.funcao = 'adicionar'
    except ValueError as e:
      self.label_mensagem['fg'] = 'red'
      self.label_mensagem['text'] = str(e)

  def verObras(self):
    self.sql.execute("SELECT Nomes, Descrição FROM Obras")
    obras = self.sql.fetchall()
    for i, obra in enumerate(obras):
      nome_obra = obra[0]
      descricao_obra = obra[1]
      label_obra = tk.Label(
          root, text=f"Nome: {nome_obra} - Descrição {descricao_obra}")
      label_obra.place(x=50, y=335 + i * 30, width=280, height=30)
      self.labels_obras.append(label_obra)

    self.funcao = 'ver_obras'

  def excluirObras(self):
    self.label_descricaoObras.place(width=0, height=0)
    self.caixa_descricaoObras.place(width=0, height=0)
    nome_obra = self.caixa_nomeObra.get()

    try:
      if not nome_obra:
        raise ValueError("Nome não pode estar vazio.")

      self.sql.execute("DELETE FROM Obras WHERE Nomes = ?", (nome_obra, ))
      self.sql.execute("UPDATE Obras SET Descrição = NULL WHERE Nomes = ?",
                       (nome_obra, ))
      self.conexao.commit()
      self.funcao = 'excluir'
    except ValueError as e:
      self.label_mensagem['fg'] = 'red'
      self.label_mensagem['text'] = str(e)

  def ok(self):
    if self.funcao == 'adicionar':
      self.label_mensagem['fg'] = 'green'
      self.label_mensagem['text'] = 'Obra adicionada com sucesso!'
      self.caixa_nomeObra.delete(0, 'end')
      self.caixa_descricaoObras.delete(0, 'end')

    elif self.funcao == 'excluir':
      self.label_mensagem['fg'] = 'red'
      self.label_mensagem['text'] = 'Obra excluída com sucesso!'
      self.caixa_nomeObra.delete(0, 'end')

  def fazerBackup(self):
    try:
      self.sql.execute("SELECT Nomes, Descrição FROM Obras")
      dados = self.sql.fetchall()

      if not dados:
        raise ValueError("Não há dados para fazer backup.")

      with open("backup_obras.pkl", "wb") as arquivo:

        pickle.dump(dados, arquivo)

      self.label_mensagem['fg'] = 'green'
      self.label_mensagem['text'] = 'Backup realizado com sucesso!'
    except Exception as e:

      self.label_mensagem['fg'] = 'red'
      self.label_mensagem['text'] = f"Erro durante o backup: {str(e)}"


if __name__ == "__main__":
  root = tk.Tk()
  app = App(root)
  root.mainloop()
