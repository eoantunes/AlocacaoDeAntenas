# AlocacaoDeAntenas
Projeto desenvolvido no curso de metrado profissional e vinculado ao Projeto CCOp Mv do Exército Brasileiro - PPCA/UnB - 2020

O problema de alocação dos nós de acesso do CCOp Mv consiste em selecionar, dentro de uma região limitada à área de atuação da tropa terrestre, as posições das viaturas de antenas que maximizam a área de cobertura dos seus sistemas de comunicação. 

Este trabalho trata do problema de alocação de estações rádio base (ERBs) dos nós de acesso do CCOp móvel para o sistema de telefonia celular de 4G LTE militar. Esse problema consiste em dada uma determinada região geográfica, onde se encontram desdobradas as tropas militares e de segurança pública no terreno, dispor antenas de modo a cobrir a maior área possível da região em estudo, além de garantir um alto nível de confiabilidade, e qualidade de serviço nas operações que necessitam de comunicações críticas. Neste trabalho foi proposto um sistema de apoio à decisão baseado em programação linear inteira que resolve de maneira ótima este problema. Foi proposto um Data Set para teste e avaliação dos resultados. A complexidade do algoritmo e das estruturas de dados empregadas foi analisada. O algoritmo apresentado calcula o raio de alcance da ERB, a quantidade mínima de ERBs necessárias para cobrir a região em estudo e a localização de cada ERB.

Inicialmente o problema foi modelado matematicamente e implementado no solver ORTools.

Foi criado um Data Set para testes e avaliações:

	---> 200 pontos de demanda: https://www.google.com/maps/d/u/2/edit?mid=1BZZA8-3ENd-8RyV27ySG6BTBSx3n7zpW&usp=sharing
	
	---> 50 possíveis posições das antenas: arquivo KMZ

A última etapa foi a elaboração de uma interface gráfica em Django que facilitasse a operação desta ferramenta.
Esta etapa contou com a integração da biblioteca folium, GeoPy e do algoritmo de otmização apresentado em main.py. A aplicação foi incorporada ao framework Django, conforme arquivos em /ProjetoDjango/AlocAntenas.

Também foi desenvolvido um algoritmo genético para melhorar o desempenho do algoritmo exato e seus detalhes podem ser visualizados no segundo artigo abaixo referenciado.

Mais detalhes podem ser obtidos nos artigos disponíveis para visualização em: https://pt.overleaf.com/read/qgshxwkmhtdt e https://www.overleaf.com/read/wrtvtyzkrdvz.
