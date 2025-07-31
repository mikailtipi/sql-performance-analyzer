USE [YourDatabase]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

-- Author: Mikail Tipi
-- Description: Runs any SQL query, measures execution time and affected rows.
-- Stores logs in a generic logging table for performance diagnostics.

CREATE PROCEDURE [dbo].[RunAndMeasure]
    @Query NVARCHAR(MAX)
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @StartTime DATETIME = GETDATE();
    DECLARE @RowCount INT = 0;

    BEGIN TRY
        EXEC sp_executesql @Query;
        SET @RowCount = @@ROWCOUNT;
    END TRY
    BEGIN CATCH
        INSERT INTO dbo.QueryPerformanceLog(QueryText, ExecutionTimeMs, AffectedRows, RunDate)
        VALUES (@Query, -1, -1, GETDATE());

        SELECT 
            'ERROR' AS Label, 
            ERROR_MESSAGE() AS Value;
        RETURN;
    END CATCH

    DECLARE @ElapsedTimeMs INT = DATEDIFF(MILLISECOND, @StartTime, GETDATE());

    INSERT INTO dbo.QueryPerformanceLog(QueryText, ExecutionTimeMs, AffectedRows, RunDate)
    VALUES (@Query, @ElapsedTimeMs, @RowCount, GETDATE());

    SELECT 
        CAST(@ElapsedTimeMs AS INT) AS DurationMs,
        CAST(@RowCount AS INT) AS AffectedRows;
END
