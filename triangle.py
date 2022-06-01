class triangle:

  def __init__(self, sideA, sideB, sideC, base, height):
    self.sideA = sideA
    self.sideB = sideB
    self.sideC = sideC
    self.base = base
    self.height = height
    
  def area(self):
      return (self.base * self.height) / 2
      
  def perimeter(self):
      return self.sideA + self.sideB + self.sideC
  
  def kind(self):
    if self.sideA > (self.sideB + self.sideC):
      return "Impossible to construct a Triangle..."
    elif (self.sideA == self.sideB) and (self.sideA == self.sideC):
      return "Equilateral triangle"
    elif (self.sideA != self.sideB) and (self.sideB != self.sideC):
      return "Scalene triangle" 
    elif (self.sideA == self.sideB) or ((self.sideA == self.sideC)) or ((self.sideB == self.sideC)):
        return "isosceles triangle"
    else:
      return "Invalid Values..."

#tretaing errors
try:
  Triangle = triangle(3, 3, -2, 3, 5)
  Triangle2 = triangle(12, 13, 15, 12, 15)
  print(Triangle.kind(), Triangle2.kind())
except TypeError: #in the case of sides provideds are more than 3
    print("In this case, propably you entered eith more that 3 arguments, \nremeber: It's a T-R-I-A-N-G-L-E >.<")



