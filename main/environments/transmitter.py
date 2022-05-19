class Transmitter():
    def __init__(self, name, lon, lat, span_lon=1.0, span_lat=1.0, height=10):
        self.name = name
        self.lon = lon
        self.lat = lat
        self.span_lon = span_lon
        self.span_lat = span_lat
        self.height = height

    def __call__(self):
        return (self.name, self.lon, self.lat, self.span_lon, self.span_lat, self.height)


transmitters = [
    Transmitter("DaeJeon", 127.3845, 36.3504),  # 대잔광역시청
    Transmitter("Deogyu Mountain", 127.7475, 35.8589),  # 덕유산 국립공원 향적봉
    Transmitter("Chiak Mountain", 128.0536, 37.3661),  # 치악산 비루봉
    Transmitter("Daedun Mountain", 127.3219, 36.125),  # 대둔산 마천대
]


print("-----------------TRANSMITTER LISTS-----------------")
for transmitter in transmitters:
    print(transmitter())
print("---------------------------------------------------")
