# En episodios anteriores...

- Rust:
    - tipo `usize` para el tamaño de palabra de la arquitectura.
    - arrays:
        - constructor literal
        ```rust
            let my_array = [1,2,3];
        ```
        - constructor con repetición
        ```rust
        let my_array: [type; size]: [elementToRepeat; size];
        ```
    - structs:
        - declaración:
            ```rust
            struct MyStruct {
                field_name: fieldType,
                another_field: anotherType,
            }
            ```
        - constructor:
            ```rust
            let my_struct = MyStruct {
                field_name: value,
                another_field: anotherValue,
            };
            ```