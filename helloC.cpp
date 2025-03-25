#include "py/obj.h" // MicroPython object definitions
#include "py/runtime.h" // MicroPython runtime API


STATIC mp_obj_t example_add_ints(mp_obj_t a_obj, mp_obj_t b_obj) {
    int a = mp_obj_get_int(a_obj); // Convert MicroPython object to C int
    int b = mp_obj_get_int(b_obj);
    int result = a + b;
    return mp_obj_new_int(result); // Convert C int back to MicroPython object
}
