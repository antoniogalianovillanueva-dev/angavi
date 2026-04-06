from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

class InputData(BaseModel):
    cantidad: int
    maximo: int
    secuencias: list[list[int]]

def frecuencias(seqs, maximo):
    f = [0]*(maximo+1)
    for s in seqs:
        for n in s:
            f[n]+=1
    return f

def generar(inicio, cantidad, maximo, freq):
    nums = list(range(1,maximo+1))
    nums.remove(inicio)
    res=[inicio]
    while len(res)<cantidad:
        nums_sorted = sorted(nums, key=lambda x: -freq[x])
        choice = nums_sorted[0]
        res.append(choice)
        nums.remove(choice)
    return res

@app.post("/analizar")
def analizar(data: InputData):
    f = frecuencias(data.secuencias, data.maximo)
    resultados=[]
    for i in range(1,data.maximo+1):
        seq = generar(i,data.cantidad,data.maximo,f)
        prob = sum(f[n] for n in seq)
        resultados.append({"inicio":i,"secuencia":seq,"prob":prob})
    resultados.sort(key=lambda x: x["prob"], reverse=True)
    return resultados
