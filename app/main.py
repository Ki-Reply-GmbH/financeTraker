from fastapi import FastAPI
from routes.users import router as UserRouter

app = FastAPI()

app.include_router(UserRouter)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


def firstRepeatingElement(arr):
    min = -1
    myset = set()

    for i in range(len(arr)-1, -1, -1):
        if arr[i] in myset:
            min = i
        else:
            myset.add(arr[i])
    
    if min != -1:
        print("The first repeating element is", arr[min])
    else:
        print("There are no repeating elements")

# Example usage
arr = [10, 5, 3, 4, 3, 5, 6]
firstRepeatingElement(arr)