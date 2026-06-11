# 📚 Alexandria

Sistema de **livraria** desenvolvido em Python com interface gráfica (Tkinter)
e banco de dados SQLite. O projeto foi estruturado em camadas e aplica
**Design Patterns** e os princípios **SOLID** e de **Calistenia de Objetos**.

---

## ✨ Funcionalidades

- **Autenticação:** cadastro e login de usuários (cliente / administrador).
- **CRUD completo** de **Livros**, **Usuários/Endereços** e **Pedidos**
  (inserir, deletar, atualizar, consultar por id e consultar todos).
- **Catálogo e busca** de livros.
- **Carrinho de compras** e **finalização de pedido** com baixa de estoque.
- **Cálculo automático do preço do pedido** via cadeia de **Decorators**
  (desconto progressivo, cupom, imposto e frete).
- **Undo** das operações administrativas de livro (padrão Command).

---

## 🧱 Arquitetura

O código é organizado em camadas, com dependências sempre apontando para o
domínio (regra de negócio no centro):

```
alexandria/
├── config.py                 # constantes (sem números mágicos)
├── domain/                   # regra de negócio pura
│   ├── entities/             # Livro, Usuario/Cliente/Administrador, Endereco, Pedido, Carrinho
│   ├── value_objects.py      # Email, Cpf, Telefone, Cep, Uf
│   ├── builders/             # LivroBuilder        (BUILDER)
│   └── pricing/              # CalculoPreco + Decorators (DECORATOR)
├── factories/                # UsuarioFactory       (FACTORY)
├── application/              # casos de uso
│   ├── validacao/            # regras de validação  (STRATEGY)
│   ├── commands/             # comandos de livro     (COMMAND)
│   └── services/             # AuthService, PedidoService
├── infra/                    # detalhes técnicos
│   ├── conexao.py            # conexão única         (SINGLETON)
│   ├── database_setup.py     # criação das tabelas
│   └── repositories/         # acesso a dados        (REPOSITORY)
└── ui/                       # interface Tkinter
```

## 🧩 Design Patterns aplicados

| Padrão | Onde | Para quê |
|--------|------|----------|
| **Decorator** | `domain/pricing/calculo_preco.py` | Compor o preço final do pedido empilhando regras (desconto progressivo → cupom → imposto → frete) sem alterar as classes existentes. |
| **Builder** | `domain/builders/livro_builder.py` | Construir um `Livro` passo a passo, validando os dados antes de instanciar. |
| **Factory** | `factories/usuario_factory.py` | Decidir qual subclasse de `Usuario` (`Cliente`/`Administrador`) criar a partir do tipo. |
| **Command** | `application/commands/livro_commands.py` | Encapsular as operações de CRUD de livro do admin e permitir **desfazer** a última ação. |
| **Strategy** | `application/validacao/validadores.py` | Validar cada campo do cadastro por uma regra independente, agregadas pelo `ValidadorCadastro`. |
| **Singleton** | `infra/conexao.py` | Manter uma única conexão com o banco. |
| **Repository** | `infra/repositories/` | Isolar o acesso a dados das regras de negócio. |

### 🎯 O processo de negócio automatizado (Decorator)

Ao finalizar um pedido, o `PedidoService.montar_calculo()` monta
**automaticamente** a cadeia de decorators sobre o subtotal do carrinho:

```
PrecoBaseCarrinho
  → DescontoProgressivo   (10% a partir de 5 itens)
  → CupomDesconto         (se um cupom válido for informado)
  → Imposto               (5%)
  → Frete                 (R$ 15,00, grátis acima de R$ 200,00)
```

Cada decorator adiciona uma responsabilidade ao cálculo sem conhecer os
demais, e a UI exibe o **detalhamento** do preço resultante.

Cupons de exemplo: `ALEXANDRIA10` (10%), `LEITOR15` (15%), `BLACKFRIDAY` (25%).

---

## 🔗 Relacionamentos entre entidades

- **1:1 — Usuário ↔ Endereço:** cada usuário possui exatamente um endereço
  (`endereco.usuario_id` é `UNIQUE`, criado junto no cadastro).
- **1:n — Pedido → Itens do Pedido:** um pedido contém vários itens
  (`item_pedido.pedido_id` referencia `pedido.id`).
- **Herança — Usuário → Cliente / Administrador.**

---

## 🧼 SOLID e Calistenia de Objetos

- **SRP:** UI só coleta dados; serviços contêm regra; repositórios persistem.
- **OCP:** novas regras de preço (decorators) ou de validação (strategies) são
  adicionadas sem modificar as existentes.
- **LSP:** `Cliente`/`Administrador` e os repositórios são substituíveis por
  suas abstrações (`Usuario`, `BaseRepository`).
- **ISP:** `BaseRepository` define um contrato CRUD enxuto.
- **DIP:** serviços dependem de abstrações e recebem repositórios por injeção.
- **Calistenia:** Value Objects encapsulam primitivos (CPF, email, ...),
  `Carrinho` é uma coleção de primeira classe, constantes nomeadas no lugar de
  números mágicos e métodos curtos.

---

## ▶️ Como executar

Requisitos: **Python 3.10+** (usa apenas a biblioteca padrão — `tkinter` e
`sqlite3`; não há dependências externas).

```bash
# 1. (opcional) popular o catálogo com livros de exemplo
python seed_livros.py

# 2. iniciar a aplicação
python main.py
```

Na primeira execução o banco `alexandria.db` é criado automaticamente.
Cadastre um usuário do tipo **admin** para gerenciar o catálogo, ou um
**cliente** para comprar.

---

## 🗂️ Estrutura do banco

| Tabela | Descrição |
|--------|-----------|
| `livro` | Catálogo de livros |
| `usuario` | Usuários (cliente/admin) |
| `endereco` | Endereço do usuário (1:1) |
| `pedido` | Cabeçalho do pedido |
| `item_pedido` | Itens do pedido (1:n) |
