gantt
    title Cronograma da POC de Plataforma de Dados para E-commerce
    dateFormat  YYYY-MM-DD
    axisFormat  %d/%m

    section Planejamento
    Leitura do case e definição do escopo           :done, p1, 2026-04-09, 1d
    Escolha da base e narrativa de negócio          :done, p2, 2026-04-09, 1d
    Estruturação do repositório e README inicial    :p3, after p2, 1d

    section Ingestão e Governança
    Preparação e validação inicial da base          :d1, after p3, 1d
    Ingestão da base na Dadosfera                   :d2, after d1, 1d
    Catalogação e organização em camadas            :d3, after d2, 1d

    section Qualidade e Processamento
    Definição das regras de data quality            :q1, after d3, 1d
    Execução do data quality e análise de achados   :q2, after q1, 1d
    Padronização mínima dos dados                   :q3, after q2, 1d
    Geração de features com LLM                     :g1, after q3, 1d

    section Analytics
    Modelagem dimensional                           :m1, after g1, 1d
    Criação de views e queries analíticas           :m2, after m1, 1d
    Construção do dashboard                         :m3, after m2, 1d

    section Operacionalização
    Construção do pipeline                          :o1, after m3, 1d
    Desenvolvimento do data app                     :o2, after o1, 1d

    section Encerramento
    Consolidação da documentação final              :f1, after o2, 1d
    Gravação da apresentação e revisão final        :f2, after f1, 1d
