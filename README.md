# Dinosaur Kingdom -- PgZero Platformer

## Descrição do Projeto

**Dinosaur Kingdom** é um jogo simples do gênero **Platformer (visão
lateral)** desenvolvido em Python utilizando **PgZero**, criado
especificamente para o *Teste de Tutores*.\
O projeto demonstra domínio de lógica de jogo, animação de sprites,
organização de código, boas práticas de nomenclatura e requisitos
formais exigidos pela banca.

O jogador controla um herói que deve derrotar inimigos e sobreviver até
eliminar todos eles.

------------------------------------------------------------------------

## Requisitos Atendidos

-   Linguagem: **Python**
-   Engine: **PgZero**
-   Bibliotecas utilizadas:
    -   `random`
    -   `pygame.Rect` (exceção permitida)
-   Gênero: **Platformer**
-   Menu principal com botões clicáveis
-   Música de fundo e efeitos sonoros com ON/OFF
-   Inimigos perigosos com movimentação própria
-   Animação real de sprites (idle e movimento)
-   Código original, organizado e independente

------------------------------------------------------------------------

## Como Jogar

### Controles do Teclado

-   **Seta para a esquerda (←)**: mover o personagem para a esquerda
-   **Seta para a direita (→)**: mover o personagem para a direita
-   **Barra de espaço**: pular

### Regras do Jogo

-   O herói pode **matar um inimigo pulando sobre ele**.
-   Se o herói **encostar lateralmente** em um inimigo, ele morre.
-   Ao eliminar **todos os inimigos**, o jogador vence a partida.
-   O pulo só pode ser executado quando o personagem estiver no chão.

------------------------------------------------------------------------

## Menu Principal

O jogo possui um menu inicial com os seguintes botões:

-   **Start Game**\
    Inicia uma nova partida.

-   **Sound: ON / OFF**\
    Liga ou desliga música e efeitos sonoros.\
    O botão fornece **feedback visual**:

    -   Verde: som ligado
    -   Vermelho: som desligado

-   **Exit**\
    Encerra o jogo.

------------------------------------------------------------------------

## Estrutura do Projeto

``` text
project/
│
├── main.py            # Código principal do jogo
│
├── images/             # Sprites do jogo
│   ├── hero_idle_0.png
│   ├── hero_idle_1.png
│   ├── hero_run_0.png
│   ├── hero_run_1.png
│   ├── enemy_0.png
│   └── enemy_1.png
│
├── sounds/             # Efeitos sonoros
│   ├── jump.wav
│   ├── hit.wav
│   └── enemy_die.wav
│
└── music/              # Música de fundo
    └── background.wav
```

------------------------------------------------------------------------

## Organização do Código

-   **AnimatedSprite**\
    Responsável pela animação contínua dos sprites.

-   **Player**\
    Controla movimento, pulo, colisão e animação do herói.

-   **Enemy**\
    Implementa inimigos com movimentação autônoma, separação e animação.

-   **Button**\
    Gerencia botões clicáveis do menu.

-   **Game**\
    Classe central que controla estados do jogo, áudio e fluxo geral.

-   **update / draw**\
    Funções principais do PgZero responsáveis pela lógica e
    renderização.

------------------------------------------------------------------------

## Observações Finais

Este projeto foi desenvolvido seguindo boas práticas de legibilidade e
arquitetura, com foco educacional, sendo adequado tanto para avaliação
quanto como material de referência para alunos iniciantes.

------------------------------------------------------------------------

**Autor:** Projeto desenvolvido de forma independente para o Teste de
Tutores.
