# 𝐃𝐚𝐬𝐡𝐛𝐨𝐚𝐫𝐝 𝐄𝐱𝐩𝐥𝐨𝐫𝐚𝐭𝐨𝐫𝐢𝐨: 𝐁𝐞𝐧𝐞𝐟𝐢𝐜𝐢𝐨𝐬 𝐈𝐍𝐒𝐒 

O objetivo deste projeto é disponibilizar um dashboard interativo com dados dos benefícios concedidos pelo INSS durante um período de 10 meses, entre junho de 2024 e março de 2025.

---

# ▸ ʙᴀsᴇ ᴅᴇ ᴅᴀᴅᴏs

As bases utilizadas estão disponíveis no [site do governo](https://dados.gov.br/dados/conjuntos-dados/perfil-das-unidades-plano-de-dados-abertos-jun-2023-a-jun-2025), estão separadas por mês e os metadados também estão disponíveis no site. Para iniciar o tratamento, verifiquei se as bases possuem a mesma estrutura. 

>➛ Caso for extraí-las diretamente do site, se atente ao fato de que algumas bases utilizam a primeira linha da tabela para título e nem sempre possuem as mesmas colunas e os arquivos presentes no repositório já estão com os devidos ajustes.

---

## ▸ ᴄᴏᴍᴏ ᴏ ᴛʀᴀᴛᴀᴍᴇɴᴛᴏ ᴅᴏs ᴅᴀᴅᴏs ғᴏɪ ʀᴇᴀʟɪᴢᴀᴅᴏ?

Após o download das bases, os arquivos foram salvos em excel na pasta bases_inss e todo o tratamento foi feito no Python usando o VS Code.

<p align="center">
  <img src="imagens/1.png" alt="Resumo do Tratamento de Dados (Part. 1)" style="width:45%; margin-right: 2%;"/>
  <img src="imagens/2.png" alt="Resumo do Tratamento de Dados (Part. 2)" style="width:45%;"/>
</p>


1. Extração e Consolidação dos Dados

2. Limpeza e Padronização Inicial

3. Engenharia de Atributos e Tratamento de Dados Específicos

4. Otimização da Estrutura dos Dados

5. Criação de Indicadores e Novas Categorias

6. Agregação e Normalização dos Dados

7. Exportação do Resultado

>➛ Primeiro deve-se rodar o notebook para gerar o arquivo da base final e conseguir rodar o streamlit

---

## ▸ ᴄᴏᴍᴏ ᴏ ᴅᴀsʜʙᴏᴀʀᴅ ғᴏɪ ғᴇɪᴛᴏ?

O Dashboard foi feito através do *Streamlit* seguindo as etapas abaixo:

<p align="left">
  <img src="imagens/3.png" alt="Resumo da Construção do Dashboard" style="width:45%;"/>
</p>

1. Configuração Inicial e Estilo da Página

2. Carregamento e Pré-processamento dos Dados

3. Criação de Filtros na Barra Lateral (sidebar)

4. Aplicação dos Filtros aos Dados

5. Exibição de Indicadores Chave (KPIs) e Gráficos

---

## ▸ ᴅᴀsʜʙᴏᴀʀᴅ ᴇ ɪɴsɪɢʜᴛs

<p align="left">
  <img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExeGQ5Y283ODg2aG5jem9yMDFtOWJxZHZnZjR2MWU3eDU3djVubXN3OSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/OYzeSIbgJ12UeBy0RE/giphy.gif" alt="Demonstração do Projeto" style="width: 600px;"/>
</p>

O dashboard evidencia importantes distinções de gênero em nossa sociedade quando se analisam os benefícios concedidos por diferentes categorias de CID. 

No gráfico "Taxa por Mês e Sexo", ao aplicar o filtro para "Transtornos mentais e comportamentais", observa-se que a taxa de mulheres beneficiárias é substancialmente mais elevada em comparação aos homens. Em contrapartida, ao filtrar por "Traumatismos e envenenamentos", o padrão se inverte, revelando uma taxa de benefícios marcadamente maior para o público masculino.

### ❯ ᴄᴏɴᴛᴀᴛᴏs ᴅᴏ ᴀᴜᴛᴏʀ :

<div>
<a href="https://www.linkedin.com/in/beckzaguiar/" target="_blank"><img loading="lazy" src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a>
<a href = "mailto:beca.aguiar12@gmail.com"><img loading="lazy" src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" target="_blank"></a>
<a href="https://www.instagram.com/b.eckz" target="_blank"><img loading="lazy" src="https://img.shields.io/badge/-Instagram-%23E4405F?style=for-the-badge&logo=instagram&logoColor=white" target="_blank"></a>
<a href="https://www.youtube.com/@beckzaguiar134/playlists" target="_blank"><img loading="lazy" src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" target="_blank"></a>  
</div>