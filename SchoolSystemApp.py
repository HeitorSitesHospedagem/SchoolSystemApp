import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

class Aluno:
    def __init__(self, id, nome, nota):
        self.id = id
        self.nome = nome
        self.nota = nota

    def __str__(self):
        return f"ID: {self.id}, Nome: {self.nome}, Nota: {self.nota}"

class Professor:
    def __init__(self, id, nome, disciplina):
        self.id = id
        self.nome = nome
        self.disciplina = disciplina

    def __str__(self):
        return f"ID: {self.id}, Nome: {self.nome}, Disciplina: {self.disciplina}"

class AplicativoSistemaEscolar:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestão Escolar")

        self.conexao_bd = sqlite3.connect('sistema_escolar.db')
        self.criar_tabelas()

        self.alunos = []
        self.professores = []

        self.criar_widgets()
        self.carregar_alunos()
        self.carregar_professores()

    def criar_tabelas(self):
        cursor = self.conexao_bd.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS alunos (
                            id INTEGER PRIMARY KEY,
                            nome TEXT,
                            nota TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS professores (
                            id INTEGER PRIMARY KEY,
                            nome TEXT,
                            disciplina TEXT)''')
        self.conexao_bd.commit()

    def criar_widgets(self):
        # Quadro de gestão de alunos
        quadro_aluno = tk.LabelFrame(self.root, text="Gestão de Alunos")
        quadro_aluno.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        tk.Label(quadro_aluno, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.entrada_nome_aluno = tk.Entry(quadro_aluno)
        self.entrada_nome_aluno.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(quadro_aluno, text="Nota:").grid(row=1, column=0, padx=5, pady=5)
        self.entrada_nota_aluno = tk.Entry(quadro_aluno)
        self.entrada_nota_aluno.grid(row=1, column=1, padx=5, pady=5)

        botao_adicionar_aluno = tk.Button(quadro_aluno, text="Adicionar Aluno", command=self.adicionar_aluno)
        botao_adicionar_aluno.grid(row=2, columnspan=2, padx=5, pady=5)

        # Quadro de gestão de professores
        quadro_professor = tk.LabelFrame(self.root, text="Gestão de Professores")
        quadro_professor.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        tk.Label(quadro_professor, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.entrada_nome_professor = tk.Entry(quadro_professor)
        self.entrada_nome_professor.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(quadro_professor, text="Disciplina:").grid(row=1, column=0, padx=5, pady=5)
        self.entrada_disciplina_professor = tk.Entry(quadro_professor)
        self.entrada_disciplina_professor.grid(row=1, column=1, padx=5, pady=5)

        botao_adicionar_professor = tk.Button(quadro_professor, text="Adicionar Professor", command=self.adicionar_professor)
        botao_adicionar_professor.grid(row=2, columnspan=2, padx=5, pady=5)

        # Quadros de registros de alunos e professores
        quadro_registros_aluno = tk.LabelFrame(self.root, text="Registros de Alunos")
        quadro_registros_aluno.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.lista_alunos = tk.Listbox(quadro_registros_aluno, height=5, width=50)
        self.lista_alunos.grid(row=0, column=0, padx=5, pady=5)

        quadro_registros_professor = tk.LabelFrame(self.root, text="Registros de Professores")
        quadro_registros_professor.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self.lista_professores = tk.Listbox(quadro_registros_professor, height=5, width=50)
        self.lista_professores.grid(row=0, column=0, padx=5, pady=5)

        # Botões de busca
        botao_buscar_aluno = tk.Button(self.root, text="Buscar Alunos", command=self.popup_buscar_alunos)
        botao_buscar_aluno.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        botao_buscar_professor = tk.Button(self.root, text="Buscar Professores", command=self.popup_buscar_professores)
        botao_buscar_professor.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        # Centralizar a janela principal
        self.centralizar_janela()

    def centralizar_janela(self):
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()

        x = (largura_tela - self.root.winfo_reqwidth()) // 2
        y = (altura_tela - self.root.winfo_reqheight()) // 2

        self.root.geometry("+{}+{}".format(x, y))

    def adicionar_aluno(self):
        nome = self.entrada_nome_aluno.get()
        nota = self.entrada_nota_aluno.get()

        if nome and nota:
            cursor = self.conexao_bd.cursor()
            cursor.execute("INSERT INTO alunos (nome, nota) VALUES (?, ?)", (nome, nota))
            self.conexao_bd.commit()
            self.carregar_alunos()
            self.entrada_nome_aluno.delete(0, tk.END)
            self.entrada_nota_aluno.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos para o aluno.")

    def adicionar_professor(self):
        nome = self.entrada_nome_professor.get()
        disciplina = self.entrada_disciplina_professor.get()

        if nome and disciplina:
            cursor = self.conexao_bd.cursor()
            cursor.execute("INSERT INTO professores (nome, disciplina) VALUES (?, ?)", (nome, disciplina))
            self.conexao_bd.commit()
            self.carregar_professores()
            self.entrada_nome_professor.delete(0, tk.END)
            self.entrada_disciplina_professor.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos para o professor.")

    def carregar_alunos(self):
        cursor = self.conexao_bd.cursor()
        cursor.execute("SELECT * FROM alunos")
        alunos = cursor.fetchall()
        self.lista_alunos.delete(0, tk.END)
        for aluno in alunos:
            self.lista_alunos.insert(tk.END, f"ID: {aluno[0]}, Nome: {aluno[1]}, Nota: {aluno[2]}")

    def carregar_professores(self):
        cursor = self.conexao_bd.cursor()
        cursor.execute("SELECT * FROM professores")
        professores = cursor.fetchall()
        self.lista_professores.delete(0, tk.END)
        for professor in professores:
            self.lista_professores.insert(tk.END, f"ID: {professor[0]}, Nome: {professor[1]}, Disciplina: {professor[2]}")

    def popup_buscar_alunos(self):
        popup = tk.Toplevel(self.root)
        popup.title("Buscar Alunos")

        tk.Label(popup, text="Digite o nome do aluno:").grid(row=0, column=0, padx=5, pady=5)
        entrada_busca = tk.Entry(popup)
        entrada_busca.grid(row=0, column=1, padx=5, pady=5)

        botao_buscar = tk.Button(popup, text="Buscar", command=lambda: self.buscar_alunos(entrada_busca.get()))
        botao_buscar.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        botao_fechar = tk.Button(popup, text="Fechar", command=popup.destroy)
        botao_fechar.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def popup_buscar_professores(self):
        popup = tk.Toplevel(self.root)
        popup.title("Buscar Professores")

        tk.Label(popup, text="Digite o nome do professor:").grid(row=0, column=0, padx=5, pady=5)
        entrada_busca = tk.Entry(popup)
        entrada_busca.grid(row=0, column=1, padx=5, pady=5)

        botao_buscar = tk.Button(popup, text="Buscar", command=lambda: self.buscar_professores(entrada_busca.get()))
        botao_buscar.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        botao_fechar = tk.Button(popup, text="Fechar", command=popup.destroy)
        botao_fechar.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def buscar_alunos(self, query):
        if query:
            cursor = self.conexao_bd.cursor()
            cursor.execute("SELECT * FROM alunos WHERE nome LIKE ?", ('%' + query + '%',))
            alunos = cursor.fetchall()
            self.lista_alunos.delete(0, tk.END)
            for aluno in alunos:
                self.lista_alunos.insert(tk.END, f"ID: {aluno[0]}, Nome: {aluno[1]}, Nota: {aluno[2]}")

    def buscar_professores(self, query):
        if query:
            cursor = self.conexao_bd.cursor()
            cursor.execute("SELECT * FROM professores WHERE nome LIKE ?", ('%' + query + '%',))
            professores = cursor.fetchall()
            self.lista_professores.delete(0, tk.END)
            for professor in professores:
                self.lista_professores.insert(tk.END, f"ID: {professor[0]}, Nome: {professor[1]}, Disciplina: {professor[2]}")

root = tk.Tk()
app = AplicativoSistemaEscolar(root)
root.mainloop()
