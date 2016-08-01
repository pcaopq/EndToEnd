cdef extern from "rectangle.h" namespace "shapes":
    cdef cppclass Rectangle:
        Rectangle() except +
        Rectangle(int, int, int, int) except +
        int x0, y0, x1, y1
        int getArea()
        void getSize(int* width, int* height)
        void move(int, int)

cdef class PyRectangle:
    cdef Rectangle c_rect      # hold a C++ instance which we're wrapping
    def __cinit__(self, int x0, int y0, int x1, int y1):
        self.c_rect = Rectangle(x0, y0, x1, y1)
    def get_area(self):
        return self.c_rect.getArea()
    def get_size(self):
        cdef: 
            int width
            int height
        self.c_rect.getSize(&width, &height)
        return width, height
    def move(self, dx, dy):
        self.c_rect.move(dx, dy)

    @property
    def x0(self):
        return self.c_rect.x0

    @x0.setter
    def x0(self, x0):
    # def __set__(self, x0):
        self.c_rect.x0 = x0

# cdef Rectangle *rec = new Rectangle(1,2,3,4)
# print(rec.getArea())
rec = PyRectangle(1, 2, 3, 4)
rec.x0 = 10
# recLength = rec.getLength()
print(rec.x0)
# del rec
# def fib(int n):
#     cdef int i, a, b
#     a, b = 1, 1
#     for i in range(n):
#         a, b = a+b, a
#     return a