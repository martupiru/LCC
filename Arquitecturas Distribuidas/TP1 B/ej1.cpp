#include <iostream>
#include <vector>
#include <thread>
#include <chrono>
#include <cmath>  
using namespace std;

// Cálculo secuencial de ln(x)
long double ln_secuencial(long double x, long long N) {
    long double z = (x - 1) / (x + 1);
    long double z_pow = z;
    long double sum = 0.0;

    for (long long i = 1; i <= 2 * N - 1; i += 2) {
        sum += z_pow / i;
        z_pow *= z * z; // siguiente potencia impar
    }

    return 2 * sum;
}

// Cálculo paralelo de ln(x) sin pow
void calcular_parcial(long double x, long long inicio, long long fin, long double &resultado) {
    long double z = (x - 1) / (x + 1);
    long double z_pow = 1.0; // se inicializa luego según el índice
    long double suma = 0.0;

    // Ajustamos la potencia inicial para cada hilo
    long long i = 2 * inicio + 1;
    z_pow = pow(z, i); // solo una vez al inicio por hilo

    for (long long n = inicio; n < fin; n++) {
        suma += z_pow / (2*n + 1);
        z_pow *= z * z; // siguiente potencia impar
    }

    resultado = 2 * suma;
}

int main() {
    long double x;
    int num_hilos;
    const long long N = 10000000; // 10 millones de términos

    cout << "Ingrese un número igual o mayor a 1500000: ";
    cin >> x;

    if (x < 1500000) {
        cout << "El número debe ser mayor a 1500000\n";
        return 1;
    }

    cout << "Ingrese la cantidad de hilos para el cálculo paralelo: ";
    cin >> num_hilos;

    // -------------------
    // Cálculo secuencial
    // -------------------
    auto inicio_seq = chrono::high_resolution_clock::now();
    long double ln_x_seq = ln_secuencial(x, N);
    auto fin_seq = chrono::high_resolution_clock::now();
    chrono::duration<long double> duracion_seq = fin_seq - inicio_seq;

    cout.precision(15);
    cout << "\nResultado secuencial:\n";
    cout << "ln(" << x << ") ≈ " << ln_x_seq << endl;
    cout << "Tiempo secuencial: " << duracion_seq.count() << " segundos\n";

    // -------------------
    // Cálculo paralelo
    // -------------------
    vector<long double> resultados(num_hilos, 0.0);
    vector<thread> hilos;

    auto inicio_par = chrono::high_resolution_clock::now();

    long long chunk = N / num_hilos;
    for (int i = 0; i < num_hilos; i++) {
        long long start = i * chunk;
        long long end = (i == num_hilos - 1) ? N : (i + 1) * chunk;
        hilos.push_back(thread(calcular_parcial, x, start, end, ref(resultados[i])));
    }

    for (auto &h : hilos) h.join();

    long double ln_x_par = 0.0;
    for (int i = 0; i < num_hilos; i++) ln_x_par += resultados[i];

    auto fin_par = chrono::high_resolution_clock::now();
    chrono::duration<long double> duracion_par = fin_par - inicio_par;

    cout << "\nResultado paralelo:\n";
    cout << "ln(" << x << ") ≈ " << ln_x_par << endl;
    cout << "Tiempo con " << num_hilos << " hilos: " << duracion_par.count() << " segundos\n";

    // -------------------
    // Speedup
    // -------------------
    long double speedup = duracion_seq.count() / duracion_par.count();
    cout << "\nSpeedup = " << speedup << endl;

    return 0;
}
