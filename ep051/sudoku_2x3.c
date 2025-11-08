#include<stdio.h>

typedef int bool;
#define TRUE 1
#define FALSE 0

#define REGION_ROWS 2
#define REGION_COLS 3
#define SIZE (REGION_ROWS * REGION_COLS)

int tablero_orig[SIZE][SIZE];
int tablero_busq[SIZE][SIZE];

int posibles[SIZE][SIZE][SIZE + 1]; // +1 para el centinela

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
    for (i = 0; i < SIZE; ++i)
    {
        for (j = 0; j < SIZE; ++j)
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
    for (n = 1; n <= SIZE; ++n)
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
           !esta_en_cuadrante(n, i, j);
}

bool esta_en_fila(int n, int i)
{
    int j;
    for (j = 0; j < SIZE; ++j)
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
    for (i = 0; i < SIZE; ++i)
    {
        if (tablero_busq[i][j] == n)
        {
            return TRUE;
        }
    }
    return FALSE;
}

/**
 * Indica si n esta en el cuadrante de la casilla i, j
 */
bool esta_en_cuadrante(int n, int i, int j)
{
    int cuad_i = i / REGION_ROWS;
    int cuad_j = j / REGION_COLS;
    int max_ci = (cuad_i + 1) * REGION_ROWS;
    int max_cj = (cuad_j + 1) * REGION_COLS;

    for (i = cuad_i * REGION_ROWS; i < max_ci; ++i)
    {
        for (j = cuad_j * REGION_COLS; j < max_cj; ++j)
        {
            if (tablero_busq[i][j] == n)
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

    si = i;
    sj = j + 1;
    if (sj == SIZE)
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
            if (i == SIZE - 1 && j == SIZE - 1)
            {
                return TRUE;
            }
            else if (resolver_recursivo(si, sj))
            {
                return TRUE;
            }
            tablero_busq[i][j] = 0;
        }
    }
    return FALSE;
}

void print_tablero(int t[SIZE][SIZE])
{
    int i, j;
    for (i = 0; i < SIZE; ++i)
    {
        for (j = 0; j < SIZE; ++j)
        {
            printf("%d ", t[i][j]);
            if (((j + 1) % REGION_COLS) == 0)
            {
                printf("  ");
            }
        }
        printf("\n");
        if ((i + 1) % REGION_ROWS == 0)
        {
            printf("\n");
        }
    }
}

void print_posibilidades()
{
    int i, j, k, n;
    for (i = 0; i < SIZE; i++)
    {
        for (j = 0; j < SIZE; j++)
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
    for (i = 0; i < SIZE; i++)
    {
        for (j = 0; j < SIZE; j++)
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