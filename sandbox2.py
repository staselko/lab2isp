from lib import Serializer as ser

serializer = ser.Serializer()


serializer.load("sample.json")

serializer.data()

serializer.load("lambda.json")

serializer.data("Name Asd")

serializer.load("class_a.json")

A = serializer.data()


print(A.dict)