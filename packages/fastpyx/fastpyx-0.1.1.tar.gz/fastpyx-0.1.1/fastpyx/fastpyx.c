#define PY_SSIZE_T_CLEAN
#include <Python.h>




static PyObject* multiply_number(PyObject* self, PyObject *const *args, Py_ssize_t nargs){
    if (nargs != 2){
        PyErr_SetString(PyExc_TypeError, "multiply_number() takes exactly 2 arguments");
        return NULL;
    }
    
    
    PyObject *py_num1 = args[0], *py_num2 = args[1];
    double num1, num2;

    num1 = PyFloat_Check(py_num1) ? PyFloat_AS_DOUBLE(py_num1) : PyLong_AsDouble(py_num1);
    num2 = PyFloat_Check(py_num2) ? PyFloat_AS_DOUBLE(py_num2) : PyLong_AsDouble(py_num2);


    if (PyErr_Occurred()) {
        return NULL;
    }
    return PyFloat_FromDouble(num1 * num2);
}

static PyMethodDef FastPyxMethods[] = {
    {"multiply_number", (PyCFunction)multiply_number, METH_FASTCALL, "Return a simple Multiply Number"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef FastPyx = {
    PyModuleDef_HEAD_INIT,
    "fastpyx",
    NULL,
    -1,
    FastPyxMethods
};

PyMODINIT_FUNC PyInit_fastpyx(void) {
    return PyModule_Create(&FastPyx);
}