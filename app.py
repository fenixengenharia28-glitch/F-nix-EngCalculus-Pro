import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Quantitativo de Materiais", page_icon="🏗️", layout="centered")

# Inicializar o banco de dados na sessão (para não sumir ao recarregar)
if "historico" not in st.session_state:
    st.session_state.historico = []

st.title("🏗️ Quantitativo de Materiais")
st.subheader("Calcule e salve os materiais da sua obra rapidamente")

# Menu de Navegação simples
aba1, aba2 = st.tabs(["🧮 Calculadora", "📋 Relatórios Salvos"])

with aba1:
    st.markdown("### Escolha o tipo de serviço")
    
    # Seleção do serviço
    servico = st.selectbox(
        "Selecione o serviço:",
        ["Alvenaria de Vedação (Tijolo 9x19x19)", "Concreto (Traço 1:2:3 - Fundação/Laje)", "Pintura (2 Demãos)"]
    )
    
    # Campos dinâmicos dependendo do serviço
    if "Alvenaria" in servico:
        area = st.number_input("Área da parede (m²):", min_value=0.1, value=10.0, step=1.0)
        # Coeficientes médios por m²
        tijolos = round(area * 25)
        cimento = round(area * 5, 2)
        areia = round(area * 0.02, 3)
        
        st.info(f"**Estimativa para {area} m²:**\n- 🧱 {tijolos} Tijolos\n- 🪨 {cimento} kg de Cimento\n- ⏳ {areia} m³ de Areia")
        
        material_resumo = f"{tijolos} Tijolos, {cimento}kg Cimento, {areia}m³ Areia"

    elif "Concreto" in servico:
        volume = st.number_input("Volume de concreto necessário (m³):", min_value=0.1, value=1.0, step=0.1)
        # Coeficientes médios por m³ para traço convencional
        cimento_sacos = round(volume * 7)
        areia_m3 = round(volume * 0.6, 2)
        brita_m3 = round(volume * 0.6, 2)
        
        st.info(f"**Estimativa para {volume} m³:**\n- 🥡 {cimento_sacos} Sacos de Cimento (50kg)\n- ⏳ {areia_m3} m³ de Areia\n- 🪨 {brita_m3} m³ de Brita")
        
        material_resumo = f"{cimento_sacos} sacos Cimento, {areia_m3}m³ Areia, {brita_m3}m³ Brita"

    elif "Pintura" in servico:
        area_pintura = st.number_input("Área de pintura (m²):", min_value=0.1, value=20.0, step=1.0)
        # Rendimento médio (duas demãos)
        lata_tinta = round((area_pintura / 75), 2)  # Considerando lata de 18L rendendo ~150m² por demão
        
        st.info(f"**Estimativa para {area_pintura} m²:**\n- 🎨 {lata_tinta} Latas de Tinta (18L)")
        
        material_resumo = f"{lata_tinta} Latas de Tinta (18L)"

    # Nome da obra/ambiente para salvar
    identificacao = st.text_input("Nome da Obra / Ambiente:", placeholder="Ex: Casa do João - Sala")
    
    if st.button("💾 Salvar no Relatório"):
        if identificacao.strip() == "":
            st.error("Por favor, digite um nome para identificar a obra antes de salvar.")
        else:
            # Salva os dados na lista
            st.session_state.historico.append({
                "Obra/Ambiente": identificacao,
                "Serviço": servico,
                "Materiais Calculados": material_resumo
            })
            st.success("Cálculo salvo com sucesso! Confira na aba 'Relatórios Salvos'.")

with aba2:
    st.markdown("### Histórico de Cálculos da Obra")
    
    if len(st.session_state.historico) == 0:
        st.warning("Nenhum cálculo foi salvo ainda.")
    else:
        # Transforma a lista em uma tabela visual do Pandas
        df = pd.DataFrame(st.session_state.historico)
        st.dataframe(df, use_container_width=True)
        
        if st.button("🗑️ Limpar Todos os Registros"):
            st.session_state.historico = []
            st.rerun()
