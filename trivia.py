import random
import time

from itertools import chain
from Maybe import Maybe
from functools import partial
from functools import reduce

import pandas as pd


def increment(x):
    return Maybe.just(x + 10)


def load_data(qa_map, csv_data, index):
    try:
        qa_map[csv_data.iloc[index, 0]] = list(csv_data.iloc[index, 1:])
        load_data(qa_map, csv_data, index + 1)
    except IndexError:
        return


def generate_trivia(qa_map):
    return generate_trivia_aux(qa_map, [], 0)


def generate_trivia_aux(qa_map, final_qa, index):
    if index == 5 or index == len(qa_map.keys()):
        return final_qa

    random_index = random.randint(0, len(qa_map.keys()) - 1)
    question = list(qa_map.keys())[random_index]
    '''Verificamos que la pregunta no se haya seleccionado hasta el momento'''
    if question not in final_qa:
        '''Se transforma 'question' en lista ya que chain() une dos listas'''
        final_qa = list(chain(final_qa, [question]))
        index += 1
    return generate_trivia_aux(qa_map, final_qa, index)


def final_stats(func):
    def wrapper(*args, **kwargs):
        init_time = time.time()
        '''Se llama a la función y recibimos el score'''
        qa_keys = list(args[1])
        score = func(args[0], iter(qa_keys))
        final_time = time.time()
        '''Se imprime un mensaje final que determina el score / total y el tiempo que se demoró en hacer el trivia'''
        print("Quiz completado, resultado final " + str(score) + "/" + str(reduce(lambda x, b: x + 1, qa_keys, 0) * 10))
        print("Has demorado " + "{:.2f}".format(final_time - init_time) + " segundos")

    return wrapper


@final_stats
def make_trivia(qa_map, qa_keys):
    '''Llama a make trivia aux para poder utilizar el decorator de forma adecuada'''
    return make_trivia_aux(qa_map, qa_keys, Maybe(0))


def obtain_options(qa_map, current_key, index):
    '''Generador de las opciones de respuesta'''
    if index == 3:
        return
    yield str(index + 1) + ". " + qa_map[current_key][index]
    yield from obtain_options(qa_map, current_key, index + 1)


def make_trivia_aux(qa_map, qa_keys, score):
    '''Recorremos iterativamente las keys (preguntas) hasta que ocurra un error, en cuyo caso retornamos el score'''
    try:
        currentKey = qa_keys.__next__()
    except StopIteration:
        return score
    '''Imprimimos la pregunta'''
    print(currentKey)

    obtain_options_start = partial(obtain_options, index=0)
    '''Obtenemos las opciones de respuesta para la pregunta actual'''
    options = obtain_options_start(qa_map, currentKey).__iter__()
    [print(x) for x in options]

    '''Se pide input al usuario y se analiza si la respuesta es correcta o incorrecta.
    En caso de ser correcta se suman 10 puntos al usuario y en caso de ser incorrecta
    el valor no se modifica'''
    ans = input("Respuesta: ")

    try:
        if qa_map[currentKey][int(ans) - 1] == qa_map[currentKey][3]:
            score = increment(score.value)
            print("Respuesta correcta")
        else:
            raise ValueError
    except (ValueError, IndexError):
        if ans.lower() == str(qa_map[currentKey][3]).lower():
            score = increment(score.value)
            print("Respuesta correcta")
        else:
            '''Se manejan todos los errores que puedan ocurrir por igual.'''
            print("Respuesta incorrecta, la correcta es " + qa_map[currentKey][3])
    # except Exception:
    #
    #     print("Respuesta incorrecta, la correcta es " + qa_map[currentKey][3])
    '''Se imprime la cantidad de puntos que tiene el usuario luego de responder cada pregunta.'''
    print("Puntos actuales " + score.__str__() + "\n")
    '''Retornamos el valor de la iteracion'''
    return make_trivia_aux(qa_map, qa_keys, score)


if __name__ == '__main__':
    '''Creamos mapas con preguntas y respuestas'''
    qa_map = {}
    '''Cargamos la info en el mapa'''
    load_data(qa_map, pd.read_csv('trivia_questions.csv'), 0)
    '''Se genera el trivia seleccionando 5 preguntas aleatorias del csv'''
    chosen_qa_keys = generate_trivia(qa_map)
    '''Comienza la partida de trivia'''
    make_trivia(qa_map, iter(chosen_qa_keys))