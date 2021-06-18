<?php

function create_conn ()
{
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
		echo "<h3>No se ha podido conectar PHP - MySQL, verifique sus datos.</h3><hr><br>";
	}
	else
	{
		#echo "<h3>Conexion Exitosa PHP - MySQL</h3><hr><br>";
	}

	return $obj_conexion;
}


function insert_mode ($options)
{
$obj_conexion = create_conn();
	
	//$var_consulta= "SELECT * FROM execution_mode";
	$var_consulta= "INSERT INTO execution_mode (type,election) VALUES (".$options[0].",".$options[1].")";
    $var_resultado = $obj_conexion->query($var_consulta);
	$var_resultado = mysqli_fetch_assoc($var_resultado);
	
	return $var_resultado;
}


function get_mode ()
{
	$obj_conexion = create_conn();
	
	$var_consulta= "SELECT * FROM execution_mode WHERE id=(SELECT MAX(id) FROM execution_mode)";
    $var_resultado = $obj_conexion->query($var_consulta);
	$var_resultado = mysqli_fetch_assoc($var_resultado);
	
	return $var_resultado;
}

function get_actual_pair($mode)
{
	$obj_conexion = create_conn();
	if ($mode == "TRADING MODE") 
		$var_consulta= "SELECT * FROM trading_stats WHERE id=(SELECT MAX(id) FROM trading_stats)";
	else 
		$var_consulta= "SELECT * FROM arbitraje_stats WHERE id=(SELECT MAX(id) FROM arbitraje_stats)";
    
	$var_resultado = $obj_conexion->query($var_consulta);
	$var_resultado = mysqli_fetch_assoc($var_resultado);
	
	return $var_resultado;
}
?>

