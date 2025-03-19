class Testing:
    def __init__(self) -> None:
        self.a = 2
        self.b = 3
    
    def summ(self) -> int:
        return self.a + self.b
    
    def raz(self) -> int:
        return self.a - self.b

    def set_a(self, a: int) -> None:
        self.a = a
    
    def set_b(self, b: int) -> None:
        self.b = b