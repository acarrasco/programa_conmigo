# Tipos de lenguajes y cómo reconocerlos

- Lenguajes regulares:
    - Expresiones regulares, e.g. números decimales `[0-9]+(\.[0-9]+)?`
    - Automátas finitos

- Lenguajes independientes del contexto:
    - Gramáticas independientes del contexto, e.g. expresiones aritméticas:
    ```
    Exp := Exp BinOp Exp
    BinOp := + | - | * | /
    Exp := (Exp)
    ```
    - Automátas a pila