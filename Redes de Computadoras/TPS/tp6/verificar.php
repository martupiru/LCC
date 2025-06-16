<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Resultado de la Encuesta</title>
  <link rel="stylesheet" href="style.css"> <!-- reutiliza tu CSS -->
  <style>
    body {
      text-align: center;
      background-color: #e9f7fc;
      font-family: Arial, sans-serif;
      padding: 30px;
    }
    h2, h3 {
      color: #2c3e50;
    }
    ul {
      list-style: none;
      padding: 0;
    }
    li {
      background-color: #ffffff;
      margin: 10px auto;
      padding: 10px;
      border-radius: 10px;
      width: 300px;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    button {
      background-color: #3498db;
      color: white;
      padding: 10px 20px;
      margin-top: 20px;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      transition: background-color 0.3s ease;
      font-size: 1rem;
    }
    button:hover {
      background-color: #2980b9;
    }
  </style>
</head>
<body>

<?php
$email = $_POST["email"];
$estacion = $_POST["estacion"];
$archivo_votos = "votos.txt";
$archivo_estadisticas = "estadisticas.txt";

// Verificar si ya votó
$votos_existentes = file_exists($archivo_votos) ? file($archivo_votos, FILE_IGNORE_NEW_LINES) : [];

$ya_voto = false;
foreach ($votos_existentes as $linea) {
    list($correo, $opcion) = explode(";", $linea);
    if (trim($correo) == trim($email)) {
        $ya_voto = true;
        break;
    }
}

if ($ya_voto) {
    echo "<h2>Usted ya votó. No puede votar dos veces.</h2>";
} else {
    // Registrar voto
    file_put_contents($archivo_votos, "$email;$estacion\n", FILE_APPEND);

    // Actualizar estadísticas
    $estadisticas = [
        "Otoño" => 0,
        "Invierno" => 0,
        "Primavera" => 0,
        "Verano" => 0
    ];

    if (file_exists($archivo_estadisticas)) {
    $lineas = file($archivo_estadisticas, FILE_IGNORE_NEW_LINES);
    foreach ($lineas as $linea) {
        if (trim($linea) === '') continue; // Ignora líneas vacías

        $partes = explode(";", $linea);
        if (count($partes) !== 2) continue; // Ignora líneas mal formadas

        list($nombre, $cantidad) = $partes;
        $estadisticas[$nombre] = (int)$cantidad;
    }
}


    $estadisticas[$estacion]++;

    // Guardar estadísticas
    $contenido = "";
    foreach ($estadisticas as $clave => $valor) {
        $contenido .= "$clave;$valor\n";
    }
    file_put_contents($archivo_estadisticas, $contenido);

    // Mostrar resultados
    echo "<h2>¡Gracias por votar!</h2>";
    echo "<h3>Resultados hasta el momento:</h3>";
    echo "<ul>";
    foreach ($estadisticas as $clave => $valor) {
        echo "<li>$clave: $valor votos</li>";
    }
echo '<form action="index.html" method="GET" style="background-color: transparent; box-shadow: none; border: none; margin-top: 30px;">
        <button type="submit">Volver a votar</button>
      </form>';


    echo "</ul>";

}
?>
</body>
</html>
