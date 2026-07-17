"""
Base de dados das 10 empresas fictícias utilizadas na atividade da Aula 2.
Mantida separada do front-end para facilitar manutenção e reuso
(ex: geração do documento em markdown, testes automatizados, etc).
"""

COMPANIES = {
    "LogiFlex Cargo Solutions": {
        "segmento": "Logística B2B (transporte rodoviário fracionado / last-mile industrial)",
        "resumo": (
            "Plataforma que conecta indústrias de médio porte a uma malha de transportadoras "
            "parceiras, cobrando comissão por rota fechada."
        ),
        "sintomas": (
            "Taxa de cotações aprovadas caiu de 61% para 34% em seis meses, mesmo com preços "
            "competitivos e prazo estável. NPS de atendimento pós-venda é alto (78), mas o "
            "cadastro de novas empresas está estagnado apesar do aumento de tráfego no site."
        ),
        "dados": "4.200 visitas/mês, conversão visita→cadastro de 1,1% (mercado: 3% a 5%), "
                 "resposta comercial ao lead em 46h.",
    },
    "Rede Ponto Certo Supermercados": {
        "segmento": "Varejo alimentar (rede regional, 38 lojas)",
        "resumo": (
            "Supermercados de bairro com posicionamento de preço competitivo e app de "
            "fidelidade lançado há 8 meses."
        ),
        "sintomas": (
            "Cadastro no app cresceu 240% no lançamento, mas resgate de cupons caiu de 22% "
            "para 6% em três meses. Ticket médio de usuários do app é 18% menor que o de "
            "clientes sem app."
        ),
        "dados": "190 mil usuários cadastrados, 41 mil cupons enviados/semana, "
                 "abertura de push notification: 3,2%.",
    },
    "ShopBoost Moda & Acessórios": {
        "segmento": "E-commerce de moda feminina (fast fashion)",
        "resumo": "Loja virtual própria + marketplace, tráfego pago intenso via redes sociais e influenciadoras.",
        "sintomas": (
            "CAC subiu 65% no trimestre; conversão do site em 0,9% (mercado: 1,8% a 2,5%); "
            "abandono de carrinho em 82%; CTR das campanhas é ótimo (4,1%)."
        ),
        "dados": "85 mil sessões/mês, 82% abandono de carrinho, checkout carrega em 6,4s.",
    },
    "IntegraSaaS Connect": {
        "segmento": "SaaS B2B de integração via API para e-commerces",
        "resumo": "Plataforma por assinatura que conecta ERPs, marketplaces e gateways de pagamento.",
        "sintomas": (
            "71% dos usuários em trial não completam a integração técnica e cancelam. "
            "Deals fechados na demo comercial: 58% (bom); churn nos primeiros 30 dias pagos: 39%."
        ),
        "dados": "Onboarding técnico médio: 9 dias (meta: 2 dias), 5,3 tickets de suporte/cliente no 1º mês, "
                 "documentação com 34 páginas.",
    },
    "AgroVision Insumos": {
        "segmento": "Distribuição B2B de insumos agrícolas",
        "resumo": (
            "Distribuidora regional (GO/MT) com representantes em campo, atendendo cooperativas "
            "e produtores rurais."
        ),
        "sintomas": (
            "Catálogo digital e chatbot no WhatsApp lançados, mas pedidos via canal digital são "
            "menos de 4% do total. Satisfação com representantes de campo é altíssima (9,2/10)."
        ),
        "dados": "1.100 acessos/mês ao catálogo digital, conversão do chatbot em pedido: 1,8%, "
                 "84% dos pedidos ainda fechados por telefone/visita.",
    },
    "FinCred Soluções": {
        "segmento": "Fintech de crédito para PMEs",
        "resumo": "Plataforma digital de análise de crédito via open finance com aprovação em até 24h.",
        "sintomas": (
            "Aprovação de crédito é alta e competitiva (68%), mas só 22% dos cadastros completam "
            "a conexão via open finance; usuários relatam não entender a etapa e temer segurança."
        ),
        "dados": "12.400 cadastros iniciados/mês, 22% concluem o open finance, "
                 "etapa leva 11 min (concorrentes: 3-4 min).",
    },
    "SaúdeAgora Telemedicina": {
        "segmento": "Healthtech (teleconsulta B2C e B2B2C)",
        "resumo": "Plataforma de teleconsulta por assinatura, vendida direto ao consumidor e como benefício corporativo.",
        "sintomas": (
            "Apenas 14% dos usuários com acesso via benefício corporativo ativam a conta no "
            "1º mês, contra 61% dos assinantes diretos. RH relata desconhecimento do benefício."
        ),
        "dados": "45 empresas parceiras, 38 mil vidas elegíveis, ativação corporativa 14% vs. "
                 "B2C direta 61%, NPS de quem usa: 71.",
    },
    "EduPro Certifica": {
        "segmento": "Edtech (cursos livres de certificação profissional)",
        "resumo": "Cursos curtos vendidos via funil de lançamento e fluxo evergreen.",
        "sintomas": (
            "Conversão de lead em venda é ótima (6,8%), mas conclusão do curso é de só 11% e "
            "reclamações de 'não era o que eu esperava' crescem a cada lançamento."
        ),
        "dados": "3.200 leads no último lançamento, conversão 6,8%, conclusão 11%, "
                 "nota pública caiu de 4,6 para 3,3 em um ano.",
    },
    "ImobTech Realty": {
        "segmento": "Proptech (marketplace de locação e venda de imóveis)",
        "resumo": "Marketplace que conecta imobiliárias parceiras a inquilinos/compradores via IA de recomendação.",
        "sintomas": (
            "Engajamento com recomendações de IA é altíssimo (CTR 38%, sessão média 14min), "
            "mas só 3% dos agendamentos retornam status pós-visita à plataforma."
        ),
        "dados": "22 mil buscas/mês, CTR de recomendações 38%, retorno de status pós-visita: 3%, "
                 "640 imobiliárias parceiras.",
    },
    "StreamPlay Media": {
        "segmento": "Streaming de conteúdo nacional (B2C)",
        "resumo": "Plataforma de streaming com plano único de assinatura e forte investimento em conteúdo original.",
        "sintomas": (
            "Trial converte bem (46%) e conteúdo tem ótima recepção orgânica, mas churn no "
            "2º mês pago é de 52% (mercado: 18% a 25%)."
        ),
        "dados": "Conversão trial→pago: 46%, churn mês 2: 52%, consumo médio semanal cai de "
                 "3,1h (mês 1) para 0,4h (mês 2).",
    },
}
