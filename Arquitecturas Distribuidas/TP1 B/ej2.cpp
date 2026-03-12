#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <thread>
#include <chrono>

using namespace std;
using namespace std::chrono;

// Funcion naive: cuenta cuántas veces aparece pattern en text
int naiveSearch(const string& text, const string& pattern) {
    int n = text.size();
    int m = pattern.size();
    if (m == 0) return 0;

    int count = 0;
    for (int i = 0; i <= n - m; i++) {
        int j = 0;
        while (j < m && text[i + j] == pattern[j]) j++;
        if (j == m) count++;
    }
    return count;
}

// funcion para cada hilo
void searchPattern(const string& text, const string& pattern, int index, vector<int>& results) {
    results[index] = naiveSearch(text, pattern);
}

int main() {
    // leer texto
    ifstream textFile("texto.txt");
    if (!textFile) {
        cerr << "No se pudo abrir texto.txt\n";
        return 1;
    }
    string text((istreambuf_iterator<char>(textFile)), istreambuf_iterator<char>());
    textFile.close();

    // leer patrones
    ifstream patternFile("patrones.txt");
    if (!patternFile) {
        cerr << "No se pudo abrir patrones.txt\n";
        return 1;
    }
    vector<string> patterns;
    string line;
    while (getline(patternFile, line)) patterns.push_back(line);
    patternFile.close();

    vector<int> results(patterns.size(), 0);

    // ===== busqueda serial =====
    auto startSerial = high_resolution_clock::now();
    for (size_t i = 0; i < patterns.size(); i++) {
        results[i] = naiveSearch(text, patterns[i]);
    }
    auto endSerial = high_resolution_clock::now();
    auto durationSerial = duration_cast<duration<double>>(endSerial - startSerial).count();

    cout << "Resultados serial:\n";
    for (size_t i = 0; i < results.size(); i++)
        cout << "el patron " << i << " aparece " << results[i] << " veces\n";
    cout << "Tiempo serial: " << durationSerial << " segundos\n\n";

    // ===== busqueda con 32 hilos =====
    results.assign(patterns.size(), 0);
    vector<thread> threads;

    auto startThreads = high_resolution_clock::now();
    for (size_t i = 0; i < patterns.size(); i++) {
        threads.emplace_back(searchPattern, cref(text), cref(patterns[i]), i, ref(results));
    }
    for (auto& t : threads) t.join();
    auto endThreads = high_resolution_clock::now();
    auto durationThreads = duration_cast<duration<double>>(endThreads - startThreads).count();

    cout << "Resultados multihilo:\n";
    for (size_t i = 0; i < results.size(); i++)
        cout << "el patron " << i << " aparece " << results[i] << " veces\n";
    cout << "Tiempo multihilo: " << durationThreads << " segundos\n";

    // speedup = T/S
    // T = tiempo que tarda el programa sin hilos
    // S = iempo que tarda el programa con hilos
    double speedup = durationSerial / durationThreads;
    cout << "\nSpeedup: " << speedup << "\n";

    return 0;
}
