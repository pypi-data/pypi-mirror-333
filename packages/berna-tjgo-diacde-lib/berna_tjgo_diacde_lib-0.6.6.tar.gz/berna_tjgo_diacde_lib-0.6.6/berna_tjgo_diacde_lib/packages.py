'''
Created on Sun Jul 21 09:54:07 2024

@authors:
    Antonio Pires
    Milton Ávila
    Wesley Oliveira

@License:
Este projeto está licenciado sob a Licença Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0). Você pode compartilhar, adaptar e construir sobre o material, desde que atribua crédito apropriado, não use o material para fins comerciais e distribua suas contribuições sob a mesma licença.
Para mais informações, consulte o arquivo [LICENSE](./LICENSE).
'''
from ._methods import *

class Packages:
    METHODS: dict[str, any] = {
        "no_ponctuation": remove_ponctuation,
        "no_multiple_spaces": remove_stopwords,
        "lemmatize": lemmatize_txt,
        "stemming": stem_txt,
        "tokenize": tokenize,
        "only_latin": set_only_latin,
        "no_numbers": remove_numbers,
        "no_multiple_spaces": remove_multiple_espaces,
        "no_loose_letters": remove_loose_letters,
        "no_email": remove_email,
        "no_html": remove_html,
        "replace_synonym_by_dict": get_synonym_by_dict
    }