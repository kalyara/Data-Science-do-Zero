#!/usr/bin/env python
# coding: utf-8

# # Motivação Hipotética: DataSciencester
# 
# ### Encontrando Conectores-Chave

# In[ ]:


users =[
    {"id": 0, "name": "Hero"},
    {"id": 1, "name": "Dunn"},
    {"id": 2, "name": "Sue"},
    {"id": 3, "name": "Chi"},
    {"id": 4, "name": "Thor"},
    {"id": 5, "name": "Clive"},
    {"id": 6, "name": "Hicks"},
    {"id": 7, "name": "Devin"},
    {"id": 8, "name": "Kate"},
    {"id": 9, "name": "Klein"},
]


# In[3]:


friendship_pairs = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (5, 6), (5, 7), (6, 8), (7, 8), (8, 9)]


# In[4]:


# Inicialize o dict com uma lista vazia para cada id de usuário:
friendships = {user["id"]: [] for user in users}


# In[5]:


# Em seguida, execute um loop pelos pares de amigos para preenchê-la:
for i, j in friendship_pairs:
    friendships[i].append(j) # adicione j como amigo do usuário i
    friendships[j].append(i) # adicione i como amigo do usuário j


# In[6]:


def number_of_friends(user):
    # Quantos amigos tem o _user_?
    user_id = user["id"]
    friend_ids = friendships[user_id]
    return len(friend_ids)

total_connections = sum(number_of_friends(user) for user in users)
total_connections 


# In[7]:


num_users = len(users) # tamanho da lista de usuários
avg_connections = total_connections/num_users 
avg_connections


# In[8]:


# Crie uma lista (user_id, number_of_friends).
num_friends_by_id = [(user["id"], number_of_friends(user)) for user in users]

num_friends_by_id.sort(
key=lambda id_and_friends: id_and_friends[1],
reverse = True) # classifica a lista por número de amigos, do maior para o menor

num_friends_by_id # métrica de centralidade de grau: identifica as pessoas que são centrais para a rede


# # Cientistas de dados que você talvez conheça
# 
# ### Os usuários podem conhecer os amigos dos seus amigos. Código para iterar os amigos e coletar os amigos dos amigos:

# In[9]:


def foaf_ids_bad(user):
    # foaf significa "friend of a friend" (amigo de um amigos)
    return [foaf_id
           for friend_id in friendships[user["id"]]
           for foaf_id in friendships[friend_id]]

foaf_ids_bad(users[0]) 


# O resultado traz o usuário 0 duas vezes, pois o id 0 é amigo dos seus amigos. Também traz os usuários 1 e 2, apesar de eles já serem amigos do id 0. E traz o usuário id 3 duas vezes, pois id 3  é acessível por meio de dois amigos:

# In[10]:


print(friendships[0])
print(friendships[1])
print(friendships[2])


# Gerar uma contagem de amigos em comum, porém excluindo as pessoas que o usuário já conhece:

# In[11]:


from collections import Counter # não é carregado por padrão

def friends_of_friends(user):
    user_id = user["id"]
    return Counter(
        foaf_id
        for friend_id in friendships[user_id]
        for foaf_id in friendships[friend_id]
        if foaf_id != user_id
        and foaf_id not in friendships[user_id]
    )

# para cada amigo meu, encontre os amigos deles que não sejam eu e não sejam meus amigos.

print(friends_of_friends(users[3]))

# essa operação informa corretamente a Chi (id 3) que ela possui dois amigos em comum com Hero (id 0 ), mas só um amigo em comum
# com Clive (id 5)

# outro exemplo
# usuário Clive (id 6)
print(friends_of_friends(users[6]))
# o usuário 6 não é amigo do usuário 7 porém eles tem dois amigos em comum, o usuário 6 não é amigo do usuário 4 porém eles tem
# um amigo em comum, o usuário 6 não é amigo do usuário 9 porém eles tem um amigo em comum


# Encontrar usuários com interesses similares

# In[12]:


interests = [
    (0, "Hadoop"), (0, "Big Data"), (0, "HBase"), (0, "Java"),
    (0, "Spark"), (0, "Storm"), (0, "Cassandra"),
    (1, "NoSQL"), (1, "MongoDB"), (1, "Cassandra"), (1, "HBase"),
    (1, "Postgres"), (2, "Python"), (2, "scikit-learn"), (2, "scipy"),
    (2, "numpy"), (2, "statsmodels"), (2, "pandas"), (3, "R"), (3, "Python"),
    (3, "Statistics"), (3, "regression"), (3, "probability"),
    (4, "machine learning"), (4, "regression"), (4, "decision trees"),
    (4, "libsvm"), (5, "Python"), (5, "R"), (5, "Java"), (5, "C++"),
    (5, "Haskell"), (5, "programming languages"), (6, "statistics"),
    (6, "probability"), (6, "mathematics"), (6, "theory"),
    (7, "machine learning"), (7, "scikit-learn"), (7, "Mahout"),
    (7, "neural networks"), (8, "neural networks"), (8, "deep learning"),
    (8, "Big Data"), (8, "artificial intelligence"), (9, "Hadoop"),
    (9, "Java"), (9, "MapReduce"), (9, "Big Data")
]



# In[13]:


# função para encontrar usuários com o mesmo interesse
def data_scientists_who_like(target_interest):
    # encontre os ids dos usuários com o mesmo interesse.
    return[user_id
          for user_id, user_interest in interests
          if user_interest == target_interest]


# A operação funciona, porém tem que examinar a lista de interesses inteira a cada busca


# In[22]:


# Construir um índice de interesses para usuários:

from collections import defaultdict
# A biblioteca collections do Python é um módulo da biblioteca padrão que fornece estruturas
# de dados adicionais além das nativas(list, dict, set, etc). Ela é super útil
# quando você quer escrever código mais limpo e eficiente.

# defaultdict = um dicionário com valor padrão para chaves inexistentes(evita keyError)

# As chaves são interesses, os valores são listas de user_ids com o interesse em questão
user_ids_by_interest = defaultdict(list)

for user_id, interest in interests:
    user_ids_by_interest[interest].append(user_id)
    

    
# índice de usuários para interesses:
# as chaves são user_ids, os valoes são listas de intereesses do user_id em questão
interests_by_user_id = defaultdict(list)

for user_id, interest in interests:
    interests_by_user_id[user_id].append(interest)
    
# Agora é fácil determinar quem tem mais interesses em comum com um usuário específico:
# 1- faça iteração dos interesses do usuário;
# 2- Para cada interesse, faça a iteração dos outros usuários com o mesmo interesse;
# 3- Conte quantsa vezes cada usuário aparece.

def most_common_interests_with(user):
    return Counter(
    interested_user_id
    for interest in interests_by_user_id[user["id"]]
    for interested_user_id in user_ids_by_interest[interest]
    if interested_user_id != user["id"]
    )


# # Salários e Experiência

# In[32]:


# tabela com salário de cada usuário e experiência como cientista de dados, em anos:

salaries_and_tenures = [(83000, 8.7), (88000, 8.1), 
                       (48000, 0.7), (76000, 6),
                       (69000, 6.5), (76000, 7.5),
                       (60000, 2.5), (83000, 10),
                       (48000, 1.9), (63000, 4.2)]



# In[39]:


# analisar a média salarial por anos de experiência:

# As chaves são anos, os valores são listas de salários por anos de experiência.
salary_by_tenure = defaultdict(list)

for salary, tenure in salaries_and_tenures:
    salary_by_tenure[tenure].append(salary)
    
# As chaves são anos, cada valor é o salário médio associado ao número de anos de experiência
average_salary_by_tenure = {
    tenure : sum(salaries)/len(salaries)
    for tenure, salaries in salary_by_tenure.items()
}

average_salary_by_tenure


# In[46]:


# buckets(baldes) de experiências:

def tenure_bucket(tenure):
    if tenure < 2:
        return "menos de 2 anos"
    elif tenure < 5:
        return "entre 2 a 5 anos"
    else: 
        return "mais de 5 anos"


# In[47]:


# Agrupando os salários correspondentes a cada bucket(balde)

# AS chaves são buckets de anos de experiência, os valores são as listas de salários associadas ao bucket em questão.

salary_by_tenure_bucket = defaultdict(list)

for salary, tenure in salaries_and_tenures:
    bucket = tenure_bucket(tenure)
    salary_by_tenure_bucket[bucket].append(salary)
    
    
salary_by_tenure_bucket 


# In[48]:


# média salarial de cada grupo

average_salary_by_bucket = {
    tenure_bucket: sum(salaries)/len(salaries)
    for tenure_bucket, salaries in salary_by_tenure_bucket.items()
}

average_salary_by_bucket


# # 

# # Contas Pagas

# In[61]:


# tabela de anos de experiência e contas pagas 

tenure_paid = [(0.7, "paid"), (1.9, "unpaid"),
              (2.5, "paid"), (4.2, "unpaid"),
              (6.0, "unpaid"), (6.5, "unpaid"),
              (7.5, "unpaid"), (8.1, "unpaid"),
              (8.7, "paid"), (10.0, "paid")]


anos = [0.7, 1.9, 2.5, 4.2, 6.0, 6.5, 7.5, 8.1, 8.7, 10.0]


# In[66]:


def predict_paid_or_unpaid(years_experience):
    if years_experience < 3.0:
        return "paid"
    elif years_experience < 8.5:
        return "unpaid"
    else:
        return "paid"
    
    
for i in anos:
    print(predict_paid_or_unpaid(i))
    
    
    
# podemos construir um modelo para prever a probabilidade de pagamento com base nos anos de experiência.


# # Tópicos de Interesse

# In[68]:


interests = [
    (0, "Hadoop"), (0, "Big Data"), (0, "HBase"), (0, "Java"),
    (0, "Spark"), (0, "Storm"), (0, "Cassandra"),
    (1, "NoSQL"), (1, "MongoDB"), (1, "Cassandra"), (1, "HBase"),
    (1, "Postgres"), (2, "Python"), (2, "scikit-learn"), (2, "scipy"),
    (2, "numpy"), (2, "statsmodels"), (2, "pandas"), (3, "R"), (3, "Python"),
    (3, "Statistics"), (3, "regression"), (3, "probability"),
    (4, "machine learning"), (4, "regression"), (4, "decision trees"),
    (4, "libsvm"), (5, "Python"), (5, "R"), (5, "Java"), (5, "C++"),
    (5, "Haskell"), (5, "programming languages"), (6, "statistics"),
    (6, "probability"), (6, "mathematics"), (6, "theory"),
    (7, "machine learning"), (7, "scikit-learn"), (7, "Mahout"),
    (7, "neural networks"), (8, "neural networks"), (8, "deep learning"),
    (8, "Big Data"), (8, "artificial intelligence"), (9, "Hadoop"),
    (9, "Java"), (9, "MapReduce"), (9, "Big Data")
]


# In[74]:


# Encontrar os interesses mais populares:
# Conte as palavras.

# 1- Escreva os interesses em letras minúsculas;
# 2- Divida-os em palavras;
# 3- Conte os resultados.

palavras_contadas = Counter(word
                            for user, interest in interests
                           for word in interest.lower().split())

# esse comando lista as ocorrencias das palavras
palavras_contadas


# In[75]:


for word, count in palavras_contadas.most_common():
    if count > 1:
        print(word, count)

# lista as palavras mais populares


# In[ ]:




