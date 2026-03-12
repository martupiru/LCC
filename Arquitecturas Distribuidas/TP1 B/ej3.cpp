#include <iostream>
#include <vector>
#include <thread>
#include <chrono>

using namespace std;
using namespace std::chrono;

// creo la matriz
using Matrix = vector<vector<float>>;

// genero una matriz NxN con valor inicial
Matrix createMatrix(int N, float value) {
    return Matrix(N, vector<float>(N, value));
}

// miultiplicaion matricial con sumatoria incluida
double multiplySerial(const Matrix& A, const Matrix& B, Matrix& C) {
    int N = A.size();
    double total = 0.0;

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            float val = 0.0f;
            for (int k = 0; k < N; k++) {
                val += A[i][k] * B[k][j];
            }
            C[i][j] = val;
            total += val; // sumamos directamente
        }
    }
    return total;
}

// Multiplicación matricial para hilos con sumatoria parcial
void multiplyPartial(const Matrix& A, const Matrix& B, Matrix& C, int startRow, int endRow, double& partialSum) {
    int N = A.size();
    double localSum = 0.0;

    for (int i = startRow; i < endRow; i++) {
        for (int j = 0; j < N; j++) {
            float val = 0.0f;
            for (int k = 0; k < N; k++) {
                val += A[i][k] * B[k][j];
            }
            C[i][j] = val;
            localSum += val;
        }
    }
    partialSum = localSum;
}

// multiplicacion de matrices con hilos
double multiplyParallel(const Matrix& A, const Matrix& B, Matrix& C, int numThreads) {
    int N = A.size();
    vector<thread> threads;
    vector<double> partialSums(numThreads, 0.0);

    int rowsPerThread = N / numThreads;
    int extra = N % numThreads;
    int currentRow = 0;

    for (int t = 0; t < numThreads; t++) {
        int startRow = currentRow;
        int endRow = startRow + rowsPerThread + (t < extra ? 1 : 0);
        threads.emplace_back(multiplyPartial, cref(A), cref(B), ref(C), startRow, endRow, ref(partialSums[t]));
        currentRow = endRow;
    }
    
    for (auto& th : threads) th.join();

    // sumatoria total
    double total = 0.0;
    for (double s : partialSums) total += s;
    return total;
}

// imprime esquinas de una matriz
void printCorners(const Matrix& M) {
    int N = M.size();
    cout << "Esquinas: "
         << M[0][0] << "  " << M[0][N-1] << "  "
         << M[N-1][0] << "  " << M[N-1][N-1] << "\n";
}

int main() {
    int N;
    cout << "Ingrese el orden de la matriz (entre 1 y 3000): ";
    cin >> N;

    if (N < 1 || N > 3000) {
        cerr << "Error: N debe estar entre 1 y 3000.\n";
        return 1;
    }

    int numThreads = 10;  // se pueden probar 10 o 20 hilos

    Matrix A = createMatrix(N, 0.1f);
    Matrix B = createMatrix(N, 0.2f);
    Matrix C_serial(N, vector<float>(N, 0.0f));
    Matrix C_parallel(N, vector<float>(N, 0.0f));

    cout << "\nMatriz A:\n";
    printCorners(A);
    cout << "Matriz B:\n";
    printCorners(B);

    // ===== Serial =====
    auto startSerial = high_resolution_clock::now();
    double sumSerial = multiplySerial(A, B, C_serial);
    auto endSerial = high_resolution_clock::now();
    double timeSerial = duration_cast<duration<double>>(endSerial - startSerial).count();

    cout << "\nResultado Serial:\n";
    printCorners(C_serial);
    cout << "Sumatoria: " << sumSerial << "\n";
    cout << "Tiempo serial: " << timeSerial << " segundos\n";

    // ===== Multihilo =====
    auto startParallel = high_resolution_clock::now();
    double sumParallel = multiplyParallel(A, B, C_parallel, numThreads);
    auto endParallel = high_resolution_clock::now();
    double timeParallel = duration_cast<duration<double>>(endParallel - startParallel).count();

    cout << "\nResultado Multihilo:\n";
    printCorners(C_parallel);
    cout << "Sumatoria: " << sumParallel << "\n";
    cout << "Tiempo multihilo: " << timeParallel << " segundos\n";

    // ===== Speedup =====
    double speedup = timeSerial / timeParallel;
    cout << "\nSpeedup: " << speedup << "\n";

    return 0;
}
