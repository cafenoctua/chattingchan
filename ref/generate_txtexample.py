def setTag2File(filename, tagtype):
    # Load data
    with open(filename, 'r') as f:
        data = f.readlines()
    
    return f'<{tagtype}>{data[0].split()[0]}</{tagtype}>'

def geneInitilizeExam():
    return ['da=initialize', 'もう一度はじめから', 
            'はじめから', 'はじめからお願いします', 
            '最初から', '最初からお願いします', 
            '初期化してください', 'キャンセル', 'すべてキャンセル']

def geneRequest(words1, words2):
    conjunction = ['','の','で']
    end_sens = ['', 'で食べたい','です','で教えて']

    sentens = []
    for sens in end_sens:
        sentens.append(words1 + sens)
        sentens.append(words2 + sens)
    
    for conj in conjunction:
        for sens in end_sens:
            sentens.append(words1 + conj + words2 + sens)
    
    return sentens

def geneCorrect(words):
    end_sens = ['じゃない','違う','ではありません', 'じゃなくて', 'じゃないです']

    sentens = []
    for sens in end_sens:
        sentens.append(words + sens)
    
    return sentens

if __name__ == "__main__":
    words1 = setTag2File('./src/pref.txt', 'place')
    words2 = setTag2File('./src/genre.txt', 'genre')

    with open('./src/example_gurunavi.txt', 'w') as f:
        f.write('da=request-restrante\n')
        for sens in geneRequest(words1, words2):
            f.write(sens + '\n')
        for sens in geneInitilizeExam():
            f.write(sens + '\n')
        f.write('da=correct-info\n')
        for sens in geneCorrect(words1):
            f.write(sens + '\n')
        for sens in geneCorrect(words2):
            f.write(sens + '\n')
                    

    