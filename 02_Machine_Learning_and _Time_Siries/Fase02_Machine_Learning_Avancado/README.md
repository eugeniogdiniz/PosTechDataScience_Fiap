# Modelos de Classificação

## Dúvidas pesquisadas

#### O que é KNeighborsClassifier ?

O KNeighborsClassifier é um algoritmo de aprendizado de máquina utilizado para classificação supervisionada. Ele faz parte da família de algoritmos conhecida como "aprendizado baseado em instância" ou "aprendizado baseado em vizinhos".

O funcionamento desse classificador se baseia na proximidade dos dados no espaço de características. A ideia é atribuir uma classe a um novo ponto de dados com base nas classes dos vizinhos mais próximos. O "K" em KNeighborsClassifier refere-se ao número de vizinhos mais próximos que são considerados para determinar a classe de um novo ponto de dados.

Por exemplo, se K for igual a 3, o algoritmo irá analisar os três vizinhos mais próximos do novo ponto de dados e atribuir a classe mais comum entre esses três vizinhos ao novo ponto.

Este algoritmo é bastante utilizado em problemas de classificação onde a estrutura dos dados sugere que pontos semelhantes devem pertencer à mesma classe. No entanto, é importante considerar o ajuste correto do parâmetro K para obter os melhores resultados de classificação para um conjunto de dados específico.

#### Qual é a diferença dele para o K-means?


O KNeighborsClassifier e o algoritmo K-means são usados em contextos diferentes de aprendizado de máquina e têm propósitos distintos:

KNeighborsClassifier: É um algoritmo de classificação supervisionada. Ele usa os rótulos das classes dos dados de treinamento para prever a classe de novos pontos de dados com base na proximidade desses pontos aos vizinhos mais próximos no espaço de características. Ele não procura encontrar grupos nos dados, mas sim classificar novos pontos com base na similaridade com os pontos já rotulados.

K-means: É um algoritmo de agrupamento não supervisionado. Ele agrupa os dados em um número fixo de clusters (representados por "K") com base na similaridade dos atributos. O K-means tenta particionar os dados em K grupos distintos, minimizando a variação dentro dos clusters e maximizando a variação entre os clusters. Ele não usa rótulos de classe como o KNeighborsClassifier, pois é um algoritmo não supervisionado e não trabalha com dados rotulados.

Em resumo, enquanto o KNeighborsClassifier é usado para classificar novos dados com base na similaridade com dados de treinamento rotulados, o K-means é usado para agrupar dados não rotulados em clusters com base na similaridade dos atributos, sem se preocupar com rótulos de classe.