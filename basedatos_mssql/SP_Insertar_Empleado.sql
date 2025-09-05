CREATE PROCEDURE sp_Insertar_Empleado
	-- Params
	@NombreP varchar(64),
	@SalarioP money
AS
-- Usamos un transaction para mantener ACID
BEGIN TRANSACTION
	-- Intentar insertar y commit
	BEGIN TRY
		INSERT INTO dbo.Empleado (Nombre, Salario) VALUES
			(@NombreP, @SalarioP);
		COMMIT
		RETURN 0; -- No errores
	END TRY
	-- Si falla hacemos rollback
	BEGIN CATCH
		ROLLBACK
		RETURN 1; -- Error ewwwwww
	END CATCH
COMMIT
GO
