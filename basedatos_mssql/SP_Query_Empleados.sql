CREATE PROCEDURE sp_Query_Empleados
	-- No params
AS
BEGIN
	SELECT Id, Nombre, Salario 
		FROM dbo.Empleado
		ORDER BY Nombre
END
GO
