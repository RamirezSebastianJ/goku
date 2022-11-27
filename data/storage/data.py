import json


def get_credits():
    filehandle = open('credits.json',)
    data = json.load(filehandle)
    return data

def get_records():
    filehandle = open('scores.json',)
    data = json.load(filehandle)
    return data['scores']

def saveRecord(score, name):
    f = open('scores.json',)
    aux = json.load(f)
    f.close()
    with open('scores.json', 'r+') as filehandle:
        data = json.load(filehandle)
        scores = data['scores']
        scores.append({
            "name": name,
            "score": score
        })
        # scores.sort(reverse=True)
        scores = sorted(scores, key=lambda x: x['score'], reverse=True)
        data['scores'] = scores
        filehandle.seek(0)
        json.dump(data, filehandle, indent=4)
        filehandle.truncate()

    f = open('scores.json',)
    f.close()
