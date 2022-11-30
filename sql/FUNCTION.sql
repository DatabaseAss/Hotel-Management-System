USE db_ass;
GO

-- FUNCT. 1
CREATE OR ALTER FUNCTION f_CheckPackage (@CUSTOMERID INT) 
RETURNS TABLE AS 
RETURN 
(
    WITH Expired_bill_service AS
    (
        SELECT  BILL_PACKAGE_NAME
                , START_DAY
                , DATEADD(YEAR, 1, START_DAY) AS EXPIRED_DATE
                , CONVERT(DATE, GETDATE()) AS PRESENT_DATE
        FROM BILL_SERVICE
        WHERE BILL_CUSTOMERID = @CUSTOMERID
    )
    , Compare_bill_service AS
    (
        SELECT  BILL_PACKAGE_NAME
                , START_DAY
                , PRESENT_DATE
                , EXPIRED_DATE
                , IIF(START_DAY > PRESENT_DATE, START_DAY, PRESENT_DATE) AS START_COUNT_DAY
        FROM Expired_bill_service
    )
    , Remain_bill_service AS
    (
        SELECT  BILL_PACKAGE_NAME
                , START_DAY
                , PRESENT_DATE
                , EXPIRED_DATE
                , DATEDIFF(day, START_COUNT_DAY, EXPIRED_DATE) AS REMAINING_DAY
        FROM Compare_bill_service
    )
    SELECT BILL_PACKAGE_NAME, PACKAGE_CAPACITY, START_DAY, EXPIRED_DATE, REMAINING_DAY
    FROM Remain_bill_service T1
    JOIN PACKAGE T2 ON T2.PACKAGE_NAME = T1.BILL_PACKAGE_NAME
)
GO
SELECT * FROM f_CheckPackage(4)
GO

--FUNCT. 2
 -- %%%%%%%%%%%%%%%%%%%% CHECKED %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CREATE OR ALTER FUNCTION f_SumGuest (@BRANCHID INT, @YEARR INT) 
RETURNS TABLE AS 
RETURN
(
    WITH receipt AS
    (
        SELECT RECEIPT_BOOKINGID, BOOKING_TIME, STAT, RECEIPT_CAPACITY
        FROM RECEIPT
        WHERE STAT = 1
    )
    , Hiring_room AS
    (
        SELECT  HR_BOOKINGID, HR_BRANCHID
        FROM HIRING_ROOM
        WHERE HR_BRANCHID = @BRANCHID
    )
    , ticket_book_room AS
    (
        SELECT  receipt.RECEIPT_BOOKINGID
                , MONTH(receipt.BOOKING_TIME) AS [Month]
                , YEAR(receipt.BOOKING_TIME) as [Year]
                , receipt.RECEIPT_CAPACITY
        FROM receipt JOIN Hiring_room ON receipt.RECEIPT_BOOKINGID = Hiring_room.HR_BOOKINGID
    )
    , Receipt_by_month AS
    (
        SELECT Month
                , SUM(RECEIPT_CAPACITY) AS [TOTAL_GUESTS_MONTH]
        FROM ticket_book_room
        WHERE [Year] = @YEARR
        GROUP BY Month
    )
    SELECT * FROM Receipt_by_month
)
GO
SELECT * FROM f_SumGuest(1, 2022)
GO
