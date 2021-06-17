<?php 

	$ENV_SERVER = 0;

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
	/*if(!$obj_conexion)
	{
		echo "<h3>No se ha podido conectar PHP - MySQL, verifique sus datos.</h3><hr><br>";
	}
	else
	{
		echo "<h3>Conexion Exitosa PHP - MySQL</h3><hr><br>";
	}*/
	
	//print_r ($_POST);
	
 	$var_consulta= "SELECT * FROM execution_mode WHERE id=(SELECT MAX(id) FROM execution_mode)";
    $var_resultado = $obj_conexion->query($var_consulta);
    $var_resultado = mysqli_fetch_assoc($var_resultado);

    echo $var_resultado["type"];