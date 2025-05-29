import machine
import random
import utime

# --- CONFIGURAÇÃO DE HARDWARE ---
# Define os pinos GPIO para os componentes do jogo.

# Configuração dos LEDs do jogo (saídas)
leds = [
    machine.Pin(16, machine.Pin.OUT),  # Amarelo (GPIO16)
    machine.Pin(17, machine.Pin.OUT),  # Azul (GPIO17)
    machine.Pin(15, machine.Pin.OUT)   # Vermelho (GPIO15)
]

# Configuração dos botões do jogo (entradas com pull-up interno)
botoes = [
    machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP), # Botão 1 (GPIO13)
    machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP), # Botão 2 (GPIO18)
    machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)  # Botão 3 (GPIO12)
]

# --- CONFIGURAÇÃO E MAPEAMENTO DOS DISPLAYS DE 7 SEGMENTOS (CATODO COMUM) ---

# Mapeamento dos padrões de acendimento dos segmentos para cada dígito (0-9 e 'off').
# Para displays de Catodo Comum, enviar HIGH (1) para o pino do segmento o acende.
# Ordem dos bits na tupla: (a, b, c, d, e, f, g).
digits_patterns = {
    '0': (1, 1, 1, 1, 1, 1, 0),
    '1': (0, 1, 1, 0, 0, 0, 0),
    '2': (1, 1, 0, 1, 1, 0, 1),
    '3': (1, 1, 1, 1, 0, 0, 1),
    '4': (0, 1, 1, 0, 0, 1, 1),
    '5': (1, 0, 1, 1, 0, 1, 1),
    '6': (1, 0, 1, 1, 1, 1, 1),
    '7': (1, 1, 1, 0, 0, 0, 0),
    '8': (1, 1, 1, 1, 1, 1, 1),
    '9': (1, 1, 1, 1, 0, 1, 1),
    'off': (0, 0, 0, 0, 0, 0, 0) # Apaga todos os segmentos
}

# Ordem dos segmentos conforme esperado pelas tuplas em digits_patterns.
segment_order_for_bits = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

# Configuração dos pinos GPIO para cada segmento dos dois displays (unidades e dezenas).
all_display_configs = [
    {
        'name': 'unidades', # Display da direita (menos significativo)
        'pins': {
            'a': machine.Pin(0, machine.Pin.OUT), 'b': machine.Pin(1, machine.Pin.OUT),
            'c': machine.Pin(2, machine.Pin.OUT), 'd': machine.Pin(3, machine.Pin.OUT),
            'e': machine.Pin(4, machine.Pin.OUT), 'f': machine.Pin(6, machine.Pin.OUT),
            'g': machine.Pin(5, machine.Pin.OUT),
        }
    },
    {
        'name': 'dezenas', # Display da esquerda (mais significativo)
        'pins': {
            'a': machine.Pin(7, machine.Pin.OUT), 'b': machine.Pin(8, machine.Pin.OUT),
            'c': machine.Pin(9, machine.Pin.OUT), 'd': machine.Pin(10, machine.Pin.OUT),
            'e': machine.Pin(11, machine.Pin.OUT), 'f': machine.Pin(19, machine.Pin.OUT),
            'g': machine.Pin(20, machine.Pin.OUT)
        }
    }
]


# --- VARIÁVEIS DE ESTADO DO JOGO ---
# Controlam o fluxo e as regras do jogo.
pontuacao = 0
vidas = 3
jogo_ativo = True       # Flag que mantém o loop principal do jogo rodando.
led_atual = -1          # Índice do LED (0-2) que está aceso, representando a "marmota".
ultimo_botao_pressionado_tempo = [0, 0, 0] # Timestamps para debounce de cada botão.
tempo_inicio_led = 0    # Timestamp de quando a "marmota" atual apareceu.

# Sistema de fases para progressão de dificuldade.
fase = 1
proxima_fase = 5       # Pontuação necessária para avançar de fase.
TEMPO_BASE = 3000      # Tempo (ms) que a marmota fica acesa (diminui com as fases).

# Constantes do jogo
PONTOS_ACERTO = 1      # Pontos ganhos por acerto.
DEBOUNCE_TIME = 300    # Intervalo (ms) para evitar leituras múltiplas de um botão.


# --- FUNÇÕES DE CONTROLE DO DISPLAY ---

# Apaga completamente ambos os displays.
def turn_off_all_displays():
    for display_conf in all_display_configs:
        for pin_obj in display_conf['pins'].values():
            pin_obj.value(0) # Para Catodo Comum, LOW (0) desliga o segmento.

# Exibe um único dígito (0-9 ou 'off') em um display específico.
def _display_single_digit_on_display(display_conf, digit_char, show_dp=False):
    # Limpa o display antes de acender novos segmentos.
    for pin_obj in display_conf['pins'].values():
        pin_obj.value(0)

    if digit_char not in digits_patterns:
        # Ação para dígito inválido, previne erro mas loga no console.
        print(f"Dígito inválido para display {display_conf['name']}: {digit_char}")
        return

    segment_values = digits_patterns[digit_char]

    # Acende os segmentos corretos conforme o padrão do dígito.
    for i, seg_name in enumerate(segment_order_for_bits):
        display_conf['pins'][seg_name].value(segment_values[i])
    
    # Controle do ponto decimal (não utilizado neste jogo, mas a função suporta).
    if 'dp' in display_conf['pins']:
        display_conf['pins']['dp'].value(1 if show_dp else 0)

# Exibe a pontuação (0-99) nos dois displays de 7 segmentos.
def display_score(score_value):
    # Limita a pontuação a 99 para caber nos dois dígitos.
    score_value = score_value % 100

    tens_digit = score_value // 10  # Dígito das dezenas.
    units_digit = score_value % 10 # Dígito das unidades.

    # Exibe dezenas no display da esquerda e unidades no da direita.
    _display_single_digit_on_display(all_display_configs[1], str(tens_digit))
    _display_single_digit_on_display(all_display_configs[0], str(units_digit))


# --- FUNÇÕES DO JOGO ---

# Gerencia a transição para a próxima fase do jogo.
def atualizar_fase():
    global fase, TEMPO_BASE, vidas, proxima_fase, pontuacao
    
    # Efeito visual para indicar transição de fase (LEDs piscam, displays mostram score).
    for _ in range(3):
        for led in leds:
            led.on()
        turn_off_all_displays()
        utime.sleep_ms(150)
        for led in leds:
            led.off()
        display_score(pontuacao)
        utime.sleep_ms(150)
    
    fase += 1
    # Aumenta a dificuldade reduzindo o tempo de reação (mínimo 1 segundo).
    TEMPO_BASE = max(1000, TEMPO_BASE - 500)
    vidas = 3 # Vidas são resetadas no início de cada nova fase.
    proxima_fase += 5 # Define a nova meta de pontuação.
    
    print(f"\n--- FASE {fase} ---")
    # ... (prints de console para depuração/informação)
    
    # Contagem regressiva (3-2-1) exibida em ambos os displays antes da fase iniciar.
    print("Nova fase começando em...")
    for i in range(3, 0, -1):
        print(f"{i}...")
        _display_single_digit_on_display(all_display_configs[0], str(i))
        _display_single_digit_on_display(all_display_configs[1], str(i))
        utime.sleep(1)
            
    # Limpa os LEDs e displays e mostra a pontuação atual antes de iniciar.
    for led in leds:
        led.off()
    turn_off_all_displays()
    display_score(pontuacao)
    utime.sleep(0.5)
    
    acender_novo_led() # Inicia a primeira rodada da nova fase.

# Acende uma "marmota" (LED) aleatória e marca o tempo.
def acender_novo_led():
    global led_atual, tempo_inicio_led
    # Garante que todos os LEDs estejam apagados antes de acender um novo.
    for led in leds:
        led.off()
        
    led_atual = random.randint(0, 2) # Escolhe um dos 3 LEDs aleatoriamente.
    leds[led_atual].on()
    tempo_inicio_led = utime.ticks_ms() # Registra quando o LED acendeu.
    # ultimo_botao_pressionado_tempo é resetado individualmente em verificar_botoes.

# Verifica o estado dos botões, processa acertos/erros e debounce.
def verificar_botoes():
    global pontuacao, vidas, jogo_ativo, ultimo_botao_pressionado_tempo
    tempo_atual = utime.ticks_ms()
    
    for i in range(3): # Itera sobre os 3 botões.
        # Lógica de debounce: processa o botão apenas se DEBOUNCE_TIME tiver passado.
        if botoes[i].value() == 0 and utime.ticks_diff(tempo_atual, ultimo_botao_pressionado_tempo[i]) > DEBOUNCE_TIME:
            ultimo_botao_pressionado_tempo[i] = tempo_atual # Atualiza o timestamp do debounce para este botão.
            
            if i == led_atual: # Jogador acertou a marmota correta.
                pontuacao += PONTOS_ACERTO
                print(f"Acerto! +{PONTOS_ACERTO} (Total: {pontuacao})")
                display_score(pontuacao)
                
                if pontuacao >= proxima_fase:
                    atualizar_fase() # Passa para a próxima fase.
                else:
                    acender_novo_led() # Continua na fase atual, nova marmota.
                return True # Ação de acerto processada.
            else: # Jogador pressionou o botão errado.
                vidas -= 1
                print(f"Errou! Vidas: {vidas}")
                
                if vidas <= 0:
                    fim_do_jogo() # Fim de jogo se não houver mais vidas.
                else:
                    acender_novo_led() # Nova marmota, jogador ainda tem vidas.
                return False # Ação de erro processada.
    return None # Nenhum botão relevante foi pressionado e processado nesta chamada.

# Encerra o jogo e exibe a pontuação final com efeitos visuais.
def fim_do_jogo():
    global jogo_ativo
    
    jogo_ativo = False # Interrompe o loop principal do jogo.
    
    for led in leds:
        led.off() # Apaga todas as marmotas.
    
    print(f"\n--- FIM DE JOGO ---")
    print(f"Pontuação Final: {pontuacao}")
    
    display_score(pontuacao) # Mostra a pontuação final.
    utime.sleep(3)
    
    # Efeito visual de "Game Over" piscando LEDs e displays.
    for _ in range(5):
        for led_obj in leds:
            led_obj.toggle()
        turn_off_all_displays()
        utime.sleep_ms(200)
        display_score(pontuacao) # Reexibe a pontuação durante o pisca-pisca.
        utime.sleep_ms(200)
            
    # Limpa LEDs e displays ao final do efeito.
    for led in leds:
        led.off()
    turn_off_all_displays()

# --- INÍCIO DO JOGO ---
# Bloco de inicialização principal do jogo.

print("WHACK THE MOLE!")
# ... (instruções no console)

# Prepara o estado inicial dos componentes visuais.
turn_off_all_displays()
for led in leds:
    led.off()

# Informações iniciais da Fase 1 e contagem regressiva.
print(f"\n--- FASE {fase} ---")
# ... (prints de console)
print("Preparando para começar...")
for i in range(3, 0, -1):
    print(f"{i}...")
    # Contagem regressiva exibida em ambos os displays.
    _display_single_digit_on_display(all_display_configs[0], str(i))
    _display_single_digit_on_display(all_display_configs[1], str(i))
    utime.sleep(1)

# Exibe a pontuação inicial (00) após a contagem.
display_score(pontuacao)
utime.sleep(0.5)

acender_novo_led() # Acende a primeira marmota.

# --- LOOP PRINCIPAL DO JOGO ---
# Mantém o jogo rodando enquanto 'jogo_ativo' for True.
while jogo_ativo:
    # Verifica se o tempo para acertar a marmota atual esgotou.
    if utime.ticks_diff(utime.ticks_ms(), tempo_inicio_led) > TEMPO_BASE:
        vidas -= 1
        print(f"Tempo esgotado! Vidas restantes: {vidas}")
        
        if vidas <= 0:
            fim_do_jogo()
        else:
            acender_novo_led() # Nova rodada se ainda houver vidas.
        
    if not jogo_ativo: # Se fim_do_jogo() foi chamado por timeout.
        break

    # Verifica e processa os botões pressionados.
    verificar_botoes()
            
    if not jogo_ativo: # Se fim_do_jogo() foi chamado por erro em verificar_botoes().
        break
            
    utime.sleep_ms(10) # Pequeno delay para otimizar o uso da CPU.

print("Obrigado por jogar!")