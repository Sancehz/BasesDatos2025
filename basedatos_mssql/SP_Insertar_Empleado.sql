CREATE PROCEDURE sp_Insertar_Empleado
	-- Params
	@NombreP varchar(64),
	@SalarioP money
AS
-- Revisamos que el usuario no exista para mantener consistencia
IF (SELECT count(Nombre) FROM dbo.Empleado WHERE Nombre = @NombreP) != 0
	RETURN 1; -- Error ewwww

-- Utilizamos un try catch para mantener ACID
BEGIN TRY
	INSERT INTO dbo.Empleado (Nombre, Salario) VALUES
		(@NombreP, @SalarioP);
	RETURN 0; -- No err
END TRY
BEGIN CATCH
	RETURN 1; -- Err
END CATCH

GO
