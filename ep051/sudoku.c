#include <stdio.h>

typedef int bool;
#define TRUE 1
#define FALSE 0

int tablero_orig[9][9];
int tablero_busq[9][9];

int posibles[9][9][10];

void leer_tablero();
long long calcular_posibles();
int calcular_posibles_casilla(int i, int j);
bool comprobar_insertar(int n, int i, int j);
bool resolver_recursivo(int i, int j);
bool es_valido(int n, int i, int j);
bool esta_en_fila(int n, int i);
bool esta_en_columna(int n, int j);
bool esta_en_cuadrante(int n, int i, int j);
void print_posibilidades();
void print_tablero();

/**
 * Rellena posibles para todas las casillas, y devuelve
 * el numero total de combinaciones posibles.
 */
long long calcular_posibles()
{
    int i, j;
    int m;
    long long n = 1;
    for (i = 0; i < 9; ++i)
    {
        for (j = 0; j < 9; ++j)
        {
            if (tablero_orig[i][j] == 0)
            {
                m = calcular_posibles_casilla(i, j);
                n *= m;
            }
        }
    }
    return n;
}

/**
 * Rellena los valores de posibles[i][j], dejando un 0 tras
 * la ultima casilla rellena y devolviendo el número de
 * posibilidades;
 */
int calcular_posibles_casilla(int i, int j)
{
    int n;
    int k = 0;
    for (n = 1; n <= 9; ++n)
    {
        if (es_valido(n, i, j))
        {
            posibles[i][j][k++] = n;
        }
    }
    posibles[i][j][k] = 0;
    if (k == 0)
    {
        k = 1;
    }
    return k;
}

bool es_valido(int n, int i, int j)
{
    return !esta_en_fila(n, i) &&
           !esta_en_columna(n, j) &&
           !esta_en_cuadrante(n, i / 3, j / 3);
}

bool esta_en_fila(int n, int i)
{
    int j;
    for (j = 0; j < 9; ++j)
    {
        if (tablero_busq[i][j] == n)
        {
            return TRUE;
        }
    }
    return FALSE;
}

bool esta_en_columna(int n, int j)
{
    int i;
    for (i = 0; i < 9; ++i)
    {
        if (tablero_busq[i][j] == n)
        {
            return TRUE;
        }
    }
    return FALSE;
}

/**
 * Indica si n esta en el cuadrante i, j, que son las coordenadas
 * del cuadrante (de 0 a 2), NO las coordenadas de una casilla
 * dentro del cuadrante.
 */
bool esta_en_cuadrante(int n, int i, int j)
{
    int k, l;
    int mk, ml;
    mk = (i + 1) * 3;
    ml = (j + 1) * 3;
    for (k = i * 3; k < mk; ++k)
    {
        for (l = j * 3; l < ml; ++l)
        {
            if (tablero_busq[k][l] == n)
            {
                return TRUE;
            }
        }
    }
    return FALSE;
}

bool resolver_recursivo(int i, int j)
{
    int n;
    int k;
    int si, sj;

    // si hemos terminado el tablero
    if (i == 9 && j == 0)
    {
        return TRUE;
    }

    // calculamos la siguiente celda
    si = i;
    sj = j + 1;
    if (sj == 9)
    {
        sj = 0;
        ++si;
    }

    if (tablero_orig[i][j])
    {
        return resolver_recursivo(si, sj);
    }

    for (k = 0; n = posibles[i][j][k]; ++k)
    {
        if (es_valido(n, i, j))
        {
            tablero_busq[i][j] = n;
            if (resolver_recursivo(si, sj))
            {
                return TRUE;
            }
        }
    }
    tablero_busq[i][j] = 0;
    return FALSE;
}

void print_tablero(int t[9][9])
{
    int i, j;
    for (i = 0; i < 9; ++i)
    {
        for (j = 0; j < 9; ++j)
        {
            printf("%d ", t[i][j]);
            if (((j + 1) % 3) == 0)
            {
                printf("  ");
            }
        }
        printf("\n");
        if ((i + 1) % 3 == 0)
        {
            printf("\n");
        }
    }
}

void print_posibilidades()
{
    int i, j, k, n;
    for (i = 0; i < 9; i++)
    {
        for (j = 0; j < 9; j++)
        {
            printf("(%d, %d) : ", i + 1, j + 1);
            for (k = 0; n = posibles[i][j][k]; k++)
            {
                printf("%d ", n);
            }
            printf("\n");
        }
    }
}

void leer_tableros()
{
    int i, j;
    int n;
    for (i = 0; i < 9; i++)
    {
        for (j = 0; j < 9; j++)
        {
            scanf(" %d ", &n);
            tablero_orig[i][j] = n;
            tablero_busq[i][j] = n;
        }
    }
}

int main()
{
    long long n;
    leer_tableros();
    print_tablero(tablero_orig);
    printf("analizando tablero...\n");
    n = calcular_posibles();
    print_posibilidades();
    printf("%lld posibles combinaciones.\n", n);
    printf("buscando solucion...\n");
    if (resolver_recursivo(0, 0))
    {
        printf("solución encontrada!:\n");
    }
    else
    {
        printf("solución no encontrada :(\n");
    }
    print_tablero(tablero_busq);
}