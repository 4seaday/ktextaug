import six
import random
import ktextaug.utils as util
from ktextaug import *

"""
Augmentation
1.Random Swap
2.Random Insertion
3.Random Deletion
4.Synonym Replacement
5.Back Translation
6.Noise Generation
7.Generative model(in progress)
"""
"""
Author : JinUk, Cho, JongHyeok, Park
Last update : 20th, Nov, 2020

각 Augmentation 기법에 대한 사용예시입니다.
"""

#######################
##Augmentation        #
#######################


def Augment(text, alpha_rs=0.2, alpha_ri=0.2, alpha_sr=0.2, p_rd=0.2, num_iter=9):
    translator = BackTranslate()
    noise_gen = NoiseGenerator()
    words = util.tokenize(text)
    num_words = len(words)
    augmented_sentence = {}
    num_per_tech = int(num_iter / 4) + 1
    n_rs = max(1, int(alpha_rs * num_words))
    n_ri = max(1, int(alpha_ri * num_words))
    n_sr = max(2, int(alpha_sr * num_words))

    # Add original words
    augmented_sentence["org"] = text
    print("rs")
    # RS
    tmp = []
    for _ in range(num_per_tech):
        a_words = random_swap(words, n_rs)
        tmp.append(a_words)
    augmented_sentence["rs"] = tmp
    print("ri")
    # RI
    tmp = []
    for _ in range(num_per_tech):
        a_words = random_insertion(words, n_ri)
        tmp.append(a_words)
    augmented_sentence["ri"] = tmp
    print("rd")
    # RD
    tmp = []
    for _ in range(num_per_tech):
        a_words = random_deletion(words, p_rd)
        tmp.append(a_words)
    augmented_sentence["rd"] = tmp
    print("sr")
    # SR
    tmp = []
    for _ in range(num_per_tech):
        a_words = synonym_replacement(words, n_sr)
        tmp.append(a_words)
    augmented_sentence["sr"] = tmp
    print("bt")
    # Tran
    tmp = []
    try:  # 오류 발생 https://github.com/ssut/py-googletrans/issues/234
        a_words = translator.backtranslate(text, target_language="en")
        tmp.append(a_words)
        a_words2 = translator.backtranslate(text, target_language="ja")
        tmp.append(a_words2)
    except Exception as e:
        tmp.append(e)

    augmented_sentence["bt"] = tmp
    print("ns")
    # Noise
    tmp = []
    a_words = noise_gen.noise_generate1(text)
    a_words2 = noise_gen.noise_generate2(text)
    tmp.append(a_words)
    tmp.append(a_words2)
    augmented_sentence["noise"] = tmp

    return augmented_sentence


#######################
##    TEST            #
#######################

if __name__ == "__main__":
    text = "이 문장은 변형적 데이터 증강기법의 예시 문장입니다."

    result = Augment(text)
    print(f"Original : {text}, length : {len(result)}")
    print("Random Swap : ", result["rs"])
    print("Random Insertion : ", result["ri"])
    print("Random Deletion : ", result["rd"])
    print("Synonym Replacement : ", result["sr"])
    print("BackTranslation : ", result["bt"])
    print("Adding Noise : ", result["noise"])
