<?php 

	$ENV_SERVER = 1;

	if ($ENV_SERVER == 0) {
		$cons_usuario="root";
		$cons_contra="";
		$cons_base_datos="stats";
		$cons_equipo="localhost";
	} else {
		$cons_usuario="felipe";
		$cons_contra="12345678";
		$cons_base_datos="stats";
		$cons_equipo="localhost";
	}
	$obj_conexion = mysqli_connect($cons_equipo,$cons_usuario,$cons_contra,$cons_base_datos);
	if(!$obj_conexion)
	{
		//echo "<h3>No se ha podido conectar PHP - MySQL, verifique sus datos.</h3><hr><br>";
	}
	else
	{
		//echo "<h3>Conexion Exitosa PHP - MySQL</h3><hr><br>";
	}
		
	$var_consulta= "INSERT INTO execution_mode (type,election) VALUES (".$_POST["modo"].",".$_POST["opcion"].");";
    $var_resultado = $obj_conexion->query($var_consulta);
<<<<<<< HEAD
	//$var_resultado = mysqli_fetch_assoc($var_resultado);
	
	//exec
	//$command = escapeshellcmd('python3 /var/www/phpmyadmin/bot/mainBot.py &');
	$command = "/usr/bin/python3 /var/www/phpmyadmin/bot/mainBot.py > /dev/null &";

	$output = exec($command);
	echo $output;
	echo "blablablablabla";
=======

	if (isset($_POST["stack"])) {
		$sym = strtoupper($_POST["stack"]);
	}
	$var_consulta= "INSERT INTO arbitraje_sym (symbol) VALUE ('".$sym."');";
    $var_resultado = $obj_conexion->query($var_consulta);
	
	
>>>>>>> ac8d5d7c8e133c383a65591c69aa469b2bec03f1
