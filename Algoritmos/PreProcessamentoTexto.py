import string
import re
import seaborn as sns
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 

stop_words = stopwords.words('english')

def limpando_issue(issue):
    issue = issue.lower()
    
    # Remoção de código
    issue = re.sub(r'`.+`', " ", issue)

    # Remoção de TAGS
    issue = re.sub(r'<.*?>', " ", issue)

    # Remoção de HREF
    issue = re.sub(r' href=".*?"', " ", issue)

    # Remoção de tabelas
    
    issue = re.sub(r'(\|)([\|\s\-]|[\:arrow\_down\:]|[\:arrow\_up\:]|[❌]|[❓]|[✔️])+(\|)', " ", issue)	

    # Remoção de url
    issue = re.sub(r"https?://[A-Za-z0-9./]+", " ", issue)

    # Remoção de referência de tabela
    issue = re.sub(r'[\!][[]([a-z]|[0-9]|[@]|[:]|[\/]|[/]|[\_])+[]]', ' ', issue)

    # Remoção de trechos de código
    issue = re.sub(r'`.+`', ' ', issue)
    issue = re.sub(r'~~~.+ ~~~', ' ', issue)

    # Remoção de comentários
    issue = re.sub(r'([\r\n\r\n])*>\s([\w]|[\d]|[—])*(.)*[.!?]*([\r\n\r\n])', ' ', issue)

    # Remoção de Warnings
    issue = re.sub(r'([a-zA-Z]+\s[0-9]+[,]\s[0-9]+\s[0-9]+[:][0-9]+[:][0-9]+\s[aApPmM]+([\w]|[\d]|[.]|[_]|[\s])+[\n])*([A-Z])+(:)([a-zA-Z]|[.]|[0-9]|[\s]|[(]|[)]|[\[]|[\]]|[{]|[}])+(:)([a-zA-Z]|[.]|[0-9]|[\s]|[(]|[)]|[\[]|[\]]|[{]|[}])+[.]', ' ', issue)

    # Remoção de Exceptions
    issue = re.sub(r'([\w]|[\d]|[.]|[_])+[\s]?[:]([\w]|[\d]|[.]|[_]|[\s])+[\']([\w]|[\d]|[.]|[_]|[\s])+[\']([\w]|[\d]|[.]|[_]|[\s]|[\(]|[\)]|[\$]|[\:])+[\)\n]', ' ', issue)

    # Remoção de Nomes de Classes
    issue = re.sub(r'[...]?[a-zA-Z]+([\.]|[\/])([\w]|[\d]|[\_]|[\.]|[\/])+([a-zA-Z]|[0-9])+', ' ', issue)

    # Remoção de caminhos
    issue = re.sub(r'[\[]? ((([\w]|[...])([\:]|[\/])([\w]|[\d]|[\]|[\\]|[\/]|[/]|[\.]|[|]|[\-])+ )) [\]]?', ' ', issue)

    # Remoção de outros tipos de caracteres
    issue = re.sub(r"@[A-Za-z0-9]+", " ", issue)    
    
    # Remoção de números
    issue = re.sub(r"[^a-zA-Z]+", " ", issue)

    # Remoção de espaços em branco sucessivos
    issue = re.sub(r" +", " ", issue)

    # Remoção de stop words
    issue = remove_stopWords(issue)

    return issue

def remove_stopWords(issue):
    global stop_words

    s = ''
    iss = word_tokenize(issue)
    
    for w in iss:
        if(len(w) > 1):
            if not w in stop_words:
                s += w + ' '
    

    return s

