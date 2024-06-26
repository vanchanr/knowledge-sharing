### Java Generics
- Enhances type system by enabling compile time type checking to avoid potential runtime errors
- Eliminates the need for explicit type casting
- Promotes code reusability and possibility to develop generic algorithms
```
public <T> List<T> replicate(T element, int count) {
    List<T> list = new ArrayList<>();
    for (int i = 0; i < count; ++i) {
        list.add(element);
    }
    return list;
}

public <T> void printGenericList(List<T> list) {
    for (T element : list) {
        System.out.println(element);
    }
}

public void printGenericList(List<?> list) {
    for (int i = 0; i < list.size(); ++i) {
        System.out.println(list.get(i));
    }
}
```
- Generic methods are methods that introduce their own type parameters. The syntax for a generic method includes a list of type parameters, inside angle brackets, which appears before the method's return type. These type parameters can then be used in the methods input parameters and the method’s logic
- We can use a wildcard (?) to create a generic method when the type parameter need not be referenced elsewhere (inside method body or any other method parameters)
