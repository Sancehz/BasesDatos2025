
CREATE TABLE dbo.Empleado2
(
	Id int IDENTITY(1,1) PRIMARY KEY NOT NULL,
	Nombre varchar(64) NOT NULL,
	Salario money NOT NULL,
)