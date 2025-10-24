import pandas as pd
import numpy as np

# =========================
# Dados sintéticos
# =========================
#np.random.seed(42)
n_pedidos = 5000  # grande volume
capacidade_lote = 50

df = pd.DataFrame({
    'id': range(n_pedidos),
    'tempo_chegada': np.random.randint(0, 120, n_pedidos),
    'dispatch_window': np.random.randint(5, 15, n_pedidos),
    'priority_score': np.random.uniform(1, 10, n_pedidos),
    'sizeCategory': np.random.choice(['P','M','G'], n_pedidos, p=[0.3,0.4,0.3])
})
df['size_weight'] = df['sizeCategory'].map({'P':1,'M':2,'G':3})

# =========================
# Função de simulação por blocos
# =========================
def simular_blocos(df, metodo='fifo', alpha=1, beta=5, delta=0.5, gamma=2, bucket_interval=5):
    pedidos = df.copy()
    
    if metodo == 'buckets':
        # calcula score
        urgencia = 1 / ((pedidos['dispatch_window'] + 1) ** gamma)
        pedidos['score'] = alpha*pedidos['priority_score'] + beta*urgencia + delta*pedidos['size_weight']
        pedidos['bucket'] = (pedidos['score'] // bucket_interval).astype(int)
        # ordena por bucket decrescente e score decrescente
        pedidos = pedidos.sort_values(['bucket','score'], ascending=[False, False])
    else:  # fifo
        pedidos = pedidos.sort_values('tempo_chegada')
    
    # simula lotes
    tempos_expedicao = []
    lote_atual = []
    carga = 0
    tempo = 0
    for idx, row in pedidos.iterrows():
        if carga + row['size_weight'] > capacidade_lote:
            # despacha lote
            for i in lote_atual:
                tempos_expedicao.append((i, tempo))
            lote_atual = []
            carga = 0
            tempo += 1  # cada lote = 1 unidade de tempo
        lote_atual.append(row['id'])
        carga += row['size_weight']
    
    # despacha último lote
    for i in lote_atual:
        tempos_expedicao.append((i, tempo))
    
    # marca tempo de expedição
    temp_df = pd.DataFrame(tempos_expedicao, columns=['id','tempo_expedicao'])
    merged = pd.merge(pedidos, temp_df, on='id')
    
    # calcula métricas
    merged['atraso'] = ((merged['tempo_expedicao'] - merged['tempo_chegada']) - merged['dispatch_window']).clip(lower=0)
    atraso_medio = merged['atraso'].mean()
    percentual_sla = (merged['atraso'] > 0).mean() * 100
    aproveitamento = merged['size_weight'].sum() / ((merged['tempo_expedicao'].max()+1)*capacidade_lote) * 100
    
    return atraso_medio, percentual_sla, aproveitamento

# =========================
# Executa simulação rápida
# =========================
res_buckets = simular_blocos(df, metodo='buckets')
res_fifo = simular_blocos(df, metodo='fifo')

print("=== Resultado Buckets ===")
print(f"Atraso médio: {res_buckets[0]:.2f}")
print(f"% SLA estourado: {res_buckets[1]:.2f}%")
print(f"Aproveitamento médio: {res_buckets[2]:.2f}%\n")

print("=== Resultado FIFO ===")
print(f"Atraso médio: {res_fifo[0]:.2f}")
print(f"% SLA estourado: {res_fifo[1]:.2f}%")
print(f"Aproveitamento médio: {res_fifo[2]:.2f}%")
