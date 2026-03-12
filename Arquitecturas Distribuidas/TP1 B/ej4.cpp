#include <iostream>
#include <vector>
#include <thread>
#include <cmath>
#include <chrono>
#include <mutex>
#include <algorithm>

using namespace std;
using namespace std::chrono;

mutex mtx; // para proteger el acceso concurrente al vector global de primos

// fncion para verificar si un num es primo 
bool esPrimo(long long n, const vector<long long>& primosBase) {
    if (n < 2) return false;
    for (long long p : primosBase) {
        if (p * p > n) break;
        if (n % p == 0) return false;
    }
    return true;
}

// genera primos hasta raiz cuadrada de N
vector<long long> generarPrimosBase(long long N) {
    vector<long long> primos;
    for (long long i = 2; i * i <= N; i++) {
        bool primo = true;
        for (long long p : primos) {
            if (p * p > i) break;
            if (i % p == 0) { primo = false; break; }
        }
        if (primo) primos.push_back(i);
    }
    return primos;
}

// version secuencial 
vector<long long> primosSecuencial(long long N) {
    vector<long long> primosBase = generarPrimosBase(N);
    vector<long long> primos;
    for (long long i = 2; i < N; i++) {
        if (esPrimo(i, primosBase)) primos.push_back(i);
    }
    return primos;
}

// trabajo que realiza cada hilo
void primosMultihilos(long long inicio, long long fin, const vector<long long>& primosBase, vector<long long>& primosGlobal) {
    vector<long long> locales;
    for (long long i = inicio; i < fin; i++) {
        if (esPrimo(i, primosBase)) locales.push_back(i);
    }
    lock_guard<mutex> lock(mtx);
    primosGlobal.insert(primosGlobal.end(), locales.begin(), locales.end());
}

// version multihilo 
vector<long long> primosMultihilo(long long N, int numHilos) {
    vector<long long> primosBase = generarPrimosBase(N);
    vector<long long> primosGlobal;

    vector<thread> hilos;
    long long bloque = N / numHilos;

    for (int t = 0; t < numHilos; t++) {
        long long inicio = t * bloque + (t == 0 ? 2 : 0);
        long long fin = (t == numHilos - 1) ? N : (t + 1) * bloque;
        hilos.emplace_back(primosMultihilos, inicio, fin, cref(primosBase), ref(primosGlobal));
    }

    for (auto& h : hilos) h.join();

    sort(primosGlobal.begin(), primosGlobal.end()); // ordenar porque se insertan desordenados
    return primosGlobal;
}

// programa principal 
int main() {
    long long N;
    cout << "Ingrese un numero N (>= 1e7 recomendado): ";
    cin >> N;

    // secuencial 
    auto inicioSec = high_resolution_clock::now();
    vector<long long> primosS = primosSecuencial(N);
    auto finSec = high_resolution_clock::now();
    double tiempoSec = duration_cast<duration<double>>(finSec - inicioSec).count();

    cout << "\n[Secuencial]\n";
    cout << "Cantidad de primos menores que " << N << ": " << primosS.size() << "\n";
    cout << "Los 10 mayores primos: ";
    for (int i = max(0, (int)primosS.size() - 10); i < primosS.size(); i++) {
        cout << primosS[i] << " ";
    }
    cout << "\nTiempo: " << tiempoSec << " segundos\n";

    // multihilos

    // ---chtgpt nos recomendo utlizar esto para mayor eficiencia---
    int numHilos = thread::hardware_concurrency(); // detecta nucleos disponibles
    if (numHilos == 0) numHilos = 8; 

    auto inicioMT = high_resolution_clock::now();
    vector<long long> primosM = primosMultihilo(N, numHilos);
    auto finMT = high_resolution_clock::now();
    double tiempoMT = duration_cast<duration<double>>(finMT - inicioMT).count();

    cout << "\n[Multihilo con " << numHilos << " hilos]\n";
    cout << "Cantidad de primos menores que " << N << ": " << primosM.size() << "\n";
    cout << "Los 10 mayores primos: ";
    for (int i = max(0, (int)primosM.size() - 10); i < primosM.size(); i++) {
        cout << primosM[i] << " ";
    }
    cout << "\nTiempo: " << tiempoMT << " segundos\n";

    // speedup
    double speedup = tiempoSec / tiempoMT;
    cout << "\n[Speedup] = " << speedup << "\n";

    return 0;
}
