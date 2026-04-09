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

    # datos actuales
    for s in seqs:
        for n in s:
            f[n]+=1

    # datos históricos (aprendizaje)
    try:
        with open("datos.json","r") as file:
            for line in file:
                data = eval(line)
                for s in data["secuencias"]:
                    for n in s:
                        f[n]+=1
    except:
        pass

    return f



@app.post("/analizar")
def analizar(guardar_datos(data)):
    f = frecuencias(data.secuencias, data.maximo)
    resultados=[]
    for i in range(1,data.maximo+1):
        seq = generar(i,data.cantidad,data.maximo,f)
        prob = sum(f[n] for n in seq)
        resultdef generar(inicio, cantidad, maximo, freq):
    nums = list(range(1,maximo+1))
    nums.remove(inicio)
    res=[inicio]

    while len(res)<cantidad:
        nums_sorted = sorted(nums, key=lambda x: -freq[x])
        
        # mezcla inteligencia + exploración
        if random.random() < 0.7:
            choice = nums_sorted[0]
        else:
            choice = random.choice(nums)

        res.append(choice)
        nums.remove(choice)

    resultados.append({
    "inicio":i,
    "secuencia":seq,
    "prob":prob,
    "explicacion": explicar_secuencia(seq, f)
})
    
    reimport json

def guardar_datos(data):
    with open("datos.json","a") as f:
        f.write(json.dumps(data.dict())+"\\n")sultados.sort(key=lambda x: x["prob"], reverse=True)
    return resultados 

def explicar_secuencia(seq, freq):
    explicacion = []
    for n in seq:
        explicacion.append(f"Número {n} tiene frecuencia {freq[n]}")
    return " | ".join(explicacion)
    
    
