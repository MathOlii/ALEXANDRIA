# Diagramas de Sequência — Alexandria

Diagramas em [Mermaid](https://mermaid.js.org/) (renderizados pelo GitHub).

## 1. Finalizar pedido (Decorator + relacionamento 1:n)

Mostra como o `PedidoService` monta **automaticamente** a cadeia de Decorators
para calcular o preço final e persiste o pedido e seus itens.

```mermaid
sequenceDiagram
    actor Cliente
    participant UI as ClienteMenu
    participant SVC as PedidoService
    participant CALC as Cadeia de Decorators
    participant LR as LivroRepository
    participant PR as PedidoRepository

    Cliente->>UI: Finalizar Pedido (cupom opcional)
    UI->>SVC: finalizar_pedido(usuario_id, carrinho, cupom)
    SVC->>SVC: montar_calculo(carrinho, cupom)
    Note over SVC,CALC: PrecoBase → DescontoProgressivo → Cupom → Imposto → Frete
    SVC->>CALC: calcular()
    CALC-->>SVC: total final
    SVC->>PR: inserir(Pedido)
    PR-->>SVC: pedido_id
    loop para cada item do carrinho
        SVC->>LR: buscar_por_id(livro_id)
        LR-->>SVC: Livro
        SVC->>SVC: livro.baixar_estoque(qtd)
        SVC->>LR: atualizar(Livro)
        SVC->>PR: inserir_item(ItemPedido)
    end
    SVC->>SVC: carrinho.limpar()
    SVC-->>UI: pedido_id
    UI-->>Cliente: "Pedido #N realizado!"
```

## 2. Cadastro de usuário + endereço (relacionamento 1:1, Factory, Strategy)

```mermaid
sequenceDiagram
    actor Visitante
    participant UI as CadastroScreen
    participant AUTH as AuthService
    participant VAL as ValidadorCadastro
    participant FAC as UsuarioFactory
    participant UR as UsuarioRepository
    participant ER as EnderecoRepository

    Visitante->>UI: Preenche formulário e clica em Cadastrar
    UI->>AUTH: cadastrar(dados)
    AUTH->>VAL: validar(dados)
    VAL-->>AUTH: lista de erros (vazia se ok)
    alt dados inválidos
        AUTH-->>UI: DadosInvalidos(erros)
        UI-->>Visitante: mostra erros
    else dados válidos
        AUTH->>FAC: criar(tipo, ...)
        FAC-->>AUTH: Cliente ou Administrador
        AUTH->>UR: inserir(usuario)
        UR-->>AUTH: usuario_id
        AUTH->>ER: inserir(endereco com usuario_id)
        AUTH-->>UI: usuario
        UI-->>Visitante: "Cadastro realizado!"
    end
```

## 3. Admin: deletar livro com Undo (Command)

```mermaid
sequenceDiagram
    actor Admin
    participant UI as AdminMenu
    participant INV as GerenciadorComandos
    participant CMD as DeletarLivroCommand
    participant LR as LivroRepository

    Admin->>UI: Deletar livro selecionado
    UI->>INV: executar(DeletarLivroCommand)
    INV->>CMD: executar()
    CMD->>LR: buscar_por_id(id)
    LR-->>CMD: Livro (guardado para undo)
    CMD->>LR: deletar(id)
    INV->>INV: histórico.append(comando)

    Admin->>UI: Desfazer última ação
    UI->>INV: desfazer_ultimo()
    INV->>CMD: desfazer()
    CMD->>LR: inserir(livro_removido)
    INV-->>UI: "Ação desfeita"
```
