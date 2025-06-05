const express = require('express');
require('dotenv').config();
const path = require('path');
const connection = require('./database/connection');

const app = express();
app.use(express.json());

// Servir arquivos estáticos da pasta "site"
app.use(express.static(path.join(__dirname, 'site')));

// Rota principal "/" -> exibe o index.html
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'site', 'index.html'));
});

// Login
app.get('/usuarios', async (req, res) => {
  try {
    const { cpf, senha } = req.query;

    if (!cpf || !senha) {
      return res.status(400).json({ error: 'CPF e senha são obrigatórios' });
    }

    const [rows] = await connection.execute(
      'SELECT * FROM usuarios WHERE cpf = ? AND senha = ?',
      [cpf, senha]
    );

    if (rows.length === 0) {
      return res.status(401).json({ message: 'CPF ou senha inválidos' });
    }

    res.json({ message: 'Login realizado com sucesso', usuario: rows[0] });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Cadastro
app.post('/usuarios', async (req, res) => {
  const { nome, cpf, data_nascimento, telefone, senha } = req.body;

  if (!nome || !cpf || !data_nascimento || !telefone || !senha) {
    return res.status(400).json({ error: 'Todos os campos são obrigatórios' });
  }

  try {
    await connection.execute(
      `INSERT INTO usuarios (nome, cpf, data_nascimento, telefone, senha)
       VALUES (?, ?, ?, ?, ?)`,
      [nome, cpf, data_nascimento, telefone, senha]
    );

    res.status(201).json({ message: 'Usuário cadastrado com sucesso' });
  } catch (error) {
    res.status(500).json({ error: 'Erro ao cadastrar usuário' });
  }
});

// Atualizar
app.put('/usuarios/:id', async (req, res) => {
  const { id } = req.params;
  const { nome, cpf, data_nascimento, telefone, senha } = req.body;

  try {
    const [result] = await connection.execute(
      `UPDATE usuarios SET nome = ?, cpf = ?, data_nascimento = ?, telefone = ?, senha = ?
       WHERE id_usuario = ?`,
      [nome, cpf, data_nascimento, telefone, senha, id]
    );

    if (result.affectedRows === 0) {
      return res.status(404).json({ message: 'Usuário não encontrado' });
    }

    res.json({ message: 'Usuário atualizado com sucesso' });
  } catch (error) {
    res.status(500).json({ error: 'Erro ao atualizar usuário' });
  }
});

// Excluir
app.delete('/usuarios/:id', async (req, res) => {
  const { id } = req.params;

  try {
    const [result] = await connection.execute(
      'DELETE FROM usuarios WHERE id_usuario = ?',
      [id]
    );

    if (result.affectedRows === 0) {
      return res.status(404).json({ message: 'Usuário não encontrado' });
    }

    res.json({ message: 'Usuário excluído com sucesso' });
  } catch (error) {
    res.status(500).json({ error: 'Erro ao excluir usuário' });
  }
});

// Iniciar o servidor
const PORT = 80;
app.listen(PORT, () =>
  console.log(`Servidor rodando em http://localhost:${PORT}`)
);
