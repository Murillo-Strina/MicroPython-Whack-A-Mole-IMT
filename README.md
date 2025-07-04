# Whack-A-Mole com MicroPython 🐹

Implementação do jogo Whack-A-Mole usando MicroPython e Raspberry Pi Pico. Projeto realizado para a disciplina de Microcontroladores e Sistemas Embarcados no Instituto Mauá de Tecnologia.

Este projeto consiste no desenvolvimento de uma versão eletrônica do clássico jogo Whack-A-Mole, utilizando MicroPython no microcontrolador Raspberry Pi Pico. O objetivo do jogador é "acertar" as "marmotas", representadas por LEDs que acendem aleatoriamente em diferentes posições. O jogador utiliza botões correspondentes para registrar os acertos. O sistema é montado em uma estrutura de caixa feita em MDF para abrigar a protoboard e os componentes, e conta com displays para feedback de pontuação e status do jogo.

## Componentes Utilizados 🛠️

* Microcontrolador Raspberry Pi Pico
* 3 Botões Push Button (C&K)
* 3 LEDs difusos 5mm
* 2 Displays de 7 segmentos (para pontuação e status do jogo)
* Resistores
* Capacitores (para debounce dos botões, ajudando a evitar múltiplos registros com um único clique)
* Protoboard (para montagem do circuito)
* Jumpers Macho-Macho e Macho-Fêmea (para as conexões)
* Estrutura/Caixa em MDF (para o suporte físico e montagem do jogo)

## Custo Médio de Produção 💲

* Raspberry pi pico: R$46,99
* Botão push button C&K: R$ 28,00 por unidade / R$ 84,00 total
* LED difuso 5mm: R$0,14 por unidade / R$0,42 total
* Display 7 segmentos: R$2,37 por unidade / R$4,74 total
* Resistor 200 Ohm: R$ 2,84
* Resistor 300 Ohm: R$ 0,61 por unidade / R$ 1,22 total
* Capacitores 10nf / 250v: R$ 1,49 por unidade / R$ 4,47
* Protoboard 830 pontos: R$ 10,97
* Jumpers (kit de 40 unidades): R$ 9,00
* MDF: R$ 5,26 para área total
* Custo total: R$ 169,91

## Requisitos 📜

* **UR01 (Obrigatório):** O sistema deve ser construído com componentes eletrônicos de fácil acesso, montado em uma protoboard e acondicionado em uma estrutura de MDF.
* **UR02 (Obrigatório):** LEDs devem acender em posições aleatórias e por tempo determinado para simular o aparecimento das "marmotas".
* **UR03 (Obrigatório):** O jogador deve conseguir "acertar" uma marmota pressionando o botão correspondente ao LED aceso dentro do tempo estipulado.
* **UR04 (Obrigatório):** O sistema deve registrar os acertos e erros do jogador de forma precisa.
* **UR05 (Obrigatório):** A pontuação do jogador deve ser atualizada e exibida nos displays de 7 segmentos.
* **UR06 (Obrigatório):** O status do jogo deve ser claramente comunicado ao jogador:
    * Displays de 7 segmentos indicarão o início do jogo (contagem regressiva), a pontuação, e o fim de jogo (exibindo a pontuação final e participando de efeitos visuais).
    * LEDs de jogo fornecerão feedback visual durante transições de fase (piscando em sequência) e no encerramento do jogo (piscando para indicar "Game Over").
* **UR07 (Obrigatório):** Utilizar MicroPython como a linguagem de programação para o Raspberry Pi Pico.
* **UR08 (Desejável):** O jogo deve apresentar níveis de dificuldade progressiva, com o tempo para acertar as marmotas diminuindo a cada nova fase.

## Funcionalidades 🕹

* Ao iniciar, o jogo realiza uma contagem regressiva (3, 2, 1), exibida em ambos os displays, seguida pela exibição da pontuação inicial (00).
* Uma "marmota" (representada por um dos três LEDs) acende em uma posição escolhida aleatoriamente. Esta permanece acesa por um tempo limite, que diminui conforme o jogador avança de fase.
* O jogador deve pressionar o botão correspondente à "marmota" (LED aceso) antes que o tempo limite da rodada se esgote para registrar um acerto.
* Cada acerto correto incrementa a pontuação do jogador em `+1` ponto. A nova pontuação é imediatamente atualizada e exibida nos dois displays.
* Pressionar o botão incorreto ou não realizar nenhuma ação antes que o tempo da rodada se esgote resulta na perda de uma vida. O jogador inicia com 3 vidas, que são restauradas no começo de cada nova fase.
* O jogo avança para uma nova fase quando o jogador atinge a meta de pontuação estabelecida (inicialmente 5 pontos, aumentando 5 pontos a cada fase). A transição de fase é marcada por um efeito visual nos LEDs e uma nova contagem regressiva nos displays.
* A dificuldade aumenta a cada fase, pois o tempo disponível para acertar a marmota (`TEMPO_BASE`) é reduzido (mínimo de 1 segundo).
* O jogo termina quando o jogador perde todas as vidas. A pontuação final é então exibida nos displays, seguida por um efeito visual de "Fim de Jogo" utilizando tanto os LEDs quanto os displays.

## Diagrama de Blocos 📊

![Diagrama de Blocos do Projeto](https://github.com/user-attachments/assets/8531ee9b-5d12-4b4d-affe-22301ee569c8)

## Galeria do Projeto 📸🎬

Nesta seção, apresentamos algumas imagens das etapas de desenvolvimento do nosso Whack-A-Mole, desde os protótipos iniciais até a montagem final, além de um vídeo demonstrando o jogo em funcionamento.

### Prototipagem e Desenvolvimento

Esta seção mostra a evolução do nosso projeto Whack-A-Mole, desde os testes iniciais em protoboard até a construção da estrutura final.

**1. Montagem Inicial e Testes em Protoboard**

![Protótipo inicial do Whack-A-Mole em protoboard](https://github.com/user-attachments/assets/f8051607-cc44-425b-a89e-044e488cff90)

Registro da fase inicial de montagem e testes do circuito Whack-A-Mole. Nesta etapa, focamos na validação das conexões elétricas entre o Raspberry Pi Pico, LEDs, botões e displays na protoboard, além de testar a funcionalidade básica de cada componente.

**2. Desenvolvimento da Estrutura em MDF**

![Estrutura da caixa do Whack-A-Mole em MDF](https://github.com/user-attachments/assets/85d055eb-1b04-4773-be3f-c6b85cf16fd7)

A estrutura que abriga todo o circuito do nosso Whack-A-Mole. Utilizamos MDF como material principal devido à sua facilidade de modelagem e acabamento. Cada face da caixa foi desenhada no software CAD SolidWorks, permitindo um planejamento preciso dos encaixes e aberturas para os LEDs, botões e displays.

**3. Integração Final do Circuito e Acabamento**

![Construção completa do projeto](https://github.com/user-attachments/assets/ff81260c-bd76-4f68-8d3e-c515afdd9ab1)

Nesta etapa, o circuito eletrônico foi cuidadosamente integrado à estrutura de MDF, resultando em um design coeso e funcional para o Whack-A-Mole. É importante notar que os pequenos botões visíveis na imagem serviram apenas para testes iniciais, sendo substituídos na versão final por botões push button C&K maiores, otimizando a jogabilidade.

### Vídeo do Projeto completo

https://github.com/user-attachments/assets/b5f4ae2c-0bf5-4c18-a005-e4c2faa4b4fc

## Integrantes 💻

* Pedro Campos Dec | 22.00787-3
* Guilherme Martins Souza Paula | 22.00006-2
* Murillo Penha Strina | 22.00730-0
* Lucas Olivares Borges da Silva | 22.00889-6

<!--![FotoIntegrantes](https://github.com/user-attachments/assets/0daaaff0-ccd7-4948-a823-202e7f7016ec)"-->

